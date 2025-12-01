# Quick Start Guide

## 🚀 Getting Started with Small Business Intelligence Analyst

### Step 1: Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Download NLTK Data

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
```

### Step 3: Prepare Your Data

1. Place your raw data files in `data/raw/`:
   - Customer reviews CSV
   - Social media posts CSV
   - Market data CSV

2. Data format should include:
   - Text column (required)
   - Date column (optional, for trend analysis)
   - Source column (optional)
   - Location column (optional)

### Step 4: Run Data Pipeline

```bash
# Open Jupyter Notebook
jupyter notebook

# Navigate to notebooks/Milestone1/01_Data_Pipeline.ipynb
# Execute all cells to preprocess your data
```

### Step 5: Run Sentiment Analysis

```python
# In a new notebook or Python script
from src.models.sentiment_analyzer import SentimentAnalyzer
from src.utils.text_preprocessor import TextPreprocessor

# Initialize
analyzer = SentimentAnalyzer(method='vader')
preprocessor = TextPreprocessor()

# Analyze text
text = "Great service, very fast delivery!"
result = analyzer.analyze(text)
print(result)
```

### Step 6: Launch Web Interface

```bash
# Run Streamlit app
streamlit run src/api/app.py
```

### Step 7: Work Through Milestones

1. **Milestone 1**: Complete data pipeline notebook
2. **Milestone 2**: Implement understanding engine (sentiment + topic modeling)
3. **Milestone 3**: Build interactive prototype
4. **Milestone 4**: Evaluation and ethical analysis
5. **Milestone 5**: Final documentation and presentation

## 📝 Next Steps

1. Replace sample data with your actual datasets
2. Customize preprocessing for Ugandan context (Luganda support)
3. Enhance sentiment analysis with domain-specific models
4. Implement topic modeling using LDA or BERTopic
5. Build knowledge graphs for reasoning
6. Create comprehensive documentation

## 🆘 Troubleshooting

### Issue: NLTK data not downloading
**Solution**: Manually download using Python:
```python
import nltk
nltk.download('all')
```

### Issue: Import errors
**Solution**: Make sure you're in the project root directory and virtual environment is activated

### Issue: Memory errors with large datasets
**Solution**: Process data in batches, use generators instead of loading all data at once

## 📚 Resources

- [Project Requirements Summary](./PROJECT_REQUIREMENTS_SUMMARY.md)
- [Main README](./README.md)
- [Part A Documentation Template](./docs/PartA/README.md)
- [Part C Documentation Template](./docs/PartC/README.md)

---

**Happy Coding! 🎉**



