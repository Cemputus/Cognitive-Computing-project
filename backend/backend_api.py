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

# Load data
try:
    reviews_path = os.path.join(backend_dir, 'data', 'processed', 'reviews_with_sentiment.csv')
    df_reviews = pd.read_csv(reviews_path)
except:
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
        result = analyzer.analyze(text)
        
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


def generate_topic_name(topic_words):
    """Generate a meaningful name for a topic based on top words"""
    if not topic_words:
        return "General Discussion"
    
    # Get top 3 words
    top_words = [word for word, _ in topic_words[:3]]
    
    # Common topic name mappings
    topic_mappings = {
        ('service', 'delivery', 'customer'): 'Customer Service & Delivery',
        ('product', 'quality', 'price'): 'Product Quality & Pricing',
        ('business', 'shop', 'store'): 'Business Operations',
        ('location', 'kampala', 'area'): 'Location & Area',
        ('experience', 'great', 'good'): 'Customer Experience',
        ('fast', 'quick', 'time'): 'Speed & Efficiency',
        ('staff', 'support', 'help'): 'Staff & Support',
        ('price', 'cost', 'affordable'): 'Pricing & Value',
    }
    
    # Try to match with known patterns
    words_lower = [w.lower() for w in top_words]
    for pattern, name in topic_mappings.items():
        if any(p in words_lower for p in pattern):
            return name
    
    # Generate name from top words
    return ' '.join([w.capitalize() for w in top_words[:2]]) + ' Discussion'


@app.route('/api/topics', methods=['GET'])
@token_required
def get_topics():
    """Get topics from LDA model with meaningful names"""
    try:
        # Load LDA model if available
        try:
            from gensim.models import LdaModel
            lda_path = os.path.join(backend_dir, 'data', 'models', 'lda_model')
            lda_model = LdaModel.load(lda_path)
            
            topics = []
            for topic_id in range(5):
                topic_words = lda_model.show_topic(topic_id, topn=10)
                topic_words_list = [(word, weight) for word, weight in topic_words]
                topic_name = generate_topic_name(topic_words_list)
                
                topics.append({
                    'topic_id': topic_id,
                    'topic_name': topic_name,
                    'topic_words': [{'word': word, 'weight': weight} for word, weight in topic_words_list],
                    'review_count': len(df_reviews[df_reviews.get('topic', -1) == topic_id]) if 'topic' in df_reviews.columns else 0
                })
            
            return jsonify(topics)
        except Exception as e:
            print(f"Error loading topics: {e}")
            return jsonify([])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/forecast', methods=['GET'])
@token_required
def get_forecast():
    """Get forecast results"""
    try:
        forecast_path = os.path.join(backend_dir, 'data', 'models', 'forecast_results.json')
        with open(forecast_path, 'r') as f:
            forecast = json.load(f)
        return jsonify(forecast)
    except FileNotFoundError:
        return jsonify({'error': 'Forecast not available. Run Milestone 2 notebook first.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


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
        
        # Create CSV report
        csv_data = []
        csv_data.append("Business Intelligence Analytics Report")
        csv_data.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        csv_data.append("")
        
        if 'dashboard_stats' in report_data:
            csv_data.append("=== Dashboard Statistics ===")
            stats = report_data['dashboard_stats']
            csv_data.append(f"Total Reviews: {stats.get('total_reviews', 0)}")
            csv_data.append(f"Positive: {stats.get('positive_pct', 0)}%")
            csv_data.append(f"Negative: {stats.get('negative_pct', 0)}%")
            csv_data.append(f"Neutral: {stats.get('neutral_pct', 0)}%")
            csv_data.append("")
        
        if 'location_analytics' in report_data:
            csv_data.append("=== Location Analytics ===")
            csv_data.append("Location,Total,Positive %,Negative %,Neutral %")
            for loc in report_data['location_analytics'].get('locations', [])[:10]:
                csv_data.append(f"{loc.get('location', '')},{loc.get('total', 0)},{loc.get('positive_pct', 0)},{loc.get('negative_pct', 0)},{loc.get('neutral_pct', 0)}")
            csv_data.append("")
        
        if 'platform_analytics' in report_data:
            csv_data.append("=== Platform Analytics ===")
            csv_data.append("Platform,Total,Positive %,Negative %,Neutral %")
            for plat in report_data['platform_analytics'].get('platforms', []):
                csv_data.append(f"{plat.get('platform', '')},{plat.get('total', 0)},{plat.get('positive_pct', 0)},{plat.get('negative_pct', 0)},{plat.get('neutral_pct', 0)}")
            csv_data.append("")
        
        csv_content = "\n".join(csv_data)
        csv_bytes = csv_content.encode('utf-8')
        
        # Send email to admin with report
        admin_email = "ensubuga019@gmail.com"
        email_body = f"""
        <html>
        <body>
            <h2>CENAnalytics Report Export</h2>
            <p>A user has exported an analytics report from CENAnalytics Platform.</p>
            <p><strong>Report Type:</strong> {report_type}</p>
            <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <hr>
            <h3>Report Summary</h3>
            <pre>{csv_content[:2000]}</pre>
            <p><small>Full report attached as CSV file.</small></p>
        </body>
        </html>
        """
        
        filename = f"analytics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        email_sent = send_email(admin_email, "CENAnalytics Report Export", email_body, csv_bytes, filename)
        
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
        
        # Return report data to frontend
        return jsonify({
            'status': 'success',
            'message': 'Report exported and sent to admin',
            'report': report_data,
            'csv': csv_content,
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


