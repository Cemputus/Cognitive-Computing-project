# 📊 Data Collection Guide - Milestone 1

## Overview

The updated Milestone 1 notebook now includes:

✅ **5000 Synthetic Reviews** - Diverse, realistic customer reviews  
✅ **Web Scraping** - Attempts to collect real reviews from Reddit  
✅ **Automatic Merging** - Combines all data sources into one DataFrame  

---

## What's New

### 1. Enhanced Data Generation
- **5000 reviews** instead of 100
- **90 unique review templates** (30 positive, 30 negative, 30 neutral)
- **Realistic sentiment distribution**: 60% positive, 25% neutral, 15% negative
- **Varied locations**: 10 Kampala areas
- **Multiple sources**: Facebook, Google, Twitter, Instagram, Website, WhatsApp
- **Date range**: Spread over last 2 years

### 2. Web Scraping Capability
- **Reddit Integration**: Attempts to scrape public reviews from Reddit
- **Respectful scraping**: Includes rate limiting and proper headers
- **Graceful fallback**: Continues with synthetic data if scraping fails
- **Public data only**: Uses Reddit's public JSON API (no authentication needed)

### 3. Automatic Data Merging
- Combines synthetic and scraped data
- Resets review IDs sequentially
- Maintains consistent column structure
- Saves raw data for reference

---

## How It Works

### Step 1: Synthetic Data Generation
```python
collector = DataCollector()
df_synthetic = collector.generate_synthetic_reviews(n_reviews=5000)
```

**Features:**
- 90 diverse review templates
- Realistic sentiment distribution
- Kampala-specific locations
- Varied business contexts
- Date spread over 2 years

### Step 2: Web Scraping (Optional)
```python
df_reddit = collector.scrape_reddit_reviews(limit=200)
```

**Features:**
- Uses Reddit's public JSON API
- No authentication required
- Respects rate limits
- Filters short/invalid posts
- Falls back gracefully if unavailable

### Step 3: Data Merging
```python
df_merged = collector.collect_all_data(
    n_synthetic=5000,
    try_reddit=True,
    reddit_limit=200
)
```

**Result:**
- Single DataFrame with all reviews
- Sequential review IDs
- Consistent structure
- Ready for preprocessing

---

## Data Structure

The collected DataFrame includes:

| Column | Description | Example |
|--------|-------------|---------|
| `review_id` | Unique identifier | 1, 2, 3... |
| `text` | Review text | "Great service! Very fast delivery..." |
| `date` | Review date | "2024-01-15" |
| `source` | Data source | "Facebook", "Reddit", etc. |
| `location` | Location | "Kampala", "Nakawa", etc. |
| `sentiment_label` | Ground truth (synthetic only) | "positive", "negative", "neutral" |

---

## Running the Updated Notebook

1. **Open the notebook:**
   ```bash
   jupyter notebook notebooks/Milestone1/01_Data_Pipeline.ipynb
   ```

2. **Run Cell 1:** Imports all libraries (including DataCollector)

3. **Run Cell 3:** Data collection
   - Generates 5000 synthetic reviews
   - Attempts Reddit scraping
   - Merges everything
   - Saves raw data

4. **Continue with remaining cells** for preprocessing and analysis

---

## Expected Outputs

### After Data Collection:
- ✅ **5000+ reviews** in DataFrame
- ✅ Raw data saved to `data/raw/collected_reviews.csv`
- ✅ Summary statistics printed
- ✅ Source and location distributions

### Data Distribution:
- **Sources**: Mix of Facebook, Google, Twitter, Instagram, Website, WhatsApp, Reddit
- **Locations**: 10 Kampala areas
- **Sentiments**: 60% positive, 25% neutral, 15% negative
- **Dates**: Spread over last 2 years

---

## Customization Options

### Adjust Number of Reviews
```python
df_reviews = collector.collect_all_data(
    n_synthetic=10000,  # Generate 10,000 instead of 5,000
    try_reddit=True,
    reddit_limit=500
)
```

### Disable Web Scraping
```python
df_reviews = collector.collect_all_data(
    n_synthetic=5000,
    try_reddit=False,  # Skip Reddit scraping
    reddit_limit=0
)
```

### Change Reddit Subreddit
Edit `src/utils/data_collector.py`:
```python
df_reddit = collector.scrape_reddit_reviews(
    subreddit='reviews',  # Change to your preferred subreddit
    limit=200
)
```

---

## Troubleshooting

### Issue: Reddit scraping fails
**Solution:** This is normal! The notebook will continue with synthetic data only. Reddit may:
- Rate limit requests
- Block certain user agents
- Require authentication for some endpoints

**Impact:** None - you'll still have 5000 synthetic reviews

### Issue: Import error for DataCollector
**Solution:** Make sure you're running from the project root:
```python
import sys
sys.path.append('../../')
from src.utils.data_collector import DataCollector
```

### Issue: Not enough reviews generated
**Solution:** Check the output. You should see:
- "✅ Generated 5000 synthetic reviews"
- Total count in final DataFrame

---

## Data Quality

### Synthetic Data Quality:
- ✅ **Diverse**: 90 unique templates
- ✅ **Realistic**: Based on common review patterns
- ✅ **Contextual**: Kampala-specific locations and businesses
- ✅ **Balanced**: Realistic sentiment distribution

### Web Scraped Data:
- ✅ **Real reviews**: Actual user feedback
- ✅ **Varied**: Different writing styles
- ✅ **Validated**: Filtered for minimum length
- ⚠️ **May vary**: Depends on Reddit availability

---

## Next Steps

After data collection:

1. ✅ **Preprocessing** - Clean and normalize text (Cell 5)
2. ✅ **Quality Analysis** - Analyze data characteristics (Cell 7)
3. ✅ **Save Processed Data** - Prepare for Milestone 2 (Cell 9)

---

## Summary

✅ **5000 diverse synthetic reviews** generated  
✅ **Web scraping** attempts to get real data  
✅ **Automatic merging** into one DataFrame  
✅ **Ready for preprocessing** and analysis  

**Your dataset is now much larger and more realistic! 🎉**

