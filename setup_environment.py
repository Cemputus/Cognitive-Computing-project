"""
Setup script to verify environment and prepare for Milestone 1
Run this before starting Milestone 1 notebook
"""

import sys
import subprocess
import os

def check_package(package_name):
    """Check if a package is installed"""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def install_package(package_name):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except:
        return False

def download_nltk_data():
    """Download required NLTK data"""
    try:
        import nltk
        print("Downloading NLTK data...")
        nltk.download('punkt', quiet=False)
        nltk.download('stopwords', quiet=False)
        nltk.download('wordnet', quiet=False)
        print("✅ NLTK data downloaded successfully")
        return True
    except Exception as e:
        print(f"⚠️ Error downloading NLTK data: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        'data/raw',
        'data/processed',
        'data/models',
        'evaluation'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Directory created/verified: {directory}")

def main():
    print("=" * 60)
    print("Setting up environment for Milestone 1")
    print("=" * 60)
    
    # Check Python version
    print(f"\nPython version: {sys.version}")
    
    # Create directories
    print("\n1. Creating project directories...")
    create_directories()
    
    # Check essential packages
    print("\n2. Checking essential packages...")
    essential_packages = {
        'pandas': 'pandas',
        'numpy': 'numpy',
        'nltk': 'nltk',
        'matplotlib': 'matplotlib',
        'seaborn': 'seaborn'
    }
    
    missing_packages = []
    for package, pip_name in essential_packages.items():
        if check_package(package):
            print(f"   ✅ {package} is installed")
        else:
            print(f"   ⚠️  {package} is NOT installed")
            missing_packages.append(pip_name)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Please run: pip install -r requirements.txt")
        response = input("\nWould you like to install missing packages now? (y/n): ")
        if response.lower() == 'y':
            for package in missing_packages:
                print(f"Installing {package}...")
                install_package(package)
    
    # Download NLTK data
    print("\n3. Setting up NLTK data...")
    if check_package('nltk'):
        download_nltk_data()
    else:
        print("⚠️  NLTK not installed. Install with: pip install nltk")
    
    # Verify source modules
    print("\n4. Verifying source modules...")
    source_files = [
        'src/utils/text_preprocessor.py',
        'src/models/sentiment_analyzer.py'
    ]
    
    for file_path in source_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path} exists")
        else:
            print(f"   ⚠️  {file_path} NOT found")
    
    print("\n" + "=" * 60)
    print("Setup complete! You can now start Milestone 1 notebook.")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Open Jupyter Notebook: jupyter notebook")
    print("2. Navigate to: notebooks/Milestone1/")
    print("3. Open: 01_Data_Pipeline.ipynb")
    print("4. Run all cells sequentially")

if __name__ == "__main__":
    main()

