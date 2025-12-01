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
from datetime import timedelta

# Add backend directory to path (src is now inside backend)
current_file = os.path.abspath(__file__)  # Full path to backend_api.py
backend_dir = os.path.dirname(current_file)  # backend
sys.path.insert(0, backend_dir)  # Add backend to path so we can import from src

# Now we can import from src
from src.models.sentiment_analyzer import SentimentAnalyzer
from src.utils.text_preprocessor import TextPreprocessor
from src.models.cognitive_agent import BusinessIntelligenceAgent
from backend.auth import (
    authenticate_user,
    create_access_token,
    verify_token,
    get_all_users,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
import pickle
import networkx as nx

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

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


@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.json
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        user = authenticate_user(email, password)
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={'sub': user['email'], 'user_id': user['id'], 'role': user['role']},
            expires_delta=access_token_expires
        )
        
        return jsonify({
            'token': access_token,
            'user': {
                'id': user['id'],
                'email': user['email'],
                'name': user['name'],
                'role': user['role'],
            },
            'message': 'Login successful'
        })
    except Exception as e:
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
        
        return jsonify(result)
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


@app.route('/api/topics', methods=['GET'])
@token_required
def get_topics():
    """Get topics from LDA model"""
    try:
        # Load LDA model if available
        try:
            from gensim.models import LdaModel
            lda_path = os.path.join(backend_dir, 'data', 'models', 'lda_model')
            lda_model = LdaModel.load(lda_path)
            
            topics = []
            for topic_id in range(5):
                topic_words = lda_model.show_topic(topic_id, topn=10)
                topics.append({
                    'topic_id': topic_id,
                    'topic_words': [{'word': word, 'weight': weight} for word, weight in topic_words],
                    'review_count': len(df_reviews[df_reviews.get('topic', -1) == topic_id]) if 'topic' in df_reviews.columns else 0
                })
            
            return jsonify(topics)
        except:
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


