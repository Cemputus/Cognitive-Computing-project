"""
Quick script to test backend initialization and check for common issues
"""
import sys
import os

# Add backend to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

print("=" * 60)
print("Backend Health Check")
print("=" * 60)
print()

# Check 1: Python version
print("1. Python Version:")
print(f"   {sys.version}")
print()

# Check 2: Virtual environment
print("2. Virtual Environment:")
venv = os.environ.get('VIRTUAL_ENV', None)
if venv:
    print(f"   ✅ Active: {venv}")
else:
    print("   ⚠️  No virtual environment detected")
print()

# Check 3: Critical imports
print("3. Testing Imports:")
try:
    from flask import Flask
    print("   ✅ Flask")
except ImportError as e:
    print(f"   ❌ Flask: {e}")

try:
    from flask_cors import CORS
    print("   ✅ Flask-CORS")
except ImportError as e:
    print(f"   ❌ Flask-CORS: {e}")

try:
    import pandas as pd
    print("   ✅ Pandas")
except ImportError as e:
    print(f"   ❌ Pandas: {e}")

try:
    import numpy as np
    print("   ✅ NumPy")
except ImportError as e:
    print(f"   ❌ NumPy: {e}")

try:
    from src.models.sentiment_analyzer import SentimentAnalyzer
    print("   ✅ SentimentAnalyzer")
except ImportError as e:
    print(f"   ❌ SentimentAnalyzer: {e}")

try:
    from src.utils.text_preprocessor import TextPreprocessor
    print("   ✅ TextPreprocessor")
except ImportError as e:
    print(f"   ❌ TextPreprocessor: {e}")

try:
    from auth import authenticate_user
    print("   ✅ auth module")
except ImportError as e:
    print(f"   ❌ auth module: {e}")
print()

# Check 4: File paths
print("4. Checking File Paths:")
paths_to_check = [
    ('data/processed/cleaned_reviews.csv', 'Review data (Milestone 1)'),
    ('data/processed/reviews_with_sentiment.csv', 'Review data (Milestone 2)'),
    ('data/models/lda_model', 'LDA model'),
    ('data/models/forecast_results.json', 'Forecast results'),
    ('auth.py', 'Authentication module'),
]

for path, description in paths_to_check:
    full_path = os.path.join(backend_dir, path)
    if os.path.exists(full_path):
        print(f"   ✅ {description}: {path}")
    else:
        print(f"   ⚠️  {description}: {path} (not found)")
print()

# Check 5: Data loading
print("5. Testing Data Loading:")
try:
    reviews_path = os.path.join(backend_dir, 'data', 'processed', 'reviews_with_sentiment.csv')
    if os.path.exists(reviews_path):
        df = pd.read_csv(reviews_path)
        print(f"   ✅ Loaded {len(df)} reviews from reviews_with_sentiment.csv")
        if 'sentiment' in df.columns:
            print("   ✅ Sentiment column found")
        else:
            print("   ⚠️  No sentiment column (will analyze on-the-fly)")
    else:
        cleaned_path = os.path.join(backend_dir, 'data', 'processed', 'cleaned_reviews.csv')
        if os.path.exists(cleaned_path):
            df = pd.read_csv(cleaned_path)
            print(f"   ⚠️  Loaded {len(df)} reviews from cleaned_reviews.csv (no sentiment)")
        else:
            print("   ❌ No review data found")
except Exception as e:
    print(f"   ❌ Error loading data: {e}")
print()

# Check 6: Flask app creation
print("6. Testing Flask App Creation:")
try:
    app = Flask(__name__)
    print("   ✅ Flask app can be created")
except Exception as e:
    print(f"   ❌ Error creating Flask app: {e}")
print()

print("=" * 60)
print("Health Check Complete!")
print("=" * 60)





Quick script to test backend initialization and check for common issues
"""
import sys
import os

# Add backend to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

print("=" * 60)
print("Backend Health Check")
print("=" * 60)
print()

# Check 1: Python version
print("1. Python Version:")
print(f"   {sys.version}")
print()

# Check 2: Virtual environment
print("2. Virtual Environment:")
venv = os.environ.get('VIRTUAL_ENV', None)
if venv:
    print(f"   ✅ Active: {venv}")
else:
    print("   ⚠️  No virtual environment detected")
print()

# Check 3: Critical imports
print("3. Testing Imports:")
try:
    from flask import Flask
    print("   ✅ Flask")
except ImportError as e:
    print(f"   ❌ Flask: {e}")

try:
    from flask_cors import CORS
    print("   ✅ Flask-CORS")
except ImportError as e:
    print(f"   ❌ Flask-CORS: {e}")

try:
    import pandas as pd
    print("   ✅ Pandas")
except ImportError as e:
    print(f"   ❌ Pandas: {e}")

try:
    import numpy as np
    print("   ✅ NumPy")
except ImportError as e:
    print(f"   ❌ NumPy: {e}")

try:
    from src.models.sentiment_analyzer import SentimentAnalyzer
    print("   ✅ SentimentAnalyzer")
except ImportError as e:
    print(f"   ❌ SentimentAnalyzer: {e}")

try:
    from src.utils.text_preprocessor import TextPreprocessor
    print("   ✅ TextPreprocessor")
except ImportError as e:
    print(f"   ❌ TextPreprocessor: {e}")

try:
    from auth import authenticate_user
    print("   ✅ auth module")
except ImportError as e:
    print(f"   ❌ auth module: {e}")
print()

# Check 4: File paths
print("4. Checking File Paths:")
paths_to_check = [
    ('data/processed/cleaned_reviews.csv', 'Review data (Milestone 1)'),
    ('data/processed/reviews_with_sentiment.csv', 'Review data (Milestone 2)'),
    ('data/models/lda_model', 'LDA model'),
    ('data/models/forecast_results.json', 'Forecast results'),
    ('auth.py', 'Authentication module'),
]

for path, description in paths_to_check:
    full_path = os.path.join(backend_dir, path)
    if os.path.exists(full_path):
        print(f"   ✅ {description}: {path}")
    else:
        print(f"   ⚠️  {description}: {path} (not found)")
print()

# Check 5: Data loading
print("5. Testing Data Loading:")
try:
    reviews_path = os.path.join(backend_dir, 'data', 'processed', 'reviews_with_sentiment.csv')
    if os.path.exists(reviews_path):
        df = pd.read_csv(reviews_path)
        print(f"   ✅ Loaded {len(df)} reviews from reviews_with_sentiment.csv")
        if 'sentiment' in df.columns:
            print("   ✅ Sentiment column found")
        else:
            print("   ⚠️  No sentiment column (will analyze on-the-fly)")
    else:
        cleaned_path = os.path.join(backend_dir, 'data', 'processed', 'cleaned_reviews.csv')
        if os.path.exists(cleaned_path):
            df = pd.read_csv(cleaned_path)
            print(f"   ⚠️  Loaded {len(df)} reviews from cleaned_reviews.csv (no sentiment)")
        else:
            print("   ❌ No review data found")
except Exception as e:
    print(f"   ❌ Error loading data: {e}")
print()

# Check 6: Flask app creation
print("6. Testing Flask App Creation:")
try:
    app = Flask(__name__)
    print("   ✅ Flask app can be created")
except Exception as e:
    print(f"   ❌ Error creating Flask app: {e}")
print()

print("=" * 60)
print("Health Check Complete!")
print("=" * 60)









