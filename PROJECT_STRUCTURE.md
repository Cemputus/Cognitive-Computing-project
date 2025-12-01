# Project Structure

This document describes the reorganized project structure for the Cognitive Computing Business Intelligence Analyst project.

## 📁 Folder Organization

```
Cognitive Computing/
├── frontend/                    # React frontend application
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── pages/              # Page components
│   │   ├── contexts/           # React contexts (Auth, etc.)
│   │   └── services/            # API services
│   ├── package.json
│   └── vite.config.js
│
├── backend/                     # Flask backend API
│   ├── backend_api.py           # Main Flask application
│   ├── auth.py                 # Authentication module
│   ├── app.py                  # Alternative app entry (if exists)
│   └── requirements_backend.txt
│
├── Cognitive Pillars/          # All notebooks and cognitive processing
│   ├── Milestone1/             # Data Pipeline (Task B1)
│   │   └── 01_Data_Pipeline.ipynb
│   ├── Milestone2/             # Understanding & Reasoning (Task B2)
│   │   └── 02_Understanding_Reasoning_Engine.ipynb
│   ├── Milestone3/             # Interactive Prototype (Task B3)
│   │   └── 03_Interactive_Prototype.ipynb
│   ├── Milestone4/             # Evaluation & Ethical Review (Task C1, C2)
│   │   └── 04_Evaluation_Ethical_Review.ipynb
│   ├── Milestone5/             # Final Documentation (Task C3)
│   │   └── 05_Final_Documentation.ipynb
│   └── evaluation/             # Additional evaluation materials
│
├── documentation/              # All project documentation
│   ├── PartA/                  # Part A deliverables
│   │   ├── 01_Problem_Analysis_Document.md
│   │   ├── 02_System_Architecture.md
│   │   └── 03_Implementation_Plan.md
│   ├── PartC/                  # Part C deliverables
│   │   ├── 01_System_Evaluation_Report.md
│   │   ├── 02_Ethical_Impact_Analysis.md
│   │   ├── 03_Final_Report.md
│   │   ├── 04_Presentation_Slides.md
│   │   └── 05_User_Manual.md
│   ├── DSC3112 COGNITIVE COMPUTING - Project-BaseBSDS BDS 3-1.pdf
│   └── [Various setup and guide markdown files]
│
├── src/                        # Core Python modules (shared by notebooks and backend)
│   ├── models/                 # ML models and cognitive components
│   │   ├── sentiment_analyzer.py
│   │   └── cognitive_agent.py
│   └── utils/                  # Utility functions
│       ├── text_preprocessor.py
│       ├── data_collector.py
│       ├── wordcloud_generator.py
│       └── robustness_validator.py
│
├── data/                       # Data storage
│   ├── raw/                    # Raw collected data
│   ├── processed/              # Processed/cleaned data
│   └── models/                 # Trained models and artifacts
│
├── scripts/                    # Helper scripts
│   ├── start_backend.bat       # Windows batch script to start backend
│   ├── start_backend.ps1       # PowerShell script to start backend
│   └── [Other utility scripts]
│
├── config/                     # Configuration files (if needed)
│
├── requirements.txt            # Python dependencies
└── README.md                   # Main project README
```

## 🎯 Key Changes

### 1. **Frontend** (`frontend/`)
- React application with modern UI
- All frontend code is self-contained here
- Run with: `cd frontend && npm run dev`

### 2. **Backend** (`backend/`)
- Flask REST API
- Authentication and business logic
- Run with: `cd backend && python backend_api.py`
- Or use scripts: `scripts/start_backend.bat` or `scripts/start_backend.ps1`

### 3. **Cognitive Pillars** (`Cognitive Pillars/`)
- All Jupyter notebooks organized by milestone
- Evaluation materials
- This is where all cognitive computing analysis happens

### 4. **Documentation** (`documentation/`)
- All markdown documentation files
- Part A and Part C deliverables
- Project requirements PDF
- Setup guides and summaries

### 5. **Source Code** (`src/`)
- Shared Python modules used by both notebooks and backend
- Models, utilities, and core functionality
- Imported as: `from src.models.sentiment_analyzer import SentimentAnalyzer`

### 6. **Data** (`data/`)
- Raw data: `data/raw/`
- Processed data: `data/processed/`
- Trained models: `data/models/`

### 7. **Scripts** (`scripts/`)
- Utility scripts for setup, testing, and running services
- Start scripts for backend

## 🔄 Import Paths

### In Backend Files
```python
from src.models.sentiment_analyzer import SentimentAnalyzer
from src.utils.text_preprocessor import TextPreprocessor
from backend.auth import authenticate_user
```

### In Notebooks
```python
import sys
sys.path.append('../..')  # Go up to project root
from src.models.sentiment_analyzer import SentimentAnalyzer
from src.utils.text_preprocessor import TextPreprocessor
```

### Data Files
All data files are referenced relative to project root:
- `data/raw/collected_reviews.csv`
- `data/processed/reviews_with_sentiment.csv`
- `data/models/knowledge_graph.pkl`

## 🚀 Quick Start

### Start Backend
```bash
# Option 1: Use script (from project root)
scripts\start_backend.bat

# Option 2: Manual
cd backend
python backend_api.py
```

### Start Frontend
```bash
cd frontend
npm run dev
```

### Run Notebooks
Open Jupyter Notebook/Lab and navigate to:
- `Cognitive Pillars/Milestone1/01_Data_Pipeline.ipynb`
- `Cognitive Pillars/Milestone2/02_Understanding_Reasoning_Engine.ipynb`
- etc.

## 📝 Notes

- The `src/` folder contains shared code used by both notebooks and backend
- Backend files are now in `backend/` instead of `src/api/`
- All notebooks are in `Cognitive Pillars/` organized by milestone
- All documentation is consolidated in `documentation/`
- Scripts are organized in `scripts/` for easy access

## 🔧 Maintenance

When adding new files:
- **Frontend code** → `frontend/`
- **Backend code** → `backend/`
- **Notebooks** → `Cognitive Pillars/[Milestone#]/`
- **Documentation** → `documentation/`
- **Shared Python modules** → `src/models/` or `src/utils/`
- **Data files** → `data/[raw|processed|models]/`
- **Scripts** → `scripts/`


