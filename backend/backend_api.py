"""
Flask/FastAPI Backend for React Frontend
Provides REST API endpoints for the Business Intelligence Analyst
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
import sys
import os
import pandas as pd
import numpy as np
import json
from datetime import timedelta, datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import io
import base64

# Add backend directory to path (src is now inside backend)
current_file = os.path.abspath(__file__)  # Full path to backend_api.py
backend_dir = os.path.dirname(current_file)  # backend
sys.path.insert(0, backend_dir)  # Add backend to path so we can import from src

# Now we can import from src
from src.models.sentiment_analyzer import SentimentAnalyzer
from src.utils.text_preprocessor import TextPreprocessor
from src.models.cognitive_agent import BusinessIntelligenceAgent
from auth import (
    authenticate_user,
    create_access_token,
    verify_token,
    get_all_users,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
import pickle
import networkx as nx

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)  # Enable CORS for React frontend

# Initialize components
analyzer = SentimentAnalyzer(method='vader')
preprocessor = TextPreprocessor()

# Load models if available
try:
    kg_path = os.path.join(backend_dir, 'data', 'models', 'knowledge_graph.pkl')
    with open(kg_path, 'rb') as f:
        knowledge_graph = pickle.load(f)
except:
    knowledge_graph = None

# Initialize cognitive agent
agent = BusinessIntelligenceAgent(analyzer, preprocessor, knowledge_graph)

# Load data - try Milestone 2 output first, then Milestone 1 output
df_reviews = pd.DataFrame()
try:
    # First try: Milestone 2 output (with sentiment already analyzed)
    reviews_path = os.path.join(backend_dir, 'data', 'processed', 'reviews_with_sentiment.csv')
    if os.path.exists(reviews_path):
        df_reviews = pd.read_csv(reviews_path)
        print(f"✅ Loaded {len(df_reviews)} reviews from Milestone 2 output (reviews_with_sentiment.csv)")
    else:
        # Fallback: Milestone 1 output (needs sentiment analysis)
        cleaned_path = os.path.join(backend_dir, 'data', 'processed', 'cleaned_reviews.csv')
        if os.path.exists(cleaned_path):
            df_reviews = pd.read_csv(cleaned_path)
            print(f"✅ Loaded {len(df_reviews)} reviews from Milestone 1 output (cleaned_reviews.csv)")
            # If sentiment column doesn't exist, we'll analyze it on-the-fly
            if 'sentiment' not in df_reviews.columns:
                print("⚠️  No sentiment column found. Will analyze sentiment on-the-fly for forecast generation.")
        else:
            print("⚠️  No review data found. Please run Milestone 1 notebook first.")
            df_reviews = pd.DataFrame()
except Exception as e:
    print(f"⚠️  Error loading review data: {e}")
    df_reviews = pd.DataFrame()

# In-memory notification storage (in production, use database)
notifications_storage = []


def token_required(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        payload = verify_token(token)
        if not payload:
            return jsonify({'error': 'Token is invalid or expired'}), 401
        
        request.current_user = payload
        return f(*args, **kwargs)
    return decorated


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'API is running'})


@app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
def login():
    """User login endpoint"""
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    try:
        # Check if request has JSON data
        if not request.is_json:
            print("ERROR: Request is not JSON")
            print(f"Content-Type: {request.content_type}")
            print(f"Headers: {dict(request.headers)}")
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        data = request.get_json(force=True)  # Force JSON parsing
        if not data:
            print("ERROR: No data in request body")
            print(f"Raw data: {request.data}")
            return jsonify({'error': 'Request body is required'}), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        print(f"Login attempt: email={email}, password_length={len(password) if password else 0}")
        print(f"Data received: {data}")
        
        if not email or not password:
            print(f"ERROR: Missing email or password - email={bool(email)}, password={bool(password)}")
            return jsonify({'error': 'Email and password are required'}), 400
        
        user = authenticate_user(email, password)
        if not user:
            print(f"Authentication failed for: {email}")
            # Test authentication directly for debugging
            from auth import find_user_by_email, hash_password
            test_user = find_user_by_email(email)
            if test_user:
                print(f"User found, testing password...")
                test_hash = hash_password(password)
                print(f"Provided password hash: {test_hash[:20]}...")
                print(f"Stored password hash: {test_user['password'][:20]}...")
                print(f"Match: {test_hash == test_user['password']}")
            else:
                print(f"User not found in database")
            return jsonify({'error': 'Invalid email or password'}), 401
        
        print(f"Authentication successful for: {email}")
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={'sub': user['email'], 'user_id': user['id'], 'role': user['role']},
            expires_delta=access_token_expires
        )
        
        # Extract surname from name
        from auth import extract_surname
        surname = extract_surname(user.get('name', ''))
        
        response_data = {
            'token': access_token,
            'user': {
                'id': user['id'],
                'email': user['email'],
                'name': user['name'],
                'surname': surname,
                'role': user['role'],
            },
            'message': 'Login successful'
        }
        print(f"Login successful, returning response for: {email}")
        return jsonify(response_data), 200
    except Exception as e:
        print(f"ERROR in login endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/me', methods=['GET'])
@token_required
def get_current_user():
    """Get current authenticated user"""
    try:
        user_id = request.current_user.get('user_id')
        # In production, fetch from database
        # For now, return from token
        return jsonify({
            'id': user_id,
            'email': request.current_user.get('sub'),
            'role': request.current_user.get('role'),
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/users', methods=['GET'])
@token_required
def get_users():
    """Get all users (admin only)"""
    try:
        if request.current_user.get('role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        users = get_all_users()
        return jsonify({'users': users, 'count': len(users)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/sentiment/analyze', methods=['POST'])
@token_required
def analyze_sentiment():
    """Analyze sentiment for a single text with enhanced robustness"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        text = data.get('text', '')
        method = data.get('method', 'ensemble')  # Get method from request, default to ensemble
        
        # Validate method
        valid_methods = ['vader', 'textblob', 'transformer', 'ensemble']
        if method not in valid_methods:
            method = 'ensemble'
        
        # Create analyzer with selected method
        method_analyzer = SentimentAnalyzer(method=method, use_ensemble=(method == 'ensemble'))
        
        # Validate input
        from src.utils.robustness_validator import RobustnessValidator
        validator = RobustnessValidator()
        is_valid, error_msg = validator.validate_text_input(text)
        
        if not is_valid:
            return jsonify({
                'error': error_msg or 'Invalid text input',
                'sentiment': 'neutral',
                'confidence': 0.0
            }), 400
        
        # Analyze with enhanced robustness
        try:
            result = method_analyzer.analyze(text)
        except ValueError as e:
            # Handle case where method raises an exception
            error_msg = str(e)
            if 'not available' in error_msg.lower():
                # Fallback to VADER or TextBlob
                print(f"⚠️  {error_msg}, falling back to VADER")
                try:
                    fallback_analyzer = SentimentAnalyzer(method='vader', use_ensemble=False)
                    result = fallback_analyzer.analyze(text)
                    result['warning'] = f'{method.capitalize()} method not available. Results shown using VADER instead.'
                except:
                    # Final fallback to TextBlob
                    print("⚠️  VADER also not available, falling back to TextBlob")
                    fallback_analyzer = SentimentAnalyzer(method='textblob', use_ensemble=False)
                    result = fallback_analyzer.analyze(text)
                    result['warning'] = f'{method.capitalize()} method not available. Results shown using TextBlob instead.'
            else:
                raise
        
        # Check if method is not available (returned as error in result, not exception)
        if result.get('error') and 'not available' in result.get('error', '').lower():
            # Method not available, try fallback
            print(f"⚠️  {result.get('error')}, attempting fallback")
            try:
                if method != 'vader':
                    fallback_analyzer = SentimentAnalyzer(method='vader', use_ensemble=False)
                    result = fallback_analyzer.analyze(text)
                    result['warning'] = f'{method.capitalize()} method not available. Results shown using VADER instead.'
                else:
                    fallback_analyzer = SentimentAnalyzer(method='textblob', use_ensemble=False)
                    result = fallback_analyzer.analyze(text)
                    result['warning'] = f'{method.capitalize()} method not available. Results shown using TextBlob instead.'
            except Exception as fallback_error:
                print(f"⚠️  Fallback also failed: {fallback_error}")
                # Ensure result has required fields even if fallback fails
                if 'pos' not in result or result.get('pos') is None:
                    result['compound'] = 0.0
                    result['pos'] = 0.0
                    result['neu'] = 1.0
                    result['neg'] = 0.0
                    result['positive'] = 0.0
                    result['neutral'] = 1.0
                    result['negative'] = 0.0
        
        # Validate result
        is_valid_result, result_error = validator.validate_sentiment_result(result)
        if not is_valid_result:
            return jsonify({
                'error': result_error or 'Invalid analysis result',
                'sentiment': 'neutral',
                'confidence': 0.0
            }), 500
        
        # Extract pos/neu/neg from nested vader_result if present
        pos = result.get('pos', 0.0)
        neu = result.get('neu', 0.0)
        neg = result.get('neg', 0.0)
        
        # If not at top level, try to get from vader_result
        if pos == 0.0 and neu == 0.0 and neg == 0.0:
            vader_result = result.get('vader_result', {})
            if vader_result:
                pos = vader_result.get('pos', vader_result.get('positive', 0.0))
                neu = vader_result.get('neu', vader_result.get('neutral', 0.0))
                neg = vader_result.get('neg', vader_result.get('negative', 0.0))
        
        # If still zero, try alternative field names
        if pos == 0.0 and neu == 0.0 and neg == 0.0:
            pos = result.get('positive', 0.0)
            neu = result.get('neutral', 0.0)
            neg = result.get('negative', 0.0)
        
        # Ensure all required fields are present with proper format
        response_data = {
            'sentiment': result.get('sentiment', 'neutral'),
            'compound': result.get('compound', 0.0),
            'pos': pos,
            'neu': neu,
            'neg': neg,
            'positive': pos,
            'neutral': neu,
            'negative': neg,
            'confidence': result.get('confidence', 0.0),
        }
        
        # Add any additional fields
        if 'details' in result:
            response_data['details'] = result['details']
        if 'method' in result:
            response_data['method'] = result['method']
        
        # Add topic information if available
        if 'topic_id' in result:
            response_data['topic_id'] = result.get('topic_id')
            response_data['topic_name'] = result.get('topic_name', 'Unknown Topic')
            response_data['topic_confidence'] = result.get('topic_confidence', 0.0)
        
        print(f"Sentiment analysis result: {response_data}")
        return jsonify(response_data)
    except Exception as e:
        import traceback
        return jsonify({
            'error': str(e),
            'sentiment': 'neutral',
            'confidence': 0.0,
            'warning': 'Error during analysis'
        }), 500


@app.route('/api/sentiment/batch', methods=['POST'])
@token_required
def batch_analyze_sentiment():
    """Batch analyze sentiment for multiple texts"""
    try:
        data = request.json
        texts = data.get('texts', [])
        
        if not texts:
            return jsonify({'error': 'Texts array is required'}), 400
        
        results = [analyzer.analyze(text) for text in texts]
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def predict_topic_for_text(text):
    """Predict the most likely topic for a given text using LDA model"""
    try:
        from gensim.models import LdaModel
        from gensim import corpora
        import re
        
        lda_path = os.path.join(backend_dir, 'data', 'models', 'lda_model')
        if not os.path.exists(lda_path):
            return None
        
        # Load LDA model
        lda_model = LdaModel.load(lda_path)
        
        # Preprocess text (simple tokenization and cleaning)
        text_lower = text.lower()
        # Remove special characters, keep words
        words = re.findall(r'\b[a-z]+\b', text_lower)
        
        if not words:
            return None
        
        # Try to load dictionary if available
        dict_path = os.path.join(backend_dir, 'data', 'models', 'dictionary.pkl')
        dictionary = None
        if os.path.exists(dict_path):
            try:
                import pickle
                with open(dict_path, 'rb') as f:
                    dictionary = pickle.load(f)
            except:
                pass
        
        # Create document representation
        if dictionary:
            # Use existing dictionary
            doc_bow = dictionary.doc2bow(words)
        else:
            # Create simple frequency dictionary
            word_freq = {}
            for word in words:
                word_freq[word] = word_freq.get(word, 0) + 1
            doc_bow = [(i, freq) for i, (word, freq) in enumerate(word_freq.items())]
        
        # Get topic distribution
        topic_dist = lda_model.get_document_topics(doc_bow, minimum_probability=0.0)
        
        if not topic_dist:
            return None
        
        # Get the topic with highest probability
        best_topic = max(topic_dist, key=lambda x: x[1])
        topic_id = best_topic[0]
        confidence = float(best_topic[1])
        
        # Get topic name
        try:
            topic_words = lda_model.show_topic(topic_id, topn=10)
            topic_words_list = [(word, weight) for word, weight in topic_words]
            topic_name = generate_topic_name(topic_words_list)
        except:
            topic_name = f"Topic {topic_id}"
        
        return {
            'topic_id': topic_id,
            'topic_name': topic_name,
            'confidence': confidence
        }
    except Exception as e:
        print(f"⚠️  Error predicting topic: {e}")
        return None


def generate_topic_name(topic_words):
    """Generate a meaningful name for a topic based on top words"""
    if not topic_words:
        return "General Discussion"
    
    # Get top words (up to 5 for better matching)
    top_words = [word.lower() for word, _ in topic_words[:5]]
    top_3_words = top_words[:3]
    
    # Enhanced topic name mappings with specific examples
    topic_mappings = [
        # Delivery-related
        (['delivery', 'late', 'delay'], 'Late Delivery'),
        (['delivery', 'fast', 'quick'], 'Fast Delivery'),
        (['delivery', 'time', 'on'], 'Delivery Timing'),
        (['delivery', 'service'], 'Delivery Service'),
        
        # Service quality
        (['service', 'good', 'great'], 'Good Service'),
        (['service', 'excellent'], 'Excellent Service'),
        (['service', 'poor', 'bad'], 'Poor Service'),
        (['service', 'customer'], 'Customer Service'),
        
        # Location-specific
        (['nakawa', 'demand'], 'Demand in Nakawa'),
        (['nakawa'], 'Nakawa Area'),
        (['kampala'], 'Kampala'),
        (['location', 'area'], 'Location & Area'),
        
        # Product quality
        (['product', 'quality', 'good'], 'Product Quality'),
        (['product', 'excellent'], 'Excellent Products'),
        (['quality', 'high'], 'High Quality'),
        
        # Pricing
        (['price', 'affordable'], 'Affordable Pricing'),
        (['price', 'expensive'], 'Expensive Pricing'),
        (['price', 'cost'], 'Pricing & Cost'),
        (['value', 'money'], 'Value for Money'),
        
        # Staff/Support
        (['staff', 'friendly'], 'Friendly Staff'),
        (['staff', 'helpful'], 'Helpful Staff'),
        (['support', 'customer'], 'Customer Support'),
        
        # Speed/Efficiency
        (['fast', 'quick'], 'Fast Service'),
        (['efficient', 'speed'], 'Efficiency & Speed'),
        (['time', 'wait'], 'Waiting Time'),
        
        # General patterns
        (['service', 'delivery'], 'Service & Delivery'),
        (['product', 'price'], 'Product & Pricing'),
        (['business', 'shop'], 'Business Operations'),
        (['experience', 'great'], 'Great Experience'),
    ]
    
    # Try to match with known patterns (check if all words in pattern are in top_words)
    for pattern, name in topic_mappings:
        if all(any(p in word or word in p for word in top_words) for p in pattern):
            return name
    
    # Generate descriptive name from top words
    # Create a phrase from the most relevant words
    if len(top_3_words) >= 2:
        # Combine words intelligently
        if 'nakawa' in top_words or 'kampala' in top_words:
            location = 'nakawa' if 'nakawa' in top_words else 'kampala'
            other_words = [w for w in top_3_words if w not in [location]]
            if other_words:
                return f"{other_words[0].capitalize()} in {location.capitalize()}"
        
        # Create natural phrase
        return f"{top_3_words[0].capitalize()} {top_3_words[1].capitalize()}"
    
    # Fallback: use first word
    return f"{top_words[0].capitalize()} Discussion" if top_words else "General Discussion"


@app.route('/api/topics', methods=['GET'])
@token_required
def get_topics():
    """Get topics from LDA model with meaningful names"""
    try:
        # Load LDA model if available
        try:
            from gensim.models import LdaModel
            lda_path = os.path.join(backend_dir, 'data', 'models', 'lda_model')
            
            if not os.path.exists(lda_path):
                print("⚠️  LDA model not found at:", lda_path)
                # Return user-friendly message but don't return 404 so frontend can still display
                return jsonify({
                    'error': 'Topic models are being generated. Please check back shortly.',
                    'message': 'Topic models are being processed and will be available soon.',
                    'topics': []
                }), 200
            
            lda_model = LdaModel.load(lda_path)
            
            # Get number of topics from model
            num_topics = lda_model.num_topics
            
            topics = []
            for topic_id in range(num_topics):
                try:
                    topic_words = lda_model.show_topic(topic_id, topn=10)
                    topic_words_list = [(word, weight) for word, weight in topic_words]
                    topic_name = generate_topic_name(topic_words_list)
                    
                    # Calculate review count for this topic
                    review_count = 0
                    if 'topic' in df_reviews.columns:
                        review_count = len(df_reviews[df_reviews.get('topic', -1) == topic_id])
                    
                    topics.append({
                        'topic_id': topic_id,
                        'topic_name': topic_name,
                        'topic_words': [{'word': word, 'weight': float(weight)} for word, weight in topic_words_list],
                        'review_count': review_count
                    })
                except Exception as e:
                    print(f"Error processing topic {topic_id}: {e}")
                    continue
            
            if not topics:
                return jsonify({
                    'error': 'No topics could be loaded from the model.',
                    'topics': []
                }), 404
            
            return jsonify(topics)
        except ImportError:
            return jsonify({
                'error': 'Gensim library not available. Please install gensim to use topic modeling.',
                'topics': []
            }), 500
        except Exception as e:
            print(f"Error loading topics: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({
                'error': f'Error loading topic models: {str(e)}. Please ensure Milestone 2 notebook has been run.',
                'topics': []
            }), 500
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e), 'topics': []}), 500


def generate_forecast_from_reviews(df_reviews, forecast_days=7):
    """Generate forecast from review data using Moving Average, Linear Trend, and ARIMA methods"""
    try:
        if df_reviews.empty:
            print("⚠️  No review data available for forecast generation")
            return None
        
        # Work with a copy to avoid modifying original dataframe
        df_work = df_reviews.copy()
        
        # Check if sentiment column exists, if not analyze on-the-fly
        if 'sentiment' not in df_work.columns:
            print("📊 Analyzing sentiment for reviews on-the-fly...")
            if 'text' not in df_work.columns and 'cleaned_text' not in df_work.columns:
                print("⚠️  No text column found. Cannot analyze sentiment.")
                return None
            
            text_column = 'text' if 'text' in df_work.columns else 'cleaned_text'
            
            # Analyze sentiment (sample for performance if too many)
            max_analyze = 1000
            total_reviews = len(df_work)
            sample_size = min(max_analyze, total_reviews)
            
            if total_reviews > sample_size:
                sample_df = df_work.sample(n=sample_size, random_state=42)
            else:
                sample_df = df_work
            
            sentiments = []
            print(f"   Analyzing sentiment for {len(sample_df)} reviews (sampled from {total_reviews})...")
            for idx, row in sample_df.iterrows():
                try:
                    text = str(row[text_column]) if pd.notna(row[text_column]) else ""
                    if text:
                        result = analyzer.analyze(text)
                        sentiment = result.get('sentiment', 'neutral')
                        sentiments.append(sentiment)
                    else:
                        sentiments.append('neutral')
                except Exception as e:
                    sentiments.append('neutral')
            
            # Apply to full dataset
            if total_reviews > sample_size:
                # Map sampled sentiments back to full dataset
                sentiment_map = dict(zip(sample_df.index, sentiments))
                most_common = pd.Series(sentiments).mode()[0] if len(set(sentiments)) > 0 else 'neutral'
                all_sentiments = [sentiment_map.get(idx, most_common) for idx in df_work.index]
                df_work['sentiment'] = all_sentiments
            else:
                df_work['sentiment'] = sentiments
            
            print(f"✅ Analyzed sentiment for {len(df_work)} reviews")
        
        # Get date column
        date_column = None
        for col in ['date', 'timestamp', 'created_at', 'review_date', 'Date', 'Timestamp']:
            if col in df_work.columns:
                date_column = col
                break
        
        # Prepare dates
        if date_column:
            try:
                df_work['date_parsed'] = pd.to_datetime(df_work[date_column], errors='coerce')
                # Filter out rows with invalid dates but keep some data
                valid_dates_mask = df_work['date_parsed'].notna()
                if valid_dates_mask.sum() < len(df_work) * 0.5:
                    # If less than 50% have valid dates, use synthetic dates
                    print("⚠️  Too many invalid dates, using synthetic dates")
                    date_column = None
                else:
                    df_work = df_work[valid_dates_mask].copy()
                    if df_work.empty:
                        date_column = None
            except Exception as e:
                print(f"⚠️  Error parsing dates: {e}")
                date_column = None
        
        if not date_column:
            # Create synthetic dates spread over time
            end_date = datetime.now()
            num_reviews = len(df_work)
            if num_reviews == 0:
                print("⚠️  No reviews to process")
                return None
            
            # Spread reviews over last 90 days or based on review count
            days_span = max(30, min(90, num_reviews))
            start_date = end_date - timedelta(days=days_span)
            
            try:
                df_work['date_parsed'] = pd.date_range(start=start_date, end=end_date, periods=num_reviews)
            except:
                # Fallback: simple date range
                df_work['date_parsed'] = pd.date_range(start=start_date, periods=num_reviews, freq='D')
        
        # Calculate daily sentiment ratios (positive sentiment ratio per day)
        df_work['is_positive'] = (df_work['sentiment'] == 'positive').astype(int)
        df_work['date_only'] = pd.to_datetime(df_work['date_parsed']).dt.date
        
        daily_sentiment = df_work.groupby('date_only').agg({
            'is_positive': ['mean', 'count']
        }).reset_index()
        daily_sentiment.columns = ['date', 'sentiment_ratio', 'review_count']
        daily_sentiment = daily_sentiment.sort_values('date')
        
        if len(daily_sentiment) < 2:
            print("⚠️  Insufficient daily data for forecast generation")
            return None
        
        # Get sentiment values as time series
        sentiment_values = daily_sentiment['sentiment_ratio'].values
        sentiment_dates = pd.to_datetime(daily_sentiment['date'].values)
        
        # Current sentiment (average of last week or all if less)
        lookback = min(7, len(sentiment_values))
        current_sentiment = float(np.mean(sentiment_values[-lookback:])) if len(sentiment_values) >= lookback else float(np.mean(sentiment_values))
        
        # Generate forecast dates (next N days from last date)
        last_date = sentiment_dates[-1]
        forecast_dates_list = [(last_date + timedelta(days=i+1)).strftime('%Y-%m-%d %H:%M:%S') 
                              for i in range(forecast_days)]
        
        # 1. Moving Average Forecast (7-day window)
        window = min(7, len(sentiment_values))
        ma_value = float(np.mean(sentiment_values[-window:])) if window > 0 else current_sentiment
        ma_forecast = [ma_value] * forecast_days
        
        # 2. Linear Trend Forecast
        if len(sentiment_values) >= 2:
            x = np.arange(len(sentiment_values))
            coeffs = np.polyfit(x, sentiment_values, 1)
            trend_forecast = []
            for i in range(forecast_days):
                future_x = len(sentiment_values) + i
                trend_val = float(np.polyval(coeffs, future_x))
                trend_val = max(0.0, min(1.0, trend_val))  # Clamp between 0 and 1
                trend_forecast.append(trend_val)
        else:
            trend_forecast = [current_sentiment] * forecast_days
        
        # 3. ARIMA Forecast (simplified auto-regressive)
        arima_forecast = []
        if len(sentiment_values) >= 3:
            # Simple auto-regressive: average of last 3 values with trend
            last_3 = sentiment_values[-3:]
            arima_base = float(np.mean(last_3))
            # Calculate trend from last 3 values
            trend_diff = float((sentiment_values[-1] - sentiment_values[-3]) / 3) if len(sentiment_values) >= 3 else 0
            
            for i in range(forecast_days):
                arima_val = arima_base + (trend_diff * (i + 1))
                arima_val = max(0.0, min(1.0, arima_val))  # Clamp between 0 and 1
                arima_forecast.append(arima_val)
        else:
            arima_forecast = [current_sentiment] * forecast_days
        
        # Calculate forecast average
        forecast_avg = float(np.mean([ma_forecast[0], trend_forecast[0], arima_forecast[0]]))
        
        # Determine trend direction
        if len(sentiment_values) >= 7:
            recent_avg = float(np.mean(sentiment_values[-7:]))
            older_avg = float(np.mean(sentiment_values[-14:-7])) if len(sentiment_values) >= 14 else float(sentiment_values[0])
            if recent_avg > older_avg * 1.05:
                trend_direction = 'INCREASING'
            elif recent_avg < older_avg * 0.95:
                trend_direction = 'DECREASING'
            else:
                trend_direction = 'STABLE'
        else:
            trend_direction = 'STABLE'
        
        forecast_result = {
            'current_sentiment': current_sentiment,
            'forecast_avg': forecast_avg,
            'trend_direction': trend_direction,
            'forecast_dates': forecast_dates_list,
            'ma_forecast': ma_forecast,
            'trend_forecast': trend_forecast,
            'arima_forecast': arima_forecast
        }
        
        print(f"✅ Generated forecast on-the-fly: {len(forecast_dates_list)} days, trend: {trend_direction}")
        
        # Optionally save for future use
        try:
            forecast_path = os.path.join(backend_dir, 'data', 'models', 'forecast_results.json')
            os.makedirs(os.path.dirname(forecast_path), exist_ok=True)
            with open(forecast_path, 'w') as f:
                json.dump(forecast_result, f, indent=2)
            print(f"✅ Saved generated forecast to {forecast_path}")
        except Exception as e:
            print(f"⚠️  Could not save forecast to file: {e}")
        
        return forecast_result
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"⚠️  Error generating forecast from reviews: {e}")
        return None


@app.route('/api/forecast', methods=['GET'])
@token_required
def get_forecast():
    """Get forecast results with period filtering and data generation"""
    try:
        forecast_path = os.path.join(backend_dir, 'data', 'models', 'forecast_results.json')
        
        # Get period parameter (7, 30, months, years, overall)
        period = request.args.get('period', '7')  # default to 7 days
        
        # Determine how many forecast days to generate
        forecast_days = 7
        if period == '30':
            forecast_days = 30
        elif period in ['months', 'years', 'overall']:
            forecast_days = 365  # Generate enough for a year
        
        # Try to load existing forecast, otherwise generate from reviews
        forecast = None
        try:
            with open(forecast_path, 'r') as f:
                forecast = json.load(f)
                # Check if forecast has valid data
                if not forecast.get('forecast_dates') or len(forecast.get('forecast_dates', [])) < 7:
                    forecast = None
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            forecast = None
        
        # If no valid forecast file exists, generate from review data on-the-fly
        if forecast is None:
            print("📊 Forecast file not found. Generating forecast from review data on-the-fly...")
            print(f"   Review data status: {len(df_reviews)} reviews loaded")
            
            if df_reviews.empty:
                print("⚠️  No review data available. Cannot generate forecast.")
                return jsonify({
                    'error': 'Forecast data is not yet available.',
                    'message': 'The predictive analytics data is still being processed. Please check back shortly.',
                    'available': False
                }), 404
            
            try:
                # Generate forecast on-the-fly from review data
                print(f"   Generating forecast for {forecast_days} days...")
                forecast = generate_forecast_from_reviews(df_reviews, forecast_days)
                
                if forecast is None:
                    print("⚠️  Forecast generation returned None")
                    return jsonify({
                        'error': 'Forecast data is not yet available.',
                        'message': 'Unable to generate forecast at this time. Please check back shortly.',
                        'available': False
                    }), 404
                
                print(f"✅ Successfully generated forecast with {len(forecast.get('forecast_dates', []))} data points")
            except Exception as e:
                import traceback
                print(f"⚠️  Error generating forecast on-the-fly: {e}")
                traceback.print_exc()
                return jsonify({
                    'error': 'Forecast data is not yet available.',
                    'message': 'Unable to generate forecast at this time. Please check back shortly.',
                    'available': False
                }), 500
        
        # Parse dates - handle various formats
        def parse_date(d):
            if isinstance(d, datetime):
                return d
            if isinstance(d, str):
                # Try ISO format first
                try:
                    return datetime.fromisoformat(d.replace('Z', '+00:00'))
                except:
                    # Try other common formats
                    for fmt in ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S']:
                        try:
                            return datetime.strptime(d, fmt)
                        except:
                            continue
            return None
        
        if 'forecast_dates' not in forecast or not forecast['forecast_dates']:
            print("⚠️  Forecast data missing forecast_dates. Returning available data.")
            return jsonify(forecast)
        
        try:
            forecast_dates = [parse_date(d) for d in forecast['forecast_dates']]
            valid_dates = [(i, d) for i, d in enumerate(forecast_dates) if d is not None]
        except Exception as e:
            print(f"⚠️  Error parsing forecast dates: {e}")
            # Return original forecast if date parsing fails
            return jsonify(forecast)
        
        if not valid_dates:
            print("⚠️  No valid dates found in forecast. Returning available data.")
            return jsonify(forecast)
        
        # Process based on period
        try:
            if period == 'overall' or period == 'years':
                # Return all data - no filtering needed (but ensure we have enough points)
                if len(forecast.get('forecast_dates', [])) < 30:
                    forecast = extend_or_sample_forecast(forecast, valid_dates, 30, 'days')
            elif period == '7':
                # Get exactly 7 data points
                num_points = 7
                forecast = extend_or_sample_forecast(forecast, valid_dates, num_points, 'days')
            elif period == '30':
                # Generate exactly 30 data points
                num_points = 30
                forecast = extend_or_sample_forecast(forecast, valid_dates, num_points, 'days')
            elif period == 'months':
                # Aggregate into 12 monthly data points
                forecast = aggregate_to_monthly(forecast, valid_dates, 12)
            else:
                # Default: 7 days
                num_points = 7
                forecast = extend_or_sample_forecast(forecast, valid_dates, num_points, 'days')
            
            # Debug: Log the actual number of points returned
            final_points = len(forecast.get('forecast_dates', []))
            print(f"📊 Forecast returned with {final_points} data points for period '{period}'")
        except Exception as e:
            print(f"⚠️  Error processing forecast for period '{period}': {e}")
            import traceback
            traceback.print_exc()
            # Return original forecast if processing fails
            pass
        
        return jsonify(forecast)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error loading forecast: {e}")
        # Return user-friendly error message
        return jsonify({
            'error': 'Unable to load forecast data at this time.',
            'message': 'The system is temporarily unable to display predictive analytics. Please try again later.',
            'available': False
        }), 500

def extend_or_sample_forecast(forecast, valid_dates, num_points, interval='days'):
    """Extend forecast data to desired number of points or sample if too many"""
    if not valid_dates:
        print("⚠️  No valid dates provided to extend_or_sample_forecast")
        return forecast
    
    try:
        # Get original data arrays
        ma_forecast = forecast.get('ma_forecast', [])
        trend_forecast = forecast.get('trend_forecast', [])
        arima_forecast = forecast.get('arima_forecast', [])
        actual_sentiment = forecast.get('actual_sentiment', [])
        
        # Start from the first date
        start_date = valid_dates[0][1]
        original_length = len(ma_forecast) if ma_forecast else len(valid_dates)
        
        if original_length >= num_points:
            # Sample if we have too many points
            step = max(1, original_length // num_points)
            indices = list(range(0, original_length, step))[:num_points]
            return filter_forecast_by_indices(forecast, indices)
        
        # Extend if we need more points
        # Calculate trends from existing data (slope per day)
        def calculate_daily_trend(values):
            if len(values) < 2:
                return 0
            # Calculate average daily change
            total_change = values[-1] - values[0]
            return total_change / (len(values) - 1) if len(values) > 1 else 0
        
        ma_trend_per_day = calculate_daily_trend(ma_forecast) if ma_forecast else 0
        trend_trend_per_day = calculate_daily_trend(trend_forecast) if trend_forecast else 0
        arima_trend_per_day = calculate_daily_trend(arima_forecast) if arima_forecast else 0
        
        # Get last values to continue from
        last_date = valid_dates[-1][1] if valid_dates else start_date
        last_ma = ma_forecast[-1] if ma_forecast else 0.5
        last_trend_val = trend_forecast[-1] if trend_forecast else 0.5
        last_arima = arima_forecast[-1] if arima_forecast else 0.5
        
        # Copy original data
        result = forecast.copy()
        result['forecast_dates'] = [d[1].strftime('%Y-%m-%d %H:%M:%S') for i, d in valid_dates]
        result['ma_forecast'] = list(ma_forecast) if ma_forecast else []
        result['trend_forecast'] = list(trend_forecast) if trend_forecast else []
        result['arima_forecast'] = list(arima_forecast) if arima_forecast else []
        if actual_sentiment:
            result['actual_sentiment'] = list(actual_sentiment)
        
        # Extend forward to reach num_points
        current_length = len(result['forecast_dates'])
        points_needed = num_points - current_length
        
        if points_needed > 0:
            # Generate additional dates and values
            for day in range(1, points_needed + 1):
                new_date = last_date + timedelta(days=day)
                result['forecast_dates'].append(new_date.strftime('%Y-%m-%d %H:%M:%S'))
                
                # Extend values using daily trend
                new_ma = last_ma + (ma_trend_per_day * day)
                new_trend = last_trend_val + (trend_trend_per_day * day)
                new_arima = last_arima + (arima_trend_per_day * day)
                
                # Clamp values between 0 and 1
                result['ma_forecast'].append(max(0.0, min(1.0, float(new_ma))))
                result['trend_forecast'].append(max(0.0, min(1.0, float(new_trend))))
                result['arima_forecast'].append(max(0.0, min(1.0, float(new_arima))))
                
                if actual_sentiment:
                    result.setdefault('actual_sentiment', []).append(None)  # No actual data for future dates
        
        # Ensure we have exactly num_points (take first num_points if we somehow have more)
        if len(result['forecast_dates']) > num_points:
            result['forecast_dates'] = result['forecast_dates'][:num_points]
            result['ma_forecast'] = result['ma_forecast'][:num_points]
            result['trend_forecast'] = result['trend_forecast'][:num_points]
            result['arima_forecast'] = result['arima_forecast'][:num_points]
            if 'actual_sentiment' in result:
                result['actual_sentiment'] = result['actual_sentiment'][:num_points]
        
        return result
    except Exception as e:
        import traceback
        print(f"⚠️  Error in extend_or_sample_forecast: {e}")
        traceback.print_exc()
        # Return original forecast if extension fails
        return forecast

def aggregate_to_monthly(forecast, valid_dates, num_months=12):
    """Aggregate forecast data into monthly buckets"""
    if not valid_dates:
        return forecast
    
    from collections import defaultdict
    
    # Group data by month-year
    monthly_data = defaultdict(lambda: {
        'dates': [],
        'ma_values': [],
        'trend_values': [],
        'arima_values': [],
        'actual_values': []
    })
    
    ma_forecast = forecast.get('ma_forecast', [])
    trend_forecast = forecast.get('trend_forecast', [])
    arima_forecast = forecast.get('arima_forecast', [])
    actual_sentiment = forecast.get('actual_sentiment', [])
    
    for idx, (orig_idx, date) in enumerate(valid_dates):
        month_key = f"{date.year}-{date.month:02d}"
        monthly_data[month_key]['dates'].append(date)
        if idx < len(ma_forecast):
            monthly_data[month_key]['ma_values'].append(ma_forecast[idx])
        if idx < len(trend_forecast):
            monthly_data[month_key]['trend_values'].append(trend_forecast[idx])
        if idx < len(arima_forecast):
            monthly_data[month_key]['arima_values'].append(arima_forecast[idx])
        if idx < len(actual_sentiment) and actual_sentiment[idx] is not None:
            monthly_data[month_key]['actual_values'].append(actual_sentiment[idx])
    
    # Sort months and take last N months
    sorted_months = sorted(monthly_data.keys())[-num_months:]
    
    # Aggregate (average) values per month
    aggregated_dates = []
    aggregated_ma = []
    aggregated_trend = []
    aggregated_arima = []
    aggregated_actual = []
    
    for month_key in sorted_months:
        month_data = monthly_data[month_key]
        if month_data['dates']:
            # Use first date of month as representative date
            rep_date = month_data['dates'][0].replace(day=1)
            aggregated_dates.append(rep_date.strftime('%Y-%m-%d %H:%M:%S'))
            
            # Average the values
            if month_data['ma_values']:
                aggregated_ma.append(sum(month_data['ma_values']) / len(month_data['ma_values']))
            else:
                aggregated_ma.append(0.5)
            
            if month_data['trend_values']:
                aggregated_trend.append(sum(month_data['trend_values']) / len(month_data['trend_values']))
            else:
                aggregated_trend.append(0.5)
            
            if month_data['arima_values']:
                aggregated_arima.append(sum(month_data['arima_values']) / len(month_data['arima_values']))
            else:
                aggregated_arima.append(0.5)
            
            if month_data['actual_values']:
                aggregated_actual.append(sum(month_data['actual_values']) / len(month_data['actual_values']))
            else:
                aggregated_actual.append(None)
    
    result = forecast.copy()
    result['forecast_dates'] = aggregated_dates
    result['ma_forecast'] = aggregated_ma
    result['trend_forecast'] = aggregated_trend
    result['arima_forecast'] = aggregated_arima
    if actual_sentiment:
        result['actual_sentiment'] = aggregated_actual
    
    return result

def filter_forecast_by_indices(forecast, indices):
    """Helper function to filter forecast data by indices"""
    filtered = forecast.copy()
    if 'forecast_dates' in forecast:
        filtered['forecast_dates'] = [forecast['forecast_dates'][i] for i in indices]
    if 'ma_forecast' in forecast:
        filtered['ma_forecast'] = [forecast['ma_forecast'][i] for i in indices]
    if 'trend_forecast' in forecast:
        filtered['trend_forecast'] = [forecast['trend_forecast'][i] for i in indices]
    if 'arima_forecast' in forecast:
        filtered['arima_forecast'] = [forecast['arima_forecast'][i] for i in indices]
    if 'actual_sentiment' in forecast:
        filtered['actual_sentiment'] = [forecast['actual_sentiment'][i] for i in indices]
    return filtered


@app.route('/api/dashboard/stats', methods=['GET'])
@token_required
def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        if df_reviews.empty:
            return jsonify({
                'total_reviews': 0,
                'positive_ratio': 0,
                'negative_ratio': 0,
                'topic_count': 0
            })
        
        stats = {
            'total_reviews': len(df_reviews),
            'positive_ratio': (df_reviews['sentiment'] == 'positive').sum() / len(df_reviews) if 'sentiment' in df_reviews.columns else 0,
            'negative_ratio': (df_reviews['sentiment'] == 'negative').sum() / len(df_reviews) if 'sentiment' in df_reviews.columns else 0,
            'topic_count': df_reviews['topic'].nunique() if 'topic' in df_reviews.columns else 0
        }
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analytics/location-sentiment', methods=['GET'])
@token_required
def get_location_sentiment():
    """Get sentiment analysis by location with filters and percentage distribution"""
    try:
        sentiment_filter = request.args.get('sentiment', 'all')  # all, positive, negative, neutral
        
        if df_reviews.empty or 'location' not in df_reviews.columns or 'sentiment' not in df_reviews.columns:
            return jsonify({'locations': [], 'summary': {}})
        
        # Calculate total counts for percentage distribution
        total_positive = (df_reviews['sentiment'] == 'positive').sum()
        total_negative = (df_reviews['sentiment'] == 'negative').sum()
        total_neutral = (df_reviews['sentiment'] == 'neutral').sum()
        total_all = len(df_reviews)
        
        # Filter by sentiment if specified
        df_filtered = df_reviews.copy()
        if sentiment_filter != 'all':
            df_filtered = df_filtered[df_filtered['sentiment'] == sentiment_filter]
        
        # Group by location
        location_stats = df_filtered.groupby('location').agg({
            'sentiment': ['count', lambda x: (x == 'positive').sum(), 
                         lambda x: (x == 'negative').sum(), 
                         lambda x: (x == 'neutral').sum()]
        }).reset_index()
        
        location_stats.columns = ['location', 'total', 'positive', 'negative', 'neutral']
        
        # Calculate percentages within location
        location_stats['positive_pct'] = (location_stats['positive'] / location_stats['total'] * 100).round(1)
        location_stats['negative_pct'] = (location_stats['negative'] / location_stats['total'] * 100).round(1)
        location_stats['neutral_pct'] = (location_stats['neutral'] / location_stats['total'] * 100).round(1)
        
        # Calculate percentage distribution (what % of all positive/negative/neutral come from each location)
        if total_positive > 0:
            location_stats['pct_of_all_positive'] = (location_stats['positive'] / total_positive * 100).round(1)
        else:
            location_stats['pct_of_all_positive'] = 0.0
        
        if total_negative > 0:
            location_stats['pct_of_all_negative'] = (location_stats['negative'] / total_negative * 100).round(1)
        else:
            location_stats['pct_of_all_negative'] = 0.0
        
        if total_neutral > 0:
            location_stats['pct_of_all_neutral'] = (location_stats['neutral'] / total_neutral * 100).round(1)
        else:
            location_stats['pct_of_all_neutral'] = 0.0
        
        location_stats['pct_of_all_reviews'] = (location_stats['total'] / total_all * 100).round(1)
        
        # Sort by total
        location_stats = location_stats.sort_values('total', ascending=False)
        
        # Summary stats
        summary = {
            'total_locations': len(location_stats),
            'total_reviews': int(location_stats['total'].sum()),
            'filter_applied': sentiment_filter,
            'total_positive': int(total_positive),
            'total_negative': int(total_negative),
            'total_neutral': int(total_neutral),
        }
        
        return jsonify({
            'locations': location_stats.to_dict('records'),
            'summary': summary
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analytics/platform-sentiment', methods=['GET'])
@token_required
def get_platform_sentiment():
    """Get sentiment analysis by platform (source) with filters and percentage distribution"""
    try:
        sentiment_filter = request.args.get('sentiment', 'all')
        
        if df_reviews.empty or 'source' not in df_reviews.columns or 'sentiment' not in df_reviews.columns:
            return jsonify({'platforms': [], 'summary': {}})
        
        # Calculate total counts for percentage distribution
        total_positive = (df_reviews['sentiment'] == 'positive').sum()
        total_negative = (df_reviews['sentiment'] == 'negative').sum()
        total_neutral = (df_reviews['sentiment'] == 'neutral').sum()
        total_all = len(df_reviews)
        
        # Filter by sentiment if specified
        df_filtered = df_reviews.copy()
        if sentiment_filter != 'all':
            df_filtered = df_filtered[df_filtered['sentiment'] == sentiment_filter]
        
        # Group by source (platform)
        platform_stats = df_filtered.groupby('source').agg({
            'sentiment': ['count', lambda x: (x == 'positive').sum(), 
                         lambda x: (x == 'negative').sum(), 
                         lambda x: (x == 'neutral').sum()]
        }).reset_index()
        
        platform_stats.columns = ['platform', 'total', 'positive', 'negative', 'neutral']
        
        # Calculate percentages within platform
        platform_stats['positive_pct'] = (platform_stats['positive'] / platform_stats['total'] * 100).round(1)
        platform_stats['negative_pct'] = (platform_stats['negative'] / platform_stats['total'] * 100).round(1)
        platform_stats['neutral_pct'] = (platform_stats['neutral'] / platform_stats['total'] * 100).round(1)
        
        # Calculate percentage distribution (what % of all positive/negative/neutral come from each platform)
        if total_positive > 0:
            platform_stats['pct_of_all_positive'] = (platform_stats['positive'] / total_positive * 100).round(1)
        else:
            platform_stats['pct_of_all_positive'] = 0.0
        
        if total_negative > 0:
            platform_stats['pct_of_all_negative'] = (platform_stats['negative'] / total_negative * 100).round(1)
        else:
            platform_stats['pct_of_all_negative'] = 0.0
        
        if total_neutral > 0:
            platform_stats['pct_of_all_neutral'] = (platform_stats['neutral'] / total_neutral * 100).round(1)
        else:
            platform_stats['pct_of_all_neutral'] = 0.0
        
        platform_stats['pct_of_all_reviews'] = (platform_stats['total'] / total_all * 100).round(1)
        
        # Sort by total
        platform_stats = platform_stats.sort_values('total', ascending=False)
        
        summary = {
            'total_platforms': len(platform_stats),
            'total_reviews': int(platform_stats['total'].sum()),
            'filter_applied': sentiment_filter,
            'total_positive': int(total_positive),
            'total_negative': int(total_negative),
            'total_neutral': int(total_neutral),
        }
        
        return jsonify({
            'platforms': platform_stats.to_dict('records'),
            'summary': summary
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analytics/topic-sentiment', methods=['GET'])
@token_required
def get_topic_sentiment():
    """Get sentiment analysis by topic with filters and percentage distribution"""
    try:
        sentiment_filter = request.args.get('sentiment', 'all')
        
        if df_reviews.empty or 'topic' not in df_reviews.columns or 'sentiment' not in df_reviews.columns:
            return jsonify({'topics': [], 'summary': {}})
        
        # Calculate total counts for percentage distribution
        total_positive = (df_reviews['sentiment'] == 'positive').sum()
        total_negative = (df_reviews['sentiment'] == 'negative').sum()
        total_neutral = (df_reviews['sentiment'] == 'neutral').sum()
        total_all = len(df_reviews)
        
        # Load topic names if available
        topic_names = {}
        try:
            from gensim.models import LdaModel
            lda_path = os.path.join(backend_dir, 'data', 'models', 'lda_model')
            lda_model = LdaModel.load(lda_path)
            for topic_id in range(5):
                topic_words = lda_model.show_topic(topic_id, topn=10)
                topic_names[topic_id] = generate_topic_name(topic_words)
        except:
            # Default names if LDA model not available
            topic_names = {i: f"Topic {i}" for i in range(5)}
        
        # Filter by sentiment if specified
        df_filtered = df_reviews.copy()
        if sentiment_filter != 'all':
            df_filtered = df_filtered[df_filtered['sentiment'] == sentiment_filter]
        
        # Group by topic
        topic_stats = df_filtered.groupby('topic').agg({
            'sentiment': ['count', lambda x: (x == 'positive').sum(), 
                         lambda x: (x == 'negative').sum(), 
                         lambda x: (x == 'neutral').sum()]
        }).reset_index()
        
        topic_stats.columns = ['topic', 'total', 'positive', 'negative', 'neutral']
        
        # Add topic names
        topic_stats['topic_name'] = topic_stats['topic'].map(lambda x: topic_names.get(x, f"Topic {x}"))
        
        # Calculate percentages within topic
        topic_stats['positive_pct'] = (topic_stats['positive'] / topic_stats['total'] * 100).round(1)
        topic_stats['negative_pct'] = (topic_stats['negative'] / topic_stats['total'] * 100).round(1)
        topic_stats['neutral_pct'] = (topic_stats['neutral'] / topic_stats['total'] * 100).round(1)
        
        # Calculate percentage distribution (what % of all positive/negative/neutral come from each topic)
        if total_positive > 0:
            topic_stats['pct_of_all_positive'] = (topic_stats['positive'] / total_positive * 100).round(1)
        else:
            topic_stats['pct_of_all_positive'] = 0.0
        
        if total_negative > 0:
            topic_stats['pct_of_all_negative'] = (topic_stats['negative'] / total_negative * 100).round(1)
        else:
            topic_stats['pct_of_all_negative'] = 0.0
        
        if total_neutral > 0:
            topic_stats['pct_of_all_neutral'] = (topic_stats['neutral'] / total_neutral * 100).round(1)
        else:
            topic_stats['pct_of_all_neutral'] = 0.0
        
        topic_stats['pct_of_all_reviews'] = (topic_stats['total'] / total_all * 100).round(1)
        
        # Sort by total
        topic_stats = topic_stats.sort_values('total', ascending=False)
        
        summary = {
            'total_topics': len(topic_stats),
            'total_reviews': int(topic_stats['total'].sum()),
            'filter_applied': sentiment_filter,
            'total_positive': int(total_positive),
            'total_negative': int(total_negative),
            'total_neutral': int(total_neutral),
        }
        
        return jsonify({
            'topics': topic_stats.to_dict('records'),
            'summary': summary
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/feedback', methods=['POST'])
def collect_feedback():
    """Collect user feedback for learning"""
    try:
        data = request.json
        query_id = data.get('query_id')
        feedback = data.get('feedback', {})
        
        agent.collect_feedback(query_id, feedback)
        
        return jsonify({'status': 'success', 'message': 'Feedback collected'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/learning/stats', methods=['GET'])
def get_learning_stats():
    """Get learning statistics"""
    try:
        stats = agent.get_learning_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def send_email(to_email, subject, body, attachment_data=None, attachment_name=None):
    """Send email using SMTP"""
    try:
        # Email configuration (using Gmail SMTP as example)
        # In production, use environment variables for credentials
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "ensubuga019@gmail.com"  # Admin email
        sender_password = os.getenv("EMAIL_PASSWORD", "")  # Set this in environment
        
        # If no password set, just log (for development)
        if not sender_password:
            print(f"[EMAIL] Would send to {to_email}: {subject}")
            print(f"[EMAIL] Body: {body[:200]}...")
            return True
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))
        
        # Add attachment if provided
        if attachment_data and attachment_name:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment_data)
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename= {attachment_name}')
            msg.attach(part)
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


@app.route('/api/contact-admin', methods=['POST'])
@token_required
def contact_admin():
    """Send email to admin from user"""
    try:
        data = request.json
        user_email = data.get('email', 'Unknown')
        subject = data.get('subject', 'Contact from User')
        message = data.get('message', '')
        user_name = data.get('name', 'User')
        
        admin_email = "ensubuga019@gmail.com"
        
        body = f"""
        <html>
        <body>
            <h2>Contact Request from Business Intelligence Platform</h2>
            <p><strong>From:</strong> {user_name} ({user_email})</p>
            <p><strong>Subject:</strong> {subject}</p>
            <hr>
            <p><strong>Message:</strong></p>
            <p>{message}</p>
            <hr>
            <p><small>Sent from Business Intelligence Analyst Platform</small></p>
        </body>
        </html>
        """
        
        send_email(admin_email, f"Contact: {subject}", body)
        
        return jsonify({'status': 'success', 'message': 'Email sent to admin'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/report', methods=['POST'])
@token_required
def export_report():
    """Export analytics report and send to admin"""
    try:
        data = request.json
        report_type = data.get('type', 'dashboard')  # dashboard, location, platform, topic
        
        # Generate report data
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'type': report_type,
            'summary': {}
        }
        
        # Get all analytics data
        try:
            # Location data
            location_response = get_location_sentiment()
            if hasattr(location_response, 'get_json'):
                location_data = location_response.get_json()
                report_data['location_analytics'] = location_data
            
            # Platform data
            platform_response = get_platform_sentiment()
            if hasattr(platform_response, 'get_json'):
                platform_data = platform_response.get_json()
                report_data['platform_analytics'] = platform_data
            
            # Topic data
            topic_response = get_topic_sentiment()
            if hasattr(topic_response, 'get_json'):
                topic_data = topic_response.get_json()
                report_data['topic_analytics'] = topic_data
            
            # Dashboard stats
            stats_response = get_dashboard_stats()
            if hasattr(stats_response, 'get_json'):
                stats_data = stats_response.get_json()
                report_data['dashboard_stats'] = stats_data
        except Exception as e:
            print(f"Error gathering report data: {e}")
        
        # Generate PDF Report
        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#5624d0'),
            spaceAfter=30,
            alignment=1  # Center
        )
        story.append(Paragraph("CENAnalytics Business Intelligence Report", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Report Info
        info_style = ParagraphStyle(
            'InfoStyle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.grey
        )
        story.append(Paragraph(f"<b>Report Type:</b> {report_type.title()}", styles['Normal']))
        story.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Dashboard Statistics
        if 'dashboard_stats' in report_data:
            story.append(Paragraph("<b>Dashboard Statistics</b>", styles['Heading2']))
            stats = report_data['dashboard_stats']
            stats_data = [
                ['Metric', 'Value'],
                ['Total Reviews', f"{stats.get('total_reviews', 0):,}"],
                ['Positive Sentiment', f"{stats.get('positive_pct', 0):.1f}%"],
                ['Negative Sentiment', f"{stats.get('negative_pct', 0):.1f}%"],
                ['Neutral Sentiment', f"{stats.get('neutral_pct', 0):.1f}%"],
            ]
            stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#5624d0')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]))
            story.append(stats_table)
            story.append(Spacer(1, 0.3*inch))
        
        # Location Analytics
        if 'location_analytics' in report_data and report_data['location_analytics'].get('locations'):
            story.append(Paragraph("<b>Location-Based Sentiment Analysis</b>", styles['Heading2']))
            loc_data = [['Location', 'Total', 'Positive %', 'Negative %', 'Neutral %']]
            for loc in report_data['location_analytics'].get('locations', [])[:10]:
                loc_data.append([
                    loc.get('location', 'N/A'),
                    str(loc.get('total', 0)),
                    f"{loc.get('positive_pct', 0):.1f}%",
                    f"{loc.get('negative_pct', 0):.1f}%",
                    f"{loc.get('neutral_pct', 0):.1f}%"
                ])
            loc_table = Table(loc_data, colWidths=[1.5*inch, 1*inch, 1*inch, 1*inch, 1*inch])
            loc_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#5624d0')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]))
            story.append(loc_table)
            story.append(Spacer(1, 0.3*inch))
        
        # Platform Analytics
        if 'platform_analytics' in report_data and report_data['platform_analytics'].get('platforms'):
            story.append(Paragraph("<b>Platform-Based Sentiment Analysis</b>", styles['Heading2']))
            plat_data = [['Platform', 'Total', 'Positive %', 'Negative %', 'Neutral %']]
            for plat in report_data['platform_analytics'].get('platforms', []):
                plat_data.append([
                    plat.get('platform', 'N/A'),
                    str(plat.get('total', 0)),
                    f"{plat.get('positive_pct', 0):.1f}%",
                    f"{plat.get('negative_pct', 0):.1f}%",
                    f"{plat.get('neutral_pct', 0):.1f}%"
                ])
            plat_table = Table(plat_data, colWidths=[1.5*inch, 1*inch, 1*inch, 1*inch, 1*inch])
            plat_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#5624d0')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]))
            story.append(plat_table)
            story.append(Spacer(1, 0.3*inch))
        
        # Topic Analytics
        if 'topic_analytics' in report_data and report_data['topic_analytics'].get('topics'):
            story.append(Paragraph("<b>Topic-Based Sentiment Analysis</b>", styles['Heading2']))
            topic_data = [['Topic', 'Total', 'Positive %', 'Negative %', 'Neutral %']]
            for topic in report_data['topic_analytics'].get('topics', []):
                topic_data.append([
                    topic.get('topic_name', 'N/A')[:30],  # Truncate long names
                    str(topic.get('total', 0)),
                    f"{topic.get('positive_pct', 0):.1f}%",
                    f"{topic.get('negative_pct', 0):.1f}%",
                    f"{topic.get('neutral_pct', 0):.1f}%"
                ])
            topic_table = Table(topic_data, colWidths=[2*inch, 1*inch, 1*inch, 1*inch, 1*inch])
            topic_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#5624d0')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]))
            story.append(topic_table)
            story.append(Spacer(1, 0.3*inch))
        
        # Footer
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph("<i>Generated by CENAnalytics Business Intelligence Platform</i>", info_style))
        
        # Build PDF
        doc.build(story)
        pdf_bytes = pdf_buffer.getvalue()
        pdf_buffer.close()
        
        # Send email to admin with PDF attachment
        admin_email = "ensubuga019@gmail.com"
        email_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2 style="color: #5624d0;">CENAnalytics Report Export</h2>
            <p>A user has exported an analytics report from CENAnalytics Platform.</p>
            <p><strong>Report Type:</strong> {report_type}</p>
            <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <hr>
            <p>The complete analytics report is attached as a PDF file.</p>
            <p><small>This is an automated message from CENAnalytics Platform.</small></p>
        </body>
        </html>
        """
        
        pdf_filename = f"CENAnalytics_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        email_sent = send_email(admin_email, "CENAnalytics Report Export", email_body, pdf_bytes, pdf_filename)
        
        # Get user info from token
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user_info = {}
        try:
            from auth import verify_token
            decoded = verify_token(token)
            user_info = decoded if decoded else {}
        except:
            pass
        
        # Create notifications
        notification_id = len(notifications_storage) + 1
        
        # Notification 1: Report generated
        notifications_storage.append({
            'id': notification_id,
            'type': 'success',
            'title': 'Report Generated',
            'message': f'Your analytics report has been generated successfully.',
            'timestamp': datetime.now().isoformat(),
            'read': False,
            'user_email': user_info.get('email', 'unknown')
        })
        
        # Notification 2: Report sent to admin
        if email_sent:
            notifications_storage.append({
                'id': notification_id + 1,
                'type': 'info',
                'title': 'Report Sent to Admin',
                'message': f'A copy of your report has been sent to ensubuga019@gmail.com',
                'timestamp': datetime.now().isoformat(),
                'read': False,
                'user_email': user_info.get('email', 'unknown')
            })
        
        # Return PDF to frontend for download
        pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
        
        return jsonify({
            'status': 'success',
            'message': 'Report exported and sent to admin',
            'report': report_data,
            'pdf': pdf_base64,
            'filename': pdf_filename,
            'notifications_created': notification_id + (1 if email_sent else 0)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/notifications', methods=['GET'])
@token_required
def get_notifications():
    """Get user notifications"""
    try:
        # Get user info from token
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user_info = {}
        try:
            from auth import verify_token, find_user_by_email
            decoded = verify_token(token)
            if decoded:
                user_info = decoded
                # Get full user data to extract surname
                user_email = decoded.get('sub') or decoded.get('email', 'unknown')
                full_user = find_user_by_email(user_email)
                if full_user:
                    from auth import extract_surname
                    user_info['surname'] = extract_surname(full_user.get('name', ''))
        except:
            pass
        
        user_email = user_info.get('sub') or user_info.get('email', 'unknown')
        
        # Get notifications for this user (or all if admin)
        user_notifications = [
            n for n in notifications_storage 
            if n.get('user_email') == user_email or user_info.get('role') == 'admin'
        ]
        
        # Sort by timestamp (newest first)
        user_notifications.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        # If no notifications, create welcome notification with user surname
        if not user_notifications:
            user_surname = user_info.get('surname', 'User')
            welcome_notification = {
                'id': len(notifications_storage) + 1,
                'type': 'info',
                'title': f'Welcome to CENAnalytics, {user_surname}!',
                'message': f'Your analytics dashboard is ready, {user_surname}. Start exploring your data insights and discover valuable business intelligence.',
                'timestamp': datetime.now().isoformat(),
                'read': False,
                'user_email': user_email
            }
            notifications_storage.append(welcome_notification)
            user_notifications = [welcome_notification]
        
        return jsonify({'notifications': user_notifications})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/notifications/mark-read', methods=['POST'])
@token_required
def mark_notification_read():
    """Mark a notification as read"""
    try:
        data = request.get_json() or {}
        notification_id = data.get('id')
        
        if not notification_id:
            return jsonify({'error': 'Notification ID required'}), 400
        
        # Get user info from token
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user_info = {}
        try:
            from auth import verify_token
            decoded = verify_token(token)
            user_info = decoded if decoded else {}
        except:
            pass
        
        user_email = user_info.get('sub') or user_info.get('email', 'unknown')
        
        # Find and update notification
        notification_found = False
        for notification in notifications_storage:
            if notification.get('id') == notification_id:
                # Check if user owns this notification or is admin
                if notification.get('user_email') == user_email or user_info.get('role') == 'admin':
                    notification['read'] = True
                    notification_found = True
                    break
        
        if notification_found:
            return jsonify({'status': 'success', 'message': 'Notification marked as read'})
        else:
            return jsonify({'error': 'Notification not found or unauthorized'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("Starting Business Intelligence Analyst API...")
    print("API will be available at http://localhost:5000")
    print("\n" + "=" * 60)
    print("Sample Users Created:")
    print("=" * 60)
    print("Admin Account:")
    print("  Email: admin@business.com")
    print("  Password: admin123")
    print("\nUser Accounts (7 users):")
    users = get_all_users()
    for i, user in enumerate(users[1:], 1):
        print(f"  User {i}: {user['email']} / user123")
    print("=" * 60 + "\n")
    app.run(debug=True, port=5000)


