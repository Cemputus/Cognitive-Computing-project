# 📁 Dataset Location Information

## Dataset Save Location

The dataset is saved to:

```
D:\Cognitive Computing\data\raw\collected_reviews.csv
```

### Relative Path
From the notebook location (`notebooks/Milestone1/`), the path is:
```python
'../../data/raw/collected_reviews.csv'
```

From the project root, the path is:
```python
'data/raw/collected_reviews.csv'
```

---

## Current Status

✅ **Directory exists**: `data/raw/`  
✅ **File exists**: `data/raw/collected_reviews.csv`  
⚠️ **Current file**: Has 100 reviews (old sample data)

---

## How to Generate & Save 5000+ Reviews

### In the Notebook (Cell 4):

The notebook already includes code to save the dataset:

```python
# Data Collection: Generate 5000 synthetic reviews + attempt web scraping
collector = DataCollector()
df_reviews = collector.collect_all_data(
    n_synthetic=5000,
    try_reddit=True,
    reddit_limit=200
)

# Save raw dataset to data/raw directory
import os
os.makedirs('../../data/raw', exist_ok=True)
raw_data_path = '../../data/raw/collected_reviews.csv'
df_reviews.to_csv(raw_data_path, index=False)
print(f"\n💾 Raw dataset saved to: {os.path.abspath(raw_data_path)}")
print(f"   Total reviews saved: {len(df_reviews)}")
```

### Steps to Run:

1. **Open the notebook:**
   ```bash
   jupyter notebook notebooks/Milestone1/01_Data_Pipeline.ipynb
   ```

2. **Run Cell 4** - This will:
   - Generate 5000 synthetic reviews
   - Attempt to scrape Reddit (may add 100-200 more)
   - Save everything to `data/raw/collected_reviews.csv`

3. **Verify the save:**
   After running, you'll see:
   ```
   💾 Raw dataset saved to: D:\Cognitive Computing\data\raw\collected_reviews.csv
      Total reviews saved: 5100
      File size: XXX KB
   ```

---

## File Structure

```
Cognitive Computing/
├── data/
│   └── raw/
│       └── collected_reviews.csv    ← Dataset saved here
├── notebooks/
│   └── Milestone1/
│       └── 01_Data_Pipeline.ipynb   ← Notebook location
└── ...
```

---

## Verify Dataset Location

### Check if file exists:
```python
import os
path = 'data/raw/collected_reviews.csv'
print(f"File exists: {os.path.exists(path)}")
print(f"Absolute path: {os.path.abspath(path)}")
```

### Load the dataset:
```python
import pandas as pd
df = pd.read_csv('data/raw/collected_reviews.csv')
print(f"Total reviews: {len(df)}")
print(f"Columns: {list(df.columns)}")
```

---

## Notes

- The file is automatically created if it doesn't exist
- The directory `data/raw/` is created automatically
- Running Cell 4 will **overwrite** the existing file with new data
- The file will contain 5000+ reviews after running Cell 4

---

## Quick Check Script

Run this to verify the dataset location:

```python
import os
import pandas as pd

path = 'data/raw/collected_reviews.csv'
if os.path.exists(path):
    df = pd.read_csv(path)
    abs_path = os.path.abspath(path)
    file_size = os.path.getsize(path) / 1024  # KB
    
    print(f"✅ Dataset found!")
    print(f"   Location: {abs_path}")
    print(f"   Reviews: {len(df)}")
    print(f"   File size: {file_size:.2f} KB")
    print(f"   Columns: {list(df.columns)}")
else:
    print(f"❌ Dataset not found at: {os.path.abspath(path)}")
    print("   Run Cell 4 in the notebook to generate and save the dataset")
```

