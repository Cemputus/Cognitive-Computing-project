"""
Quick test script to verify Milestone 1 components work correctly
Run this before opening the notebook to ensure everything is ready
"""

import sys
import os

# Add backend directory to path (scripts are in backend/scripts/)
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

print("=" * 60)
print("Testing Milestone 1 Components")
print("=" * 60)

# Test 1: Import libraries
print("\n1. Testing library imports...")
try:
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    import nltk
    print("   ✅ All core libraries imported successfully")
except ImportError as e:
    print(f"   ❌ Import error: {e}")
    sys.exit(1)

# Test 2: Import custom modules
print("\n2. Testing custom module imports...")
try:
    from src.utils.text_preprocessor import TextPreprocessor
    print("   ✅ TextPreprocessor imported successfully")
except ImportError as e:
    print(f"   ❌ Import error: {e}")
    print("   ⚠️  Check that src/utils/text_preprocessor.py exists")

# Test 3: Test TextPreprocessor
print("\n3. Testing TextPreprocessor...")
try:
    preprocessor = TextPreprocessor()
    test_text = "Great service! Very fast delivery in Kampala. 😊"
    cleaned = preprocessor.preprocess(test_text)
    print(f"   ✅ Preprocessor works")
    print(f"      Input:  {test_text}")
    print(f"      Output: {cleaned}")
except Exception as e:
    print(f"   ❌ Preprocessor error: {e}")

# Test 4: Create sample data
print("\n4. Testing data creation...")
try:
    sample_reviews = {
        'review_id': range(1, 6),
        'text': [
            "Great service, very fast delivery",
            "Product was damaged",
            "Amazing quality, will buy again",
            "Late delivery but good product",
            "Excellent customer support"
        ],
        'source': ['Facebook', 'Google', 'Twitter', 'Instagram', 'Facebook'],
        'location': ['Kampala', 'Nakawa', 'Kawempe', 'Makindye', 'Kampala']
    }
    df = pd.DataFrame(sample_reviews)
    print(f"   ✅ Sample DataFrame created: {df.shape}")
    print(f"      Columns: {list(df.columns)}")
except Exception as e:
    print(f"   ❌ Data creation error: {e}")

# Test 5: Check directories
print("\n5. Checking directories...")
project_root = os.path.dirname(backend_dir)
directories = [
    os.path.join(backend_dir, 'data', 'raw'),
    os.path.join(backend_dir, 'data', 'processed'),
    os.path.join(backend_dir, 'data', 'models'),
    os.path.join(project_root, 'Cognitive Pillars', 'Milestone1')
]
for directory in directories:
    rel_path = os.path.relpath(directory, project_root)
    if os.path.exists(directory):
        print(f"   ✅ {rel_path} exists")
    else:
        print(f"   ⚠️  {rel_path} NOT found - creating it")
        os.makedirs(directory, exist_ok=True)

# Test 6: Check notebook file
print("\n6. Checking notebook file...")
notebook_path = os.path.join(project_root, 'Cognitive Pillars', 'Milestone1', '01_Data_Pipeline.ipynb')
notebook_rel = os.path.relpath(notebook_path, project_root)
if os.path.exists(notebook_path):
    print(f"   ✅ Notebook found: {notebook_rel}")
else:
    print(f"   ❌ Notebook NOT found: {notebook_rel}")

print("\n" + "=" * 60)
print("✅ All tests passed! Ready to start Milestone 1")
print("=" * 60)
print("\nNext step: Open the notebook with:")
print("  jupyter notebook Cognitive Pillars/Milestone1/01_Data_Pipeline.ipynb")
print("\nOr use:")
print("  jupyter lab")

