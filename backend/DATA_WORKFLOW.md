# Data Workflow Guide

## Overview

This guide explains how the backend uses data from Milestone 2 and ensures you don't need to rerun the notebook repeatedly.

## One-Time Setup (Milestone 2)

After running Milestone 2 notebook **once**, it generates the following files in `backend/data/`:

### Required Files (for full functionality)

1. **`data/processed/reviews_with_sentiment.csv`**
   - Contains all reviews with pre-analyzed sentiment
   - **Location**: `backend/data/processed/reviews_with_sentiment.csv`
   - **Used by**: All sentiment analysis endpoints, dashboard stats, location/platform/topic analysis
   - **Fallback**: If missing, backend uses `cleaned_reviews.csv` and analyzes sentiment on-the-fly

2. **`data/models/lda_model/`** (directory with model files)
   - Trained LDA topic model
   - **Location**: `backend/data/models/lda_model`
   - **Used by**: Topic Analysis page (`/api/topics`)
   - **Fallback**: If missing, Topic Analysis will show a message asking to run Milestone 2

3. **`data/models/forecast_results.json`**
   - Pre-computed forecast results
   - **Location**: `backend/data/models/forecast_results.json`
   - **Used by**: Trends & Insights page (`/api/forecast`)
   - **Fallback**: If missing, backend generates forecasts on-the-fly from review data

### Optional Files

- `data/processed/cleaned_reviews.csv` - Fallback if reviews_with_sentiment.csv is missing
- `data/models/knowledge_graph.pkl` - Knowledge graph for advanced features
- `data/models/sentiment_analyzer.pkl` - Saved analyzer (not required, backend creates its own)

## How the Backend Works

### 1. **Data Loading (Startup)**
When the backend starts, it:
- First tries to load `reviews_with_sentiment.csv` (Milestone 2 output)
- Falls back to `cleaned_reviews.csv` (Milestone 1 output) if needed
- Loads LDA model if available
- Loads forecast results if available

### 2. **On-the-Fly Generation**
The backend can generate missing data on-the-fly:
- **Forecasts**: If `forecast_results.json` is missing, it generates forecasts from review data
- **Sentiment**: If reviews don't have sentiment, it analyzes them on-the-fly
- **Topics**: If LDA model is missing, it returns a helpful error message

### 3. **Data Persistence**
- Generated forecasts are automatically saved to `forecast_results.json` for future use
- Review data is read-only (not modified by the backend)
- Models are read-only (not retrained by the backend)

## Verification

### Check Your Data

Run the verification script:

```bash
# Windows PowerShell
cd backend
python scripts/verify_data.py

# Or from project root
python backend/scripts/verify_data.py
```

This will show you:
- ✅ Which files are present
- ❌ Which files are missing
- ⚠️ What features will be limited if files are missing

### Expected Output

```
======================================================================
DATA VERIFICATION - Milestone 2 Output Check
======================================================================

Checking required data files from Milestone 2:
----------------------------------------------------------------------
✅ Reviews with Sentiment: data/processed/reviews_with_sentiment.csv
   Columns: review_id, text, cleaned_text, sentiment, compound...
   Rows: 1,234
✅ LDA Topic Model: data/models/lda_model
   Contains 4 file(s)
✅ Forecast Results: data/models/forecast_results.json
   Keys: current_sentiment, forecast_avg, trend_direction...

======================================================================
✅ ALL REQUIRED FILES PRESENT
✅ Backend is ready to run without rerunning Milestone 2
======================================================================
```

## When to Rerun Milestone 2

You only need to rerun Milestone 2 if:

1. **New review data is added** - You've collected new reviews and want to include them
2. **LDA model needs retraining** - You want to update topics based on new data
3. **Model version mismatch** - You get NumPy version errors (regenerate the model)
4. **Data corruption** - Files are corrupted or incomplete

## Workflow Summary

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Run Milestone 2 Notebook (ONE TIME)                       │
│    ↓                                                          │
│    Generates:                                                 │
│    - reviews_with_sentiment.csv                               │
│    - lda_model/                                               │
│    - forecast_results.json                                    │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. Verify Data (Optional)                                    │
│    python backend/scripts/verify_data.py                    │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. Start Backend                                            │
│    python backend_api.py                                     │
│    OR                                                        │
│    scripts/start_backend.ps1                                │
│    ↓                                                         │
│    Backend automatically:                                    │
│    - Loads saved data files                                  │
│    - Generates missing data on-the-fly                       │
│    - Saves generated forecasts for future use               │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. Use Frontend                                             │
│    - Dashboard: Shows stats from saved data                 │
│    - Sentiment Analysis: Uses saved sentiment or analyzes   │
│    - Topic Analysis: Uses saved LDA model                    │
│    - Trends & Insights: Uses saved or generated forecasts   │
└─────────────────────────────────────────────────────────────┘
```

## Troubleshooting

### "Topic models are being generated" message
- **Cause**: LDA model file is missing
- **Solution**: Run Milestone 2 notebook to generate the model

### "No review data found"
- **Cause**: Neither `reviews_with_sentiment.csv` nor `cleaned_reviews.csv` exists
- **Solution**: Run Milestone 1 notebook first, then Milestone 2

### "LDA model version mismatch"
- **Cause**: Model was created with a different NumPy version
- **Solution**: Regenerate the model by running Milestone 2 notebook again

### Forecasts are slow
- **Cause**: `forecast_results.json` is missing, so forecasts are generated on-the-fly
- **Solution**: Run Milestone 2 notebook to pre-generate forecasts, or wait for the backend to save them automatically

## Best Practices

1. **Run Milestone 2 once** after collecting/updating review data
2. **Verify data** using the verification script before starting the backend
3. **Keep data files** - Don't delete the generated files in `backend/data/`
4. **Backup data** - Consider backing up `backend/data/` folder
5. **Check logs** - Backend prints status messages showing which files it's using

## File Locations Reference

```
backend/
├── data/
│   ├── processed/
│   │   ├── reviews_with_sentiment.csv  ← Milestone 2 output
│   │   └── cleaned_reviews.csv          ← Milestone 1 output (fallback)
│   └── models/
│       ├── lda_model/                   ← Milestone 2 output (directory)
│       │   ├── lda_model.expElogbeta.npy
│       │   ├── lda_model.id2word
│       │   └── lda_model.state
│       └── forecast_results.json         ← Milestone 2 output
└── backend_api.py                        ← Reads from above files
```

## Summary

✅ **You only need to run Milestone 2 once** after collecting new data  
✅ **Backend automatically uses saved files** when available  
✅ **Backend generates missing data on-the-fly** when needed  
✅ **Generated data is saved** for future use  
✅ **No need to rerun notebooks** for normal frontend usage




## Overview

This guide explains how the backend uses data from Milestone 2 and ensures you don't need to rerun the notebook repeatedly.

## One-Time Setup (Milestone 2)

After running Milestone 2 notebook **once**, it generates the following files in `backend/data/`:

### Required Files (for full functionality)

1. **`data/processed/reviews_with_sentiment.csv`**
   - Contains all reviews with pre-analyzed sentiment
   - **Location**: `backend/data/processed/reviews_with_sentiment.csv`
   - **Used by**: All sentiment analysis endpoints, dashboard stats, location/platform/topic analysis
   - **Fallback**: If missing, backend uses `cleaned_reviews.csv` and analyzes sentiment on-the-fly

2. **`data/models/lda_model/`** (directory with model files)
   - Trained LDA topic model
   - **Location**: `backend/data/models/lda_model`
   - **Used by**: Topic Analysis page (`/api/topics`)
   - **Fallback**: If missing, Topic Analysis will show a message asking to run Milestone 2

3. **`data/models/forecast_results.json`**
   - Pre-computed forecast results
   - **Location**: `backend/data/models/forecast_results.json`
   - **Used by**: Trends & Insights page (`/api/forecast`)
   - **Fallback**: If missing, backend generates forecasts on-the-fly from review data

### Optional Files

- `data/processed/cleaned_reviews.csv` - Fallback if reviews_with_sentiment.csv is missing
- `data/models/knowledge_graph.pkl` - Knowledge graph for advanced features
- `data/models/sentiment_analyzer.pkl` - Saved analyzer (not required, backend creates its own)

## How the Backend Works

### 1. **Data Loading (Startup)**
When the backend starts, it:
- First tries to load `reviews_with_sentiment.csv` (Milestone 2 output)
- Falls back to `cleaned_reviews.csv` (Milestone 1 output) if needed
- Loads LDA model if available
- Loads forecast results if available

### 2. **On-the-Fly Generation**
The backend can generate missing data on-the-fly:
- **Forecasts**: If `forecast_results.json` is missing, it generates forecasts from review data
- **Sentiment**: If reviews don't have sentiment, it analyzes them on-the-fly
- **Topics**: If LDA model is missing, it returns a helpful error message

### 3. **Data Persistence**
- Generated forecasts are automatically saved to `forecast_results.json` for future use
- Review data is read-only (not modified by the backend)
- Models are read-only (not retrained by the backend)

## Verification

### Check Your Data

Run the verification script:

```bash
# Windows PowerShell
cd backend
python scripts/verify_data.py

# Or from project root
python backend/scripts/verify_data.py
```

This will show you:
- ✅ Which files are present
- ❌ Which files are missing
- ⚠️ What features will be limited if files are missing

### Expected Output

```
======================================================================
DATA VERIFICATION - Milestone 2 Output Check
======================================================================

Checking required data files from Milestone 2:
----------------------------------------------------------------------
✅ Reviews with Sentiment: data/processed/reviews_with_sentiment.csv
   Columns: review_id, text, cleaned_text, sentiment, compound...
   Rows: 1,234
✅ LDA Topic Model: data/models/lda_model
   Contains 4 file(s)
✅ Forecast Results: data/models/forecast_results.json
   Keys: current_sentiment, forecast_avg, trend_direction...

======================================================================
✅ ALL REQUIRED FILES PRESENT
✅ Backend is ready to run without rerunning Milestone 2
======================================================================
```

## When to Rerun Milestone 2

You only need to rerun Milestone 2 if:

1. **New review data is added** - You've collected new reviews and want to include them
2. **LDA model needs retraining** - You want to update topics based on new data
3. **Model version mismatch** - You get NumPy version errors (regenerate the model)
4. **Data corruption** - Files are corrupted or incomplete

## Workflow Summary

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Run Milestone 2 Notebook (ONE TIME)                       │
│    ↓                                                          │
│    Generates:                                                 │
│    - reviews_with_sentiment.csv                               │
│    - lda_model/                                               │
│    - forecast_results.json                                    │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. Verify Data (Optional)                                    │
│    python backend/scripts/verify_data.py                    │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. Start Backend                                            │
│    python backend_api.py                                     │
│    OR                                                        │
│    scripts/start_backend.ps1                                │
│    ↓                                                         │
│    Backend automatically:                                    │
│    - Loads saved data files                                  │
│    - Generates missing data on-the-fly                       │
│    - Saves generated forecasts for future use               │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. Use Frontend                                             │
│    - Dashboard: Shows stats from saved data                 │
│    - Sentiment Analysis: Uses saved sentiment or analyzes   │
│    - Topic Analysis: Uses saved LDA model                    │
│    - Trends & Insights: Uses saved or generated forecasts   │
└─────────────────────────────────────────────────────────────┘
```

## Troubleshooting

### "Topic models are being generated" message
- **Cause**: LDA model file is missing
- **Solution**: Run Milestone 2 notebook to generate the model

### "No review data found"
- **Cause**: Neither `reviews_with_sentiment.csv` nor `cleaned_reviews.csv` exists
- **Solution**: Run Milestone 1 notebook first, then Milestone 2

### "LDA model version mismatch"
- **Cause**: Model was created with a different NumPy version
- **Solution**: Regenerate the model by running Milestone 2 notebook again

### Forecasts are slow
- **Cause**: `forecast_results.json` is missing, so forecasts are generated on-the-fly
- **Solution**: Run Milestone 2 notebook to pre-generate forecasts, or wait for the backend to save them automatically

## Best Practices

1. **Run Milestone 2 once** after collecting/updating review data
2. **Verify data** using the verification script before starting the backend
3. **Keep data files** - Don't delete the generated files in `backend/data/`
4. **Backup data** - Consider backing up `backend/data/` folder
5. **Check logs** - Backend prints status messages showing which files it's using

## File Locations Reference

```
backend/
├── data/
│   ├── processed/
│   │   ├── reviews_with_sentiment.csv  ← Milestone 2 output
│   │   └── cleaned_reviews.csv          ← Milestone 1 output (fallback)
│   └── models/
│       ├── lda_model/                   ← Milestone 2 output (directory)
│       │   ├── lda_model.expElogbeta.npy
│       │   ├── lda_model.id2word
│       │   └── lda_model.state
│       └── forecast_results.json         ← Milestone 2 output
└── backend_api.py                        ← Reads from above files
```

## Summary

✅ **You only need to run Milestone 2 once** after collecting new data  
✅ **Backend automatically uses saved files** when available  
✅ **Backend generates missing data on-the-fly** when needed  
✅ **Generated data is saved** for future use  
✅ **No need to rerun notebooks** for normal frontend usage




