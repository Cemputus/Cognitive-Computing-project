# Cognitive Computing - Business Intelligence Analyst

A comprehensive cognitive computing system for small business intelligence analysis, focusing on sentiment analysis and market trends from customer reviews and social media posts.

## 📋 Project Overview

This project implements a cognitive computing system with four core pillars:
- **Understand**: Sentiment analysis and text understanding
- **Reason**: Topic modeling, knowledge graphs, and predictive analytics
- **Learn**: Active feedback loops and model improvement
- **Interact**: Modern React frontend with Flask backend API

## 🏗️ Project Structure

```
Cognitive Computing/
├── frontend/              # React frontend application
├── backend/               # Flask REST API
├── Cognitive Pillars/    # Jupyter notebooks (Milestones 1-5)
├── documentation/        # All project documentation
├── src/                  # Shared Python modules
├── data/                 # Data storage (raw, processed, models)
└── scripts/              # Utility scripts
```

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed structure.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Jupyter Notebook/Lab

### Installation

1. **Clone/Download the project**
   ```bash
   cd "D:\Cognitive Computing"
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r backend/requirements_backend.txt
   ```

3. **Install Frontend dependencies**
   ```bash
   cd frontend
   npm install
   ```

### Running the System

#### Start Backend Server
```bash
# Option 1: Use script (from project root)
scripts\start_backend.bat

# Option 2: Manual
cd backend
python backend_api.py
```
Backend will run on `http://localhost:5000`

#### Start Frontend
```bash
cd frontend
npm run dev
```
Frontend will run on `http://localhost:3000`

#### Run Notebooks
Open Jupyter Notebook/Lab and navigate to:
- `Cognitive Pillars/Milestone1/01_Data_Pipeline.ipynb` - Data collection and preprocessing
- `Cognitive Pillars/Milestone2/02_Understanding_Reasoning_Engine.ipynb` - Sentiment analysis and reasoning
- `Cognitive Pillars/Milestone3/03_Interactive_Prototype.ipynb` - Interactive prototype
- `Cognitive Pillars/Milestone4/04_Evaluation_Ethical_Review.ipynb` - Evaluation and ethics
- `Cognitive Pillars/Milestone5/05_Final_Documentation.ipynb` - Final documentation

## 👤 Login Credentials

### Admin Account
- **Email**: `admin@business.com`
- **Password**: `admin123`

### Regular Users (7 users)
- **Email**: `user1@business.com` through `user7@business.com`
- **Password**: `user123` (for all)

## 📚 Documentation

All documentation is in the `documentation/` folder:

- **Part A**: Problem Analysis, System Architecture, Implementation Plan
- **Part C**: System Evaluation, Ethical Analysis, Final Report, Presentation, User Manual
- **Guides**: Setup guides, implementation summaries, migration notes

## 🧠 Cognitive Pillars

### Milestone 1: Data Pipeline (Task B1)
- Data collection (synthetic + web scraping)
- Data cleaning and preprocessing
- Data validation and quality reports

### Milestone 2: Understanding & Reasoning (Task B2)
- Sentiment analysis (VADER, TextBlob, Ensemble)
- Topic modeling (LDA)
- Machine learning classification
- Knowledge graph construction
- Predictive modeling (trend forecasting)

### Milestone 3: Interactive Prototype (Task B3)
- React frontend with modern UI
- Flask REST API backend
- User authentication
- Real-time sentiment analysis
- Dashboard and visualizations

### Milestone 4: Evaluation & Ethics (Task C1, C2)
- System performance evaluation
- Ethical impact analysis
- Bias and fairness assessment

### Milestone 5: Final Documentation (Task C3)
- Project statistics
- Final visualizations
- Documentation checklist

## 🛠️ Technology Stack

### Backend
- Flask (REST API)
- PyJWT (Authentication)
- Pandas, NumPy (Data processing)
- scikit-learn (ML models)
- Gensim (Topic modeling)
- NetworkX (Knowledge graphs)

### Frontend
- React 18
- Material-UI (MUI)
- Framer Motion (Animations)
- React Icons
- Axios (API calls)
- Recharts (Visualizations)

### Data Science
- NLTK, spaCy (NLP)
- VADER, TextBlob (Sentiment)
- Transformers (BERT)
- Gensim (LDA)
- NetworkX (Graphs)
- Matplotlib, Seaborn, Plotly (Visualization)

## 📊 Features

- **Sentiment Analysis**: Multi-method ensemble with confidence scoring
- **Topic Modeling**: LDA-based topic extraction
- **Knowledge Graphs**: Dynamic entity and relationship extraction
- **Predictive Analytics**: Trend forecasting (ARIMA, Moving Average)
- **Interactive Dashboard**: Real-time insights and visualizations
- **User Authentication**: JWT-based secure authentication
- **Modern UI**: Responsive design with animations

## 📁 Key Files

- `backend/backend_api.py` - Main Flask API
- `backend/auth.py` - Authentication module
- `src/models/sentiment_analyzer.py` - Sentiment analysis engine
- `src/models/cognitive_agent.py` - Cognitive agent orchestrator
- `frontend/src/App.jsx` - Main React app
- `Cognitive Pillars/Milestone*/` - Jupyter notebooks

## 🔧 Development

### Adding New Features
- **Backend**: Add endpoints in `backend/backend_api.py`
- **Frontend**: Add components in `frontend/src/components/` or pages in `frontend/src/pages/`
- **Models**: Add new models in `src/models/`
- **Utils**: Add utilities in `src/utils/`

### Testing
- Backend: Test API endpoints with curl or Postman
- Frontend: Test in browser at `http://localhost:3000`
- Notebooks: Run cells sequentially in Jupyter

## 📝 License

This project is for educational purposes as part of the Cognitive Computing course.

## 👥 Authors

Developed for DSC3112 Cognitive Computing - Project-Based Learning

---

For detailed information, see the [documentation](documentation/) folder and [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md).
