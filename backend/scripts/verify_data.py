"""
Data Verification Script
Checks if all required data files from Milestone 2 are present and accessible.
Run this script to verify your setup before starting the backend.
"""

import os
import sys
import json
import pandas as pd

# Get backend directory
current_file = os.path.abspath(__file__)
scripts_dir = os.path.dirname(current_file)
backend_dir = os.path.dirname(scripts_dir)

def check_file(path, description, required=True):
    """Check if a file or directory exists"""
    full_path = os.path.join(backend_dir, path)
    exists = os.path.exists(full_path)
    status = "✅" if exists else ("❌" if required else "⚠️")
    print(f"{status} {description}: {path}")
    if exists:
        if os.path.isfile(full_path):
            size = os.path.getsize(full_path)
            print(f"   Size: {size:,} bytes ({size / 1024:.2f} KB)")
        elif os.path.isdir(full_path):
            files = os.listdir(full_path)
            print(f"   Contains {len(files)} file(s)")
    return exists

def check_csv_file(path, description):
    """Check CSV file and show basic stats"""
    full_path = os.path.join(backend_dir, path)
    if os.path.exists(full_path):
        try:
            df = pd.read_csv(full_path, nrows=1)  # Just read header
            print(f"✅ {description}: {path}")
            print(f"   Columns: {', '.join(df.columns[:5])}{'...' if len(df.columns) > 5 else ''}")
            # Get full row count
            df_full = pd.read_csv(full_path)
            print(f"   Rows: {len(df_full):,}")
            return True
        except Exception as e:
            print(f"❌ {description}: {path} (Error reading: {e})")
            return False
    else:
        print(f"❌ {description}: {path} (Not found)")
        return False

def check_json_file(path, description):
    """Check JSON file"""
    full_path = os.path.join(backend_dir, path)
    if os.path.exists(full_path):
        try:
            with open(full_path, 'r') as f:
                data = json.load(f)
            print(f"✅ {description}: {path}")
            if isinstance(data, dict):
                print(f"   Keys: {', '.join(list(data.keys())[:5])}{'...' if len(data.keys()) > 5 else ''}")
            return True
        except Exception as e:
            print(f"❌ {description}: {path} (Error reading: {e})")
            return False
    else:
        print(f"❌ {description}: {path} (Not found)")
        return False

def main():
    print("=" * 70)
    print("DATA VERIFICATION - Milestone 2 Output Check")
    print("=" * 70)
    print()
    
    print("Checking required data files from Milestone 2:")
    print("-" * 70)
    
    # Required files
    required_files = []
    
    # 1. Processed reviews with sentiment
    if check_csv_file('data/processed/reviews_with_sentiment.csv', 'Reviews with Sentiment'):
        required_files.append(True)
    else:
        required_files.append(False)
        print("   ⚠️  Backend can use cleaned_reviews.csv as fallback")
    
    # 2. LDA Model
    if check_file('data/models/lda_model', 'LDA Topic Model'):
        required_files.append(True)
    else:
        required_files.append(False)
        print("   ⚠️  Topic Analysis will not be available")
    
    # 3. Forecast Results (optional - can be generated on-the-fly)
    if check_json_file('data/models/forecast_results.json', 'Forecast Results'):
        required_files.append(True)
    else:
        required_files.append(False)
        print("   ℹ️  Forecasts will be generated on-the-fly from review data")
    
    print()
    print("Checking optional/supporting files:")
    print("-" * 70)
    
    # Optional files
    check_file('data/processed/cleaned_reviews.csv', 'Cleaned Reviews (Fallback)', required=False)
    check_file('data/models/knowledge_graph.pkl', 'Knowledge Graph', required=False)
    check_file('data/models/sentiment_analyzer.pkl', 'Saved Sentiment Analyzer', required=False)
    
    print()
    print("=" * 70)
    
    # Summary
    all_required = all(required_files)
    if all_required:
        print("✅ ALL REQUIRED FILES PRESENT")
        print("✅ Backend is ready to run without rerunning Milestone 2")
    else:
        print("⚠️  SOME FILES ARE MISSING")
        print("⚠️  Backend will work but some features may be limited:")
        if not required_files[0]:
            print("   - Sentiment analysis will be done on-the-fly (slower)")
        if not required_files[1]:
            print("   - Topic Analysis will not be available")
        if not required_files[2]:
            print("   - Forecasts will be generated on-the-fly (slower)")
        print()
        print("To generate missing files, run the Milestone 2 notebook.")
    
    print("=" * 70)
    print()
    print("Next steps:")
    print("1. Start the backend: python backend_api.py")
    print("2. Or use the startup script: scripts/start_backend.ps1 (Windows)")
    print("3. The backend will automatically use available files")
    print("4. Missing files will trigger on-the-fly generation where possible")
    print()

if __name__ == '__main__':
    main()



Data Verification Script
Checks if all required data files from Milestone 2 are present and accessible.
Run this script to verify your setup before starting the backend.
"""

import os
import sys
import json
import pandas as pd

# Get backend directory
current_file = os.path.abspath(__file__)
scripts_dir = os.path.dirname(current_file)
backend_dir = os.path.dirname(scripts_dir)

def check_file(path, description, required=True):
    """Check if a file or directory exists"""
    full_path = os.path.join(backend_dir, path)
    exists = os.path.exists(full_path)
    status = "✅" if exists else ("❌" if required else "⚠️")
    print(f"{status} {description}: {path}")
    if exists:
        if os.path.isfile(full_path):
            size = os.path.getsize(full_path)
            print(f"   Size: {size:,} bytes ({size / 1024:.2f} KB)")
        elif os.path.isdir(full_path):
            files = os.listdir(full_path)
            print(f"   Contains {len(files)} file(s)")
    return exists

def check_csv_file(path, description):
    """Check CSV file and show basic stats"""
    full_path = os.path.join(backend_dir, path)
    if os.path.exists(full_path):
        try:
            df = pd.read_csv(full_path, nrows=1)  # Just read header
            print(f"✅ {description}: {path}")
            print(f"   Columns: {', '.join(df.columns[:5])}{'...' if len(df.columns) > 5 else ''}")
            # Get full row count
            df_full = pd.read_csv(full_path)
            print(f"   Rows: {len(df_full):,}")
            return True
        except Exception as e:
            print(f"❌ {description}: {path} (Error reading: {e})")
            return False
    else:
        print(f"❌ {description}: {path} (Not found)")
        return False

def check_json_file(path, description):
    """Check JSON file"""
    full_path = os.path.join(backend_dir, path)
    if os.path.exists(full_path):
        try:
            with open(full_path, 'r') as f:
                data = json.load(f)
            print(f"✅ {description}: {path}")
            if isinstance(data, dict):
                print(f"   Keys: {', '.join(list(data.keys())[:5])}{'...' if len(data.keys()) > 5 else ''}")
            return True
        except Exception as e:
            print(f"❌ {description}: {path} (Error reading: {e})")
            return False
    else:
        print(f"❌ {description}: {path} (Not found)")
        return False

def main():
    print("=" * 70)
    print("DATA VERIFICATION - Milestone 2 Output Check")
    print("=" * 70)
    print()
    
    print("Checking required data files from Milestone 2:")
    print("-" * 70)
    
    # Required files
    required_files = []
    
    # 1. Processed reviews with sentiment
    if check_csv_file('data/processed/reviews_with_sentiment.csv', 'Reviews with Sentiment'):
        required_files.append(True)
    else:
        required_files.append(False)
        print("   ⚠️  Backend can use cleaned_reviews.csv as fallback")
    
    # 2. LDA Model
    if check_file('data/models/lda_model', 'LDA Topic Model'):
        required_files.append(True)
    else:
        required_files.append(False)
        print("   ⚠️  Topic Analysis will not be available")
    
    # 3. Forecast Results (optional - can be generated on-the-fly)
    if check_json_file('data/models/forecast_results.json', 'Forecast Results'):
        required_files.append(True)
    else:
        required_files.append(False)
        print("   ℹ️  Forecasts will be generated on-the-fly from review data")
    
    print()
    print("Checking optional/supporting files:")
    print("-" * 70)
    
    # Optional files
    check_file('data/processed/cleaned_reviews.csv', 'Cleaned Reviews (Fallback)', required=False)
    check_file('data/models/knowledge_graph.pkl', 'Knowledge Graph', required=False)
    check_file('data/models/sentiment_analyzer.pkl', 'Saved Sentiment Analyzer', required=False)
    
    print()
    print("=" * 70)
    
    # Summary
    all_required = all(required_files)
    if all_required:
        print("✅ ALL REQUIRED FILES PRESENT")
        print("✅ Backend is ready to run without rerunning Milestone 2")
    else:
        print("⚠️  SOME FILES ARE MISSING")
        print("⚠️  Backend will work but some features may be limited:")
        if not required_files[0]:
            print("   - Sentiment analysis will be done on-the-fly (slower)")
        if not required_files[1]:
            print("   - Topic Analysis will not be available")
        if not required_files[2]:
            print("   - Forecasts will be generated on-the-fly (slower)")
        print()
        print("To generate missing files, run the Milestone 2 notebook.")
    
    print("=" * 70)
    print()
    print("Next steps:")
    print("1. Start the backend: python backend_api.py")
    print("2. Or use the startup script: scripts/start_backend.ps1 (Windows)")
    print("3. The backend will automatically use available files")
    print("4. Missing files will trigger on-the-fly generation where possible")
    print()

if __name__ == '__main__':
    main()







