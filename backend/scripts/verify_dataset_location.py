"""
Quick script to verify dataset location and status
"""

import os
import pandas as pd

print("=" * 60)
print("Dataset Location Verification")
print("=" * 60)

# Define paths
relative_path = 'data/raw/collected_reviews.csv'
absolute_path = os.path.abspath(relative_path)
project_root = os.path.abspath('.')

print(f"\n📍 Dataset Location:")
print(f"   Relative path: {relative_path}")
print(f"   Absolute path: {absolute_path}")
print(f"\n📂 Project Structure:")
print(f"   Project root: {project_root}")
print(f"   Data directory: {os.path.abspath('data')}")
print(f"   Raw directory: {os.path.abspath('data/raw')}")

print(f"\n✅ Directory Status:")
print(f"   data/ directory exists: {os.path.exists('data')}")
print(f"   data/raw/ directory exists: {os.path.exists('data/raw')}")
print(f"   Dataset file exists: {os.path.exists(relative_path)}")

if os.path.exists(relative_path):
    print(f"\n📊 Current Dataset Info:")
    try:
        df = pd.read_csv(relative_path)
        file_size = os.path.getsize(relative_path) / 1024  # KB
        
        print(f"   Total reviews: {len(df)}")
        print(f"   File size: {file_size:.2f} KB")
        print(f"   Columns: {list(df.columns)}")
        
        if len(df) < 5000:
            print(f"\n⚠️  NOTE: File has only {len(df)} reviews")
            print(f"   Run Cell 4 in the notebook to generate 5000+ reviews")
        else:
            print(f"\n✅ Dataset has {len(df)} reviews - looks good!")
            
    except Exception as e:
        print(f"   ⚠️  Error reading file: {e}")
else:
    print(f"\n⚠️  Dataset file not found yet")
    print(f"   Run Cell 4 in the notebook to generate and save the dataset")

print("\n" + "=" * 60)
print("✅ Verification Complete!")
print("=" * 60)

