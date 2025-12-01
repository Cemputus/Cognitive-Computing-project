# Backend API

## Starting the Server

**Important**: Run from the `backend/` directory:

```powershell
# From project root (D:\Cognitive Computing)
cd backend
python backend_api.py
```

Or use the provided scripts:
```powershell
# From project root
backend\scripts\start_backend.bat

# OR from backend/scripts/
cd backend\scripts
.\start_backend.bat
```

## Path Configuration

The backend automatically detects the `backend/` directory and adds it to the Python path, so imports work correctly:
- `from src.models...` works because `src/` is in `backend/`
- `from auth import...` works because `auth.py` is in `backend/`
- Data paths use `backend_dir` which points to `backend/`

## Troubleshooting

If you see `ModuleNotFoundError`:
1. Make sure you're in the `backend/` directory or using the start scripts
2. Install dependencies: `pip install -r requirements.txt`
3. Check that `src/` and `data/` folders exist in `backend/`

## Dependencies

Install all dependencies:
```powershell
cd backend
pip install -r requirements.txt
```

Key backend dependencies:
- flask, flask-cors, PyJWT
- pandas, numpy, scikit-learn
- nltk, textblob, vaderSentiment
- gensim (for LDA topic modeling)
- networkx (for knowledge graphs)
- transformers (for BERT sentiment)
- matplotlib, seaborn, plotly, wordcloud

