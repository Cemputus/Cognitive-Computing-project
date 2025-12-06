# 🧠 CENAnalytics - Cognitive Computing Business Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18.2-blue.svg)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-Educational-lightgrey.svg)](LICENSE)

A comprehensive cognitive computing system for small business intelligence analysis, focusing on sentiment analysis, topic modeling, and predictive analytics from customer reviews and social media posts. Built with React frontend and Flask backend, implementing the four core cognitive computing pillars: **Understand**, **Reason**, **Learn**, and **Interact**.

## 📋 Table of Contents

- [Features](#-features)
- [Project Overview](#-project-overview)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Authentication](#-authentication)
- [Features in Detail](#-features-in-detail)
- [Documentation](#-documentation)
- [Development](#-development)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### Core Capabilities

- 🔍 **Multi-Method Sentiment Analysis** - VADER, TextBlob, and Ensemble methods with confidence scoring
- 📊 **Interactive Dashboard** - Real-time analytics with dynamic visualizations
- 📈 **Predictive Analytics** - Trend forecasting using ARIMA and Moving Average models
- 🎯 **Topic Modeling** - LDA-based topic extraction and analysis
- 🗺️ **Knowledge Graphs** - Dynamic entity and relationship extraction
- 📧 **PDF Report Export** - Generate and download comprehensive analytics reports
- 🔔 **Notification System** - Real-time notifications for user actions
- 👥 **User Management** - Role-based authentication (Admin/User)
- 📱 **Responsive Design** - Modern UI with Material-UI components
- 🎨 **Data Visualizations** - Charts, graphs, word clouds, and interactive plots

### Advanced Features

- **Location-Based Analytics** - Sentiment analysis by geographic location
- **Platform Analytics** - Cross-platform sentiment comparison
- **Topic-Based Insights** - Deep dive into topic-specific sentiment trends
- **Email Integration** - Automated PDF report delivery to administrators
- **Active Learning** - Feedback loops for model improvement
- **Real-Time Processing** - Live sentiment analysis and batch processing

## 🎯 Project Overview

CENAnalytics implements a cognitive computing system designed to help small businesses understand customer sentiment, identify trends, and make data-driven decisions. The system processes customer reviews and social media posts through a sophisticated pipeline that includes:

1. **Data Collection & Preprocessing** - Automated data gathering and cleaning
2. **Sentiment Analysis** - Multi-method ensemble approach for accurate sentiment detection
3. **Topic Modeling** - Unsupervised topic discovery using LDA
4. **Knowledge Graph Construction** - Entity-relationship mapping
5. **Predictive Analytics** - Trend forecasting and pattern recognition
6. **Interactive Visualization** - User-friendly dashboards and reports

### Cognitive Computing Pillars

- **🧠 Understand**: Advanced NLP and sentiment analysis to comprehend customer feedback
- **💭 Reason**: Topic modeling, knowledge graphs, and predictive analytics for insights
- **📚 Learn**: Active feedback mechanisms and continuous model improvement
- **🤝 Interact**: Modern web interface with real-time analytics and reporting

## 🛠️ Technology Stack

### Backend

- **Framework**: Flask 2.3+ (REST API)
- **Authentication**: PyJWT (JWT tokens)
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: scikit-learn, Gensim (LDA)
- **NLP**: NLTK, TextBlob, VADER Sentiment, Transformers (BERT)
- **Graph Analytics**: NetworkX
- **PDF Generation**: ReportLab
- **Visualization**: Matplotlib, Seaborn, Plotly, WordCloud

### Frontend

- **Framework**: React 18.2
- **UI Library**: Material-UI (MUI) 5.15
- **Charts**: Recharts 2.10
- **Animations**: Framer Motion 10.16
- **HTTP Client**: Axios 1.6
- **Routing**: React Router DOM 6.20
- **Build Tool**: Vite 5.0

### Data Science

- **Notebooks**: Jupyter Notebook/Lab
- **Visualization**: Matplotlib, Seaborn, Plotly
- **Topic Modeling**: Gensim LDA
- **Graph Visualization**: NetworkX, Pyvis

## 📦 Installation

### Prerequisites

- **Python**: 3.8 or higher
- **Node.js**: 16.0 or higher
- **npm** or **yarn**: Latest version
- **Jupyter Notebook/Lab**: For running milestone notebooks
- **Git**: For version control

### Step 1: Clone the Repository

```bash
git clone <https://github.com/Cemputus/Cognitive-Computing-project>
cd "Cognitive Computing"
```

### Step 2: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data (first time only)
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('vader_lexicon')"
```

### Step 3: Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

## 🚀 Quick Start

### Data Setup (One-Time)

**Important**: After running Milestone 2 notebook once, you don't need to rerun it for normal frontend usage. The backend automatically uses saved data files.

1. **Run Milestone 2 Notebook** (one-time setup):
   ```bash
   # Open and run: Cognitive Pillars/Milestone2/02_Understanding_Reasoning_Engine.ipynb
   # This generates:
   # - backend/data/processed/reviews_with_sentiment.csv
   # - backend/data/models/lda_model/
   # - backend/data/models/forecast_results.json
   ```

2. **Verify Data Files** (optional):
   ```bash
   cd backend
   python scripts/verify_data.py
   ```
   
   This will show you which files are present and ready to use.

3. **Backend Behavior**:
   - ✅ Uses saved files when available (fast)
   - ✅ Generates missing data on-the-fly when needed (slower but works)
   - ✅ Saves generated forecasts for future use

**📖 For detailed workflow information, see [backend/DATA_WORKFLOW.md](backend/DATA_WORKFLOW.md)**

### Starting the Backend Server

**Option 1: Using the provided script (Windows)**

```powershell
# From project root
.\backend\scripts\start_backend.bat
```

**Option 2: Manual start**

```bash
cd backend
python backend_api.py
```

The backend will start on `http://localhost:5000`

### Starting the Frontend

```bash
cd frontend
npm run dev
```

The frontend will start on `http://localhost:5173` (Vite default port)

### Accessing the Application

1. Open your browser and navigate to `http://localhost:5173`
2. Login with the provided credentials (see [Authentication](#-authentication))
3. Explore the dashboard and analytics features

## 📁 Project Structure

```
Cognitive Computing/
├── backend/                    # Flask REST API backend
│   ├── backend_api.py         # Main API server
│   ├── auth.py                # Authentication module
│   ├── requirements.txt       # Python dependencies
│   ├── data/                  # Data storage
│   │   ├── raw/              # Raw collected data
│   │   ├── processed/        # Processed datasets
│   │   └── models/           # Trained models (pickle files)
│   ├── src/                   # Source modules
│   │   ├── models/           # ML models (sentiment, cognitive agent)
│   │   └── utils/            # Utilities (preprocessing, wordcloud)
│   └── scripts/              # Utility scripts
│
├── frontend/                   # React frontend application
│   ├── src/
│   │   ├── pages/            # Page components
│   │   │   ├── Dashboard.jsx
│   │   │   ├── SentimentAnalysis.jsx
│   │   │   ├── TopicAnalysis.jsx
│   │   │   ├── TrendsInsights.jsx
│   │   │   └── ...
│   │   ├── components/       # Reusable components
│   │   ├── contexts/        # React contexts (Auth, Notifications)
│   │   └── services/        # API service layer
│   ├── package.json
│   └── vite.config.js
│
├── Cognitive Pillars/          # Jupyter notebooks (Milestones)
│   ├── Milestone1/           # Data Pipeline
│   ├── Milestone2/           # Understanding & Reasoning
│   ├── Milestone3/           # Interactive Prototype
│   ├── Milestone4/           # Evaluation & Ethics
│   └── Milestone5/           # Final Documentation
│
├── documentation/              # Project documentation
│   ├── PartA/                # Problem Analysis, Architecture, Implementation
│   └── PartC/                # Evaluation, Ethics, Final Report
│
└── README.md                  # This file
```

## 🏗️ System Architecture

### High-Level Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              React Frontend (Port 5173)                   │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │  │
│  │  │  Pages   │ │Components│ │Contexts  │ │ Services │   │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘   │  │
│  │  - Dashboard  - Navbar     - Auth      - API Client    │  │
│  │  - Sentiment  - Charts     - Notify    - Axios         │  │
│  │  - Topics     - Cards                                   │  │
│  │  - Trends                                                │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────────┘
                               │ HTTP/REST (JSON)
                               │ JWT Authentication
┌──────────────────────────────▼──────────────────────────────────┐
│                      API GATEWAY LAYER                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         Flask REST API Server (Port 5000)                │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │          backend_api.py (Main Router)              │  │  │
│  │  │  - Route Handlers  - Middleware  - Error Handling │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │              auth.py (Security Layer)              │  │  │
│  │  │  - JWT Token Generation  - Token Verification      │  │  │
│  │  │  - User Authentication  - Role-Based Access        │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                  COGNITIVE PROCESSING LAYER                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ UNDERSTAND   │  │   REASON     │  │   LEARN      │        │
│  │   Pillar     │  │   Pillar     │  │   Pillar     │        │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤        │
│  │ - NLP        │  │ - Topic Model│  │ - Feedback   │        │
│  │ - Sentiment  │  │ - Knowledge  │  │ - Model      │        │
│  │   Analysis   │  │   Graph      │  │   Updates    │        │
│  │ - Text       │  │ - Predictive │  │ - Performance│        │
│  │   Preproc    │  │   Analytics  │  │   Tracking   │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Business Intelligence Agent                  │  │
│  │  - Orchestrates all cognitive processes                  │  │
│  │  - Manages data flow between pillars                     │  │
│  │  - Generates insights and responses                      │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                      DATA LAYER                                 │
│  ┌──────────────────┐  ┌──────────────────┐                   │
│  │   Data Storage   │  │  Model Storage   │                   │
│  ├──────────────────┤  ├──────────────────┤                   │
│  │ - Raw Data       │  │ - LDA Models     │                   │
│  │   (CSV)          │  │ - Knowledge      │                   │
│  │ - Processed Data │  │   Graphs (PKL)   │                   │
│  │   (CSV)          │  │ - Forecast Data  │                   │
│  │ - Review Data    │  │   (JSON)         │                   │
│  └──────────────────┘  └──────────────────┘                   │
└─────────────────────────────────────────────────────────────────┘
```

### Frontend Architecture

#### Component Hierarchy

```
App (Root)
├── AuthProvider (Context)
│   ├── NotificationProvider (Context)
│   │   └── AppRoutes
│   │       ├── LandingPage (Public)
│   │       ├── Login (Public)
│   │       └── Protected Routes
│   │           ├── Dashboard
│   │           │   ├── StatCards
│   │           │   ├── Charts (Recharts)
│   │           │   ├── Filters
│   │           │   └── DataTables
│   │           ├── SentimentAnalysis
│   │           │   ├── TextInput
│   │           │   ├── MethodSelector
│   │           │   ├── ResultsDisplay
│   │           │   ├── RadialChart
│   │           │   └── HistoryPanel
│   │           ├── TopicAnalysis
│   │           │   ├── TopicCards
│   │           │   ├── BarChart
│   │           │   └── KeywordDisplay
│   │           ├── TrendsInsights
│   │           │   ├── ForecastChart
│   │           │   ├── PeriodSelector
│   │           │   └── InsightsPanel
│   │           ├── Profile
│   │           ├── Notifications
│   │           └── About
│   └── Navbar (Global Component)
```

#### State Management

- **AuthContext**: User authentication state, JWT token management
- **NotificationContext**: Real-time notifications, unread counts
- **Local State**: Component-level state using React Hooks (`useState`, `useEffect`)
- **LocalStorage**: Persistent user preferences, sentiment history per user

#### Routing Architecture

- **React Router DOM v6**: Client-side routing
- **Protected Routes**: Authentication-gated routes using `ProtectedRoute` component
- **Public Routes**: Landing page, Login, About
- **Route Guards**: Automatic redirect to login for unauthenticated users

### Backend Architecture

#### API Server Structure

```
backend_api.py (Flask Application)
├── Initialization
│   ├── Flask App Setup
│   ├── CORS Configuration
│   ├── Component Initialization
│   │   ├── SentimentAnalyzer
│   │   ├── TextPreprocessor
│   │   ├── BusinessIntelligenceAgent
│   │   └── Knowledge Graph (optional)
│   └── Data Loading
│       └── df_reviews (Global DataFrame)
│
├── Authentication Middleware
│   └── @token_required decorator
│
├── API Routes
│   ├── /api/auth/* (Authentication)
│   ├── /api/sentiment/* (Sentiment Analysis)
│   ├── /api/topics (Topic Modeling)
│   ├── /api/forecast (Predictive Analytics)
│   ├── /api/dashboard/* (Dashboard Stats)
│   ├── /api/analytics/* (Advanced Analytics)
│   ├── /api/export/* (Report Generation)
│   └── /api/notifications/* (Notification System)
│
└── Helper Functions
    ├── generate_topic_name()
    ├── predict_topic_for_text()
    ├── generate_forecast_from_reviews()
    ├── extend_or_sample_forecast()
    ├── aggregate_to_monthly()
    └── filter_forecast_by_indices()
```

#### Core Modules

**1. Sentiment Analysis Module** (`src/models/sentiment_analyzer.py`)

```
SentimentAnalyzer
├── __init__(method, use_ensemble)
├── analyze_vader(text)
│   └── Returns: {sentiment, pos, neu, neg, compound, confidence}
├── analyze_textblob(text)
│   └── Returns: {sentiment, pos, neu, neg, compound, confidence}
├── analyze_transformer(text)
│   └── Returns: {sentiment, pos, neu, neg, compound, confidence}
├── analyze_ensemble(text)
│   └── Combines methods → weighted average
└── analyze(text) [Main Entry Point]
```

**2. Cognitive Agent** (`src/models/cognitive_agent.py`)

```
BusinessIntelligenceAgent
├── __init__(analyzer, preprocessor, knowledge_graph)
├── process_query(user_input)
│   ├── Text Preprocessing
│   ├── Sentiment Analysis
│   ├── Insight Extraction
│   ├── Knowledge Graph Query
│   └── Response Generation
├── batch_process(texts)
├── collect_feedback(query_id, feedback)
└── get_learning_stats()
```

**3. Text Preprocessing** (`src/utils/text_preprocessor.py`)

```
TextPreprocessor
├── clean_text(text)
├── tokenize(text)
├── remove_stopwords(tokens)
└── lemmatize(tokens)
```

**4. Topic Prediction** (`backend_api.py`)

```
predict_topic_for_text(text)
├── Load LDA Model
├── Preprocess Text
├── Create Document Representation
├── Get Topic Distribution
└── Return: {topic_id, topic_name, confidence}
```

**5. Forecast Generation** (`backend_api.py`)

```
generate_forecast_from_reviews(df_reviews, forecast_days)
├── Load/Sample Review Data
├── Analyze Sentiment (if needed)
├── Calculate Daily Sentiment Ratios
├── Generate Forecasts:
│   ├── Moving Average (7-day window)
│   ├── Linear Trend (polynomial regression)
│   └── ARIMA (auto-regressive)
└── Return: {forecast_dates, ma_forecast, trend_forecast, arima_forecast}
```

### Data Flow Architecture

#### Request Flow (Sentiment Analysis Example)

```
1. User Input (Frontend)
   └──> User types text in SentimentAnalysis component
   
2. Frontend Processing
   └──> apiService.analyzeSentiment(text, method)
       └──> Axios POST /api/sentiment/analyze
           └──> JWT Token in Authorization header
   
3. Backend Processing
   └──> backend_api.py: /api/sentiment/analyze
       ├──> @token_required middleware
       │   └──> Verify JWT token
       ├──> Extract text and method from request
       ├──> SentimentAnalyzer.analyze(text, method)
       │   ├──> Text Preprocessing
       │   ├──> Method-specific analysis
       │   └──> Return sentiment scores
       ├──> predict_topic_for_text(text)
       │   ├──> Load LDA model
       │   ├──> Predict topic
       │   └──> Generate topic name
       └──> Return JSON response
   
4. Response Processing (Frontend)
   └──> Update component state
       ├──> Display sentiment results
       ├──> Show topic information
       ├──> Render charts
       └──> Save to history (localStorage)
```

#### Data Processing Pipeline

```
Raw Reviews (CSV)
    │
    ▼
[Data Loading] (Milestone 1)
    │
    ▼
[Text Preprocessing]
    │ - Cleaning
    │ - Tokenization
    │ - Stopword removal
    │
    ▼
[Sentiment Analysis] ←─── UNDERSTAND Pillar
    │ - VADER
    │ - TextBlob
    │ - Transformer (optional)
    │ - Ensemble
    │
    ▼
[Topic Prediction] ←─── REASON Pillar
    │ - LDA Model
    │ - Topic Assignment
    │ - Topic Naming
    │
    ▼
[Knowledge Graph] ←─── REASON Pillar (optional)
    │ - Entity Extraction
    │ - Relationship Mapping
    │
    ▼
[Forecast Generation] ←─── REASON Pillar
    │ - Daily Aggregation
    │ - Trend Analysis
    │ - Predictive Models
    │
    ▼
[Response Formatting] ←─── INTERACT Pillar
    │ - JSON Structure
    │ - Metadata
    │
    ▼
Frontend Display
```

### Component Interaction Diagram

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   React     │ HTTP    │   Flask     │ Python  │   Models    │
│  Frontend   │────────▶│   Backend   │────────▶│   Layer     │
│             │◀────────│             │◀────────│             │
└─────────────┘ JSON    └─────────────┘ Results └─────────────┘
     │                        │                       │
     │                        │                       │
     ▼                        ▼                       ▼
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│  Components │         │   Routes    │         │  Analytics  │
│  & Pages    │         │  & Handlers │         │  Functions  │
└─────────────┘         └─────────────┘         └─────────────┘
     │                        │                       │
     │                        │                       │
     ▼                        ▼                       ▼
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Context   │         │  Middleware │         │   Storage   │
│  Providers  │         │  (Auth)     │         │   (Files)   │
└─────────────┘         └─────────────┘         └─────────────┘
```

### Technology Stack Layers

#### Presentation Layer (Frontend)

- **Framework**: React 18.2 (Component-based UI)
- **UI Library**: Material-UI 5.15 (Design System)
- **Charts**: Recharts 2.10 (Data Visualization)
- **Animations**: Framer Motion 10.16 (UI Animations)
- **Routing**: React Router DOM 6.20 (Navigation)
- **HTTP Client**: Axios 1.6 (API Communication)
- **Build Tool**: Vite 5.0 (Fast Development)

#### Application Layer (Backend)

- **Framework**: Flask 2.3+ (Web Framework)
- **Authentication**: PyJWT 2.9+ (JWT Tokens)
- **CORS**: Flask-CORS 5.0 (Cross-Origin Support)
- **API Design**: RESTful (JSON Responses)

#### Business Logic Layer

- **NLP**: NLTK, TextBlob, VADER Sentiment
- **ML**: scikit-learn, Gensim (LDA)
- **Advanced NLP**: Transformers (BERT, optional)
- **Graph Analytics**: NetworkX

#### Data Processing Layer

- **Data Manipulation**: Pandas, NumPy
- **Text Processing**: Custom preprocessing modules
- **Time Series**: NumPy, Pandas (for forecasting)

#### Data Persistence Layer

- **File Storage**: CSV files (raw/processed data)
- **Model Storage**: Pickle files (.pkl)
- **Forecast Storage**: JSON files
- **Local Storage**: Browser localStorage (frontend)

### Security Architecture

```
┌─────────────────────────────────────────┐
│         Security Layers                 │
├─────────────────────────────────────────┤
│ 1. Authentication (JWT)                 │
│    - Token-based auth                   │
│    - Token expiration (24h)             │
│    - Secure token storage (localStorage)│
├─────────────────────────────────────────┤
│ 2. Authorization                        │
│    - Role-based access (Admin/User)     │
│    - Protected routes                   │
│    - API endpoint guards                │
├─────────────────────────────────────────┤
│ 3. Input Validation                     │
│    - Text input validation              │
│    - Robustness validator               │
│    - Error handling                     │
├─────────────────────────────────────────┤
│ 4. CORS Protection                      │
│    - Configured origins                 │
│    - Credential support                 │
└─────────────────────────────────────────┘
```

### Cognitive Computing Pillars Implementation

#### 🧠 UNDERSTAND Pillar

- **Location**: `src/models/sentiment_analyzer.py`, `src/utils/text_preprocessor.py`
- **Functions**:
  - Text preprocessing and cleaning
  - Sentiment analysis (multi-method)
  - Entity extraction
  - Topic prediction for text

#### 💭 REASON Pillar

- **Location**: `backend_api.py`, `src/models/cognitive_agent.py`
- **Functions**:
  - Topic modeling (LDA)
  - Knowledge graph queries
  - Predictive analytics (forecasting)
  - Insight generation

#### 📚 LEARN Pillar

- **Location**: `src/models/cognitive_agent.py`
- **Functions**:
  - Feedback collection
  - Performance tracking
  - Model improvement suggestions

#### 🤝 INTERACT Pillar

- **Location**: Frontend components, `backend_api.py` response formatting
- **Functions**:
  - User interface rendering
  - Response generation
  - Visualization creation
  - Report generation

### Deployment Architecture

#### Development Environment

```
Developer Machine
├── Backend (Flask)
│   └── Runs on: http://localhost:5000
├── Frontend (Vite Dev Server)
│   └── Runs on: http://localhost:5173
└── Data Storage
    └── Local file system
```

#### Production Considerations

- **Backend**: Can be deployed on cloud platforms (AWS, Azure, GCP)
- **Frontend**: Static build can be hosted on CDN or web server
- **Database**: Currently file-based; can migrate to PostgreSQL/MySQL
- **Model Storage**: Consider cloud storage (S3, Azure Blob)
- **Caching**: Redis for session management and API caching
- **Load Balancing**: Multiple backend instances for scalability

---

## 📡 API Documentation

### Base URL

```
http://localhost:5000/api
```

### Authentication Endpoints

| Method | Endpoint            | Description                | Auth Required |
| ------ | ------------------- | -------------------------- | ------------- |
| POST   | `/api/auth/login` | User login                 | No            |
| GET    | `/api/auth/me`    | Get current user info      | Yes           |
| GET    | `/api/auth/users` | Get all users (admin only) | Yes           |

### Analytics Endpoints

| Method | Endpoint                              | Description                | Auth Required |
| ------ | ------------------------------------- | -------------------------- | ------------- |
| POST   | `/api/sentiment/analyze`            | Analyze single text        | Yes           |
| POST   | `/api/sentiment/batch`              | Batch sentiment analysis   | Yes           |
| GET    | `/api/topics`                       | Get topic modeling results | Yes           |
| GET    | `/api/forecast`                     | Get trend forecasts        | Yes           |
| GET    | `/api/dashboard/stats`              | Get dashboard statistics   | Yes           |
| GET    | `/api/analytics/location-sentiment` | Location-based analytics   | Yes           |
| GET    | `/api/analytics/platform-sentiment` | Platform-based analytics   | Yes           |
| GET    | `/api/analytics/topic-sentiment`    | Topic-based analytics      | Yes           |

### Report & Export

| Method | Endpoint               | Description       | Auth Required |
| ------ | ---------------------- | ----------------- | ------------- |
| POST   | `/api/export/report` | Export PDF report | Yes           |

### Other Endpoints

| Method | Endpoint                         | Description               | Auth Required |
| ------ | -------------------------------- | ------------------------- | ------------- |
| GET    | `/api/health`                  | Health check              | No            |
| POST   | `/api/feedback`                | Submit feedback           | Yes           |
| GET    | `/api/learning/stats`          | Learning statistics       | Yes           |
| POST   | `/api/contact-admin`           | Contact administrator     | Yes           |
| GET    | `/api/notifications`           | Get notifications         | Yes           |
| POST   | `/api/notifications/mark-read` | Mark notification as read | Yes           |

For detailed API documentation, see [backend/README.md](backend/README.md)

## 🔐 Authentication

### Default Login Credentials

#### Admin Account

- **Email**: `admin@business.com`
- **Password**: `admin123`
- **Role**: Administrator (full access)

#### Regular User Accounts

- **Email**: `user1@business.com` through `user7@business.com`
- **Password**: `user123` (for all users)
- **Role**: User (standard access)

### Authentication Flow

1. User submits login credentials via `/api/auth/login`
2. Backend validates credentials and returns JWT token
3. Frontend stores token in localStorage
4. Token is included in `Authorization: Bearer <token>` header for protected routes
5. Token expires after 24 hours (configurable)

## 🎨 Features in Detail

### 1. Sentiment Analysis

- **Single Text Analysis**: Real-time sentiment analysis for individual texts
- **Batch Processing**: Analyze multiple texts simultaneously
- **Multi-Method Ensemble**: Combines VADER, TextBlob, and BERT for accuracy
- **Confidence Scoring**: Provides confidence levels for each prediction

### 2. Dashboard

- **Overview Statistics**: Total reviews, sentiment distribution
- **Interactive Charts**: Bar charts, pie charts, line graphs
- **Real-Time Updates**: Live data refresh capabilities
- **Filter Options**: Filter by date range, location, platform

### 3. Topic Analysis

- **LDA Topic Modeling**: Discover hidden topics in reviews
- **Topic Visualization**: Word clouds and topic distribution charts
- **Topic-Sentiment Mapping**: Understand sentiment per topic

### 4. Trends & Insights

- **Forecast Visualization**: Predictive trend charts
- **Historical Analysis**: Time-series sentiment trends
- **Pattern Recognition**: Identify recurring patterns

### 5. Report Export

- **PDF Generation**: Comprehensive analytics reports in PDF format
- **Automatic Email**: Reports automatically sent to administrator
- **Download Option**: Users can download reports directly

### 6. Notifications

- **Real-Time Alerts**: System notifications for important events
- **User-Specific**: Personalized notification feed
- **Mark as Read**: Notification management

## 📚 Documentation

Comprehensive documentation is available in the `documentation/` folder:

### Part A: System Design

- `01_Problem_Analysis_Document.md` - Problem statement and requirements
- `02_System_Architecture.md` - System architecture and design
- `03_Implementation_Plan.md` - Implementation roadmap

### Part C: Evaluation & Final Report

- `01_System_Evaluation_Report.md` - Performance evaluation
- `02_Ethical_Impact_Analysis.md` - Ethical considerations
- `03_Final_Report.md` - Comprehensive project report
- `04_Presentation_Slides.md` - Presentation materials
- `05_User_Manual.md` - User guide

### Additional Guides

- `BACKEND_SETUP.md` - Backend setup instructions
- `AUTHENTICATION_SETUP.md` - Authentication configuration
- `DATA_COLLECTION_GUIDE.md` - Data collection process

## 🛠️ Development

### Adding New Features

#### Backend

1. Add new endpoints in `backend/backend_api.py`
2. Create models in `backend/src/models/` if needed
3. Add utilities in `backend/src/utils/` if needed
4. Update `requirements.txt` if new packages are required

#### Frontend

1. Create new pages in `frontend/src/pages/`
2. Add reusable components in `frontend/src/components/`
3. Update routing in `frontend/src/App.jsx`
4. Add API calls in `frontend/src/services/api.js`

### Running Tests

```bash
# Backend tests (if available)
cd backend
python -m pytest tests/

# Frontend tests (if available)
cd frontend
npm test
```

### Code Style

- **Python**: Follow PEP 8 guidelines
- **JavaScript**: Follow ESLint configuration
- **React**: Use functional components with hooks

## 🧪 Running Milestone Notebooks

The project includes Jupyter notebooks for each milestone:

1. **Milestone 1**: Data Pipeline (`Cognitive Pillars/Milestone1/01_Data_Pipeline.ipynb`)

   - Data collection and preprocessing
   - Data validation and quality reports
2. **Milestone 2**: Understanding & Reasoning (`Cognitive Pillars/Milestone2/02_Understanding_Reasoning_Engine.ipynb`)

   - Sentiment analysis implementation
   - Topic modeling with LDA
   - Knowledge graph construction
3. **Milestone 3**: Interactive Prototype (`Cognitive Pillars/Milestone3/03_Interactive_Prototype.ipynb`)

   - Frontend-backend integration
   - API testing
4. **Milestone 4**: Evaluation & Ethics (`Cognitive Pillars/Milestone4/04_Evaluation_Ethical_Review.ipynb`)

   - System performance evaluation
   - Ethical impact analysis
5. **Milestone 5**: Final Documentation (`Cognitive Pillars/Milestone5/05_Final_Documentation.ipynb`)

   - Project statistics
   - Final visualizations

To run notebooks:

```bash
jupyter notebook
# or
jupyter lab
```

## 🐛 Troubleshooting

### Backend Issues

**ModuleNotFoundError**

```bash
# Ensure virtual environment is activated
cd backend
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate     # Linux/Mac

# Reinstall dependencies
pip install -r requirements.txt
```

**Port Already in Use**

```bash
# Change port in backend_api.py
app.run(host='0.0.0.0', port=5001)  # Use different port
```

### Frontend Issues

**npm install fails**

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**CORS Errors**

- Ensure backend CORS is configured correctly
- Check that backend is running on correct port

### Common Issues

1. **NLTK Data Missing**: Run `python -c "import nltk; nltk.download('all')"`
2. **Model Files Not Found**: Ensure models are trained and saved in `backend/data/models/`
3. **Email Not Sending**: Configure SMTP settings in backend (see `send_email` function)

## 🤝 Contributing

This is an educational project for the Cognitive Computing course. If you'd like to contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👥 Authors

Emmanuel Nsubuga [https://github.com/Cemputus] Developed for **DSC3112 Cognitive Computing** - Project-Based Learning

## 🙏 Acknowledgments

- **NLTK** - Natural Language Toolkit
- **Material-UI** - React component library
- **Flask** - Python web framework
- **React** - JavaScript library for building user interfaces
- **Gensim** - Topic modeling library
- **NetworkX** - Graph analysis library

## 📞 Support

For issues, questions, or contributions, please open an issue on the GitHub repository.

---

**Built for Cognitive Computing(Academic Reasons)**

   # - backend/data/models/forecast_results.json
   ```

2. **Verify Data Files** (optional):
   ```bash
   cd backend
   python scripts/verify_data.py
   ```
   
   This will show you which files are present and ready to use.

3. **Backend Behavior**:
   - ✅ Uses saved files when available (fast)
   - ✅ Generates missing data on-the-fly when needed (slower but works)
   - ✅ Saves generated forecasts for future use

**📖 For detailed workflow information, see [backend/DATA_WORKFLOW.md](backend/DATA_WORKFLOW.md)**

### Starting the Backend Server

**Option 1: Using the provided script (Windows)**

```powershell
# From project root
.\backend\scripts\start_backend.bat
```

**Option 2: Manual start**

```bash
cd backend
python backend_api.py
```

The backend will start on `http://localhost:5000`

### Starting the Frontend

```bash
cd frontend
npm run dev
```

The frontend will start on `http://localhost:5173` (Vite default port)

### Accessing the Application

1. Open your browser and navigate to `http://localhost:5173`
2. Login with the provided credentials (see [Authentication](#-authentication))
3. Explore the dashboard and analytics features

## 📁 Project Structure

```
Cognitive Computing/
├── backend/                    # Flask REST API backend
│   ├── backend_api.py         # Main API server
│   ├── auth.py                # Authentication module
│   ├── requirements.txt       # Python dependencies
│   ├── data/                  # Data storage
│   │   ├── raw/              # Raw collected data
│   │   ├── processed/        # Processed datasets
│   │   └── models/           # Trained models (pickle files)
│   ├── src/                   # Source modules
│   │   ├── models/           # ML models (sentiment, cognitive agent)
│   │   └── utils/            # Utilities (preprocessing, wordcloud)
│   └── scripts/              # Utility scripts
│
├── frontend/                   # React frontend application
│   ├── src/
│   │   ├── pages/            # Page components
│   │   │   ├── Dashboard.jsx
│   │   │   ├── SentimentAnalysis.jsx
│   │   │   ├── TopicAnalysis.jsx
│   │   │   ├── TrendsInsights.jsx
│   │   │   └── ...
│   │   ├── components/       # Reusable components
│   │   ├── contexts/        # React contexts (Auth, Notifications)
│   │   └── services/        # API service layer
│   ├── package.json
│   └── vite.config.js
│
├── Cognitive Pillars/          # Jupyter notebooks (Milestones)
│   ├── Milestone1/           # Data Pipeline
│   ├── Milestone2/           # Understanding & Reasoning
│   ├── Milestone3/           # Interactive Prototype
│   ├── Milestone4/           # Evaluation & Ethics
│   └── Milestone5/           # Final Documentation
│
├── documentation/              # Project documentation
│   ├── PartA/                # Problem Analysis, Architecture, Implementation
│   └── PartC/                # Evaluation, Ethics, Final Report
│
└── README.md                  # This file
```

## 🏗️ System Architecture

### High-Level Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              React Frontend (Port 5173)                   │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │  │
│  │  │  Pages   │ │Components│ │Contexts  │ │ Services │   │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘   │  │
│  │  - Dashboard  - Navbar     - Auth      - API Client    │  │
│  │  - Sentiment  - Charts     - Notify    - Axios         │  │
│  │  - Topics     - Cards                                   │  │
│  │  - Trends                                                │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────────┘
                               │ HTTP/REST (JSON)
                               │ JWT Authentication
┌──────────────────────────────▼──────────────────────────────────┐
│                      API GATEWAY LAYER                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         Flask REST API Server (Port 5000)                │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │          backend_api.py (Main Router)              │  │  │
│  │  │  - Route Handlers  - Middleware  - Error Handling │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │              auth.py (Security Layer)              │  │  │
│  │  │  - JWT Token Generation  - Token Verification      │  │  │
│  │  │  - User Authentication  - Role-Based Access        │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                  COGNITIVE PROCESSING LAYER                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ UNDERSTAND   │  │   REASON     │  │   LEARN      │        │
│  │   Pillar     │  │   Pillar     │  │   Pillar     │        │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤        │
│  │ - NLP        │  │ - Topic Model│  │ - Feedback   │        │
│  │ - Sentiment  │  │ - Knowledge  │  │ - Model      │        │
│  │   Analysis   │  │   Graph      │  │   Updates    │        │
│  │ - Text       │  │ - Predictive │  │ - Performance│        │
│  │   Preproc    │  │   Analytics  │  │   Tracking   │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Business Intelligence Agent                  │  │
│  │  - Orchestrates all cognitive processes                  │  │
│  │  - Manages data flow between pillars                     │  │
│  │  - Generates insights and responses                      │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                      DATA LAYER                                 │
│  ┌──────────────────┐  ┌──────────────────┐                   │
│  │   Data Storage   │  │  Model Storage   │                   │
│  ├──────────────────┤  ├──────────────────┤                   │
│  │ - Raw Data       │  │ - LDA Models     │                   │
│  │   (CSV)          │  │ - Knowledge      │                   │
│  │ - Processed Data │  │   Graphs (PKL)   │                   │
│  │   (CSV)          │  │ - Forecast Data  │                   │
│  │ - Review Data    │  │   (JSON)         │                   │
│  └──────────────────┘  └──────────────────┘                   │
└─────────────────────────────────────────────────────────────────┘
```

### Frontend Architecture

#### Component Hierarchy

```
App (Root)
├── AuthProvider (Context)
│   ├── NotificationProvider (Context)
│   │   └── AppRoutes
│   │       ├── LandingPage (Public)
│   │       ├── Login (Public)
│   │       └── Protected Routes
│   │           ├── Dashboard
│   │           │   ├── StatCards
│   │           │   ├── Charts (Recharts)
│   │           │   ├── Filters
│   │           │   └── DataTables
│   │           ├── SentimentAnalysis
│   │           │   ├── TextInput
│   │           │   ├── MethodSelector
│   │           │   ├── ResultsDisplay
│   │           │   ├── RadialChart
│   │           │   └── HistoryPanel
│   │           ├── TopicAnalysis
│   │           │   ├── TopicCards
│   │           │   ├── BarChart
│   │           │   └── KeywordDisplay
│   │           ├── TrendsInsights
│   │           │   ├── ForecastChart
│   │           │   ├── PeriodSelector
│   │           │   └── InsightsPanel
│   │           ├── Profile
│   │           ├── Notifications
│   │           └── About
│   └── Navbar (Global Component)
```

#### State Management

- **AuthContext**: User authentication state, JWT token management
- **NotificationContext**: Real-time notifications, unread counts
- **Local State**: Component-level state using React Hooks (`useState`, `useEffect`)
- **LocalStorage**: Persistent user preferences, sentiment history per user

#### Routing Architecture

- **React Router DOM v6**: Client-side routing
- **Protected Routes**: Authentication-gated routes using `ProtectedRoute` component
- **Public Routes**: Landing page, Login, About
- **Route Guards**: Automatic redirect to login for unauthenticated users

### Backend Architecture

#### API Server Structure

```
backend_api.py (Flask Application)
├── Initialization
│   ├── Flask App Setup
│   ├── CORS Configuration
│   ├── Component Initialization
│   │   ├── SentimentAnalyzer
│   │   ├── TextPreprocessor
│   │   ├── BusinessIntelligenceAgent
│   │   └── Knowledge Graph (optional)
│   └── Data Loading
│       └── df_reviews (Global DataFrame)
│
├── Authentication Middleware
│   └── @token_required decorator
│
├── API Routes
│   ├── /api/auth/* (Authentication)
│   ├── /api/sentiment/* (Sentiment Analysis)
│   ├── /api/topics (Topic Modeling)
│   ├── /api/forecast (Predictive Analytics)
│   ├── /api/dashboard/* (Dashboard Stats)
│   ├── /api/analytics/* (Advanced Analytics)
│   ├── /api/export/* (Report Generation)
│   └── /api/notifications/* (Notification System)
│
└── Helper Functions
    ├── generate_topic_name()
    ├── predict_topic_for_text()
    ├── generate_forecast_from_reviews()
    ├── extend_or_sample_forecast()
    ├── aggregate_to_monthly()
    └── filter_forecast_by_indices()
```

#### Core Modules

**1. Sentiment Analysis Module** (`src/models/sentiment_analyzer.py`)

```
SentimentAnalyzer
├── __init__(method, use_ensemble)
├── analyze_vader(text)
│   └── Returns: {sentiment, pos, neu, neg, compound, confidence}
├── analyze_textblob(text)
│   └── Returns: {sentiment, pos, neu, neg, compound, confidence}
├── analyze_transformer(text)
│   └── Returns: {sentiment, pos, neu, neg, compound, confidence}
├── analyze_ensemble(text)
│   └── Combines methods → weighted average
└── analyze(text) [Main Entry Point]
```

**2. Cognitive Agent** (`src/models/cognitive_agent.py`)

```
BusinessIntelligenceAgent
├── __init__(analyzer, preprocessor, knowledge_graph)
├── process_query(user_input)
│   ├── Text Preprocessing
│   ├── Sentiment Analysis
│   ├── Insight Extraction
│   ├── Knowledge Graph Query
│   └── Response Generation
├── batch_process(texts)
├── collect_feedback(query_id, feedback)
└── get_learning_stats()
```

**3. Text Preprocessing** (`src/utils/text_preprocessor.py`)

```
TextPreprocessor
├── clean_text(text)
├── tokenize(text)
├── remove_stopwords(tokens)
└── lemmatize(tokens)
```

**4. Topic Prediction** (`backend_api.py`)

```
predict_topic_for_text(text)
├── Load LDA Model
├── Preprocess Text
├── Create Document Representation
├── Get Topic Distribution
└── Return: {topic_id, topic_name, confidence}
```

**5. Forecast Generation** (`backend_api.py`)

```
generate_forecast_from_reviews(df_reviews, forecast_days)
├── Load/Sample Review Data
├── Analyze Sentiment (if needed)
├── Calculate Daily Sentiment Ratios
├── Generate Forecasts:
│   ├── Moving Average (7-day window)
│   ├── Linear Trend (polynomial regression)
│   └── ARIMA (auto-regressive)
└── Return: {forecast_dates, ma_forecast, trend_forecast, arima_forecast}
```

### Data Flow Architecture

#### Request Flow (Sentiment Analysis Example)

```
1. User Input (Frontend)
   └──> User types text in SentimentAnalysis component
   
2. Frontend Processing
   └──> apiService.analyzeSentiment(text, method)
       └──> Axios POST /api/sentiment/analyze
           └──> JWT Token in Authorization header
   
3. Backend Processing
   └──> backend_api.py: /api/sentiment/analyze
       ├──> @token_required middleware
       │   └──> Verify JWT token
       ├──> Extract text and method from request
       ├──> SentimentAnalyzer.analyze(text, method)
       │   ├──> Text Preprocessing
       │   ├──> Method-specific analysis
       │   └──> Return sentiment scores
       ├──> predict_topic_for_text(text)
       │   ├──> Load LDA model
       │   ├──> Predict topic
       │   └──> Generate topic name
       └──> Return JSON response
   
4. Response Processing (Frontend)
   └──> Update component state
       ├──> Display sentiment results
       ├──> Show topic information
       ├──> Render charts
       └──> Save to history (localStorage)
```

#### Data Processing Pipeline

```
Raw Reviews (CSV)
    │
    ▼
[Data Loading] (Milestone 1)
    │
    ▼
[Text Preprocessing]
    │ - Cleaning
    │ - Tokenization
    │ - Stopword removal
    │
    ▼
[Sentiment Analysis] ←─── UNDERSTAND Pillar
    │ - VADER
    │ - TextBlob
    │ - Transformer (optional)
    │ - Ensemble
    │
    ▼
[Topic Prediction] ←─── REASON Pillar
    │ - LDA Model
    │ - Topic Assignment
    │ - Topic Naming
    │
    ▼
[Knowledge Graph] ←─── REASON Pillar (optional)
    │ - Entity Extraction
    │ - Relationship Mapping
    │
    ▼
[Forecast Generation] ←─── REASON Pillar
    │ - Daily Aggregation
    │ - Trend Analysis
    │ - Predictive Models
    │
    ▼
[Response Formatting] ←─── INTERACT Pillar
    │ - JSON Structure
    │ - Metadata
    │
    ▼
Frontend Display
```

### Component Interaction Diagram

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   React     │ HTTP    │   Flask     │ Python  │   Models    │
│  Frontend   │────────▶│   Backend   │────────▶│   Layer     │
│             │◀────────│             │◀────────│             │
└─────────────┘ JSON    └─────────────┘ Results └─────────────┘
     │                        │                       │
     │                        │                       │
     ▼                        ▼                       ▼
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│  Components │         │   Routes    │         │  Analytics  │
│  & Pages    │         │  & Handlers │         │  Functions  │
└─────────────┘         └─────────────┘         └─────────────┘
     │                        │                       │
     │                        │                       │
     ▼                        ▼                       ▼
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Context   │         │  Middleware │         │   Storage   │
│  Providers  │         │  (Auth)     │         │   (Files)   │
└─────────────┘         └─────────────┘         └─────────────┘
```

### Technology Stack Layers

#### Presentation Layer (Frontend)

- **Framework**: React 18.2 (Component-based UI)
- **UI Library**: Material-UI 5.15 (Design System)
- **Charts**: Recharts 2.10 (Data Visualization)
- **Animations**: Framer Motion 10.16 (UI Animations)
- **Routing**: React Router DOM 6.20 (Navigation)
- **HTTP Client**: Axios 1.6 (API Communication)
- **Build Tool**: Vite 5.0 (Fast Development)

#### Application Layer (Backend)

- **Framework**: Flask 2.3+ (Web Framework)
- **Authentication**: PyJWT 2.9+ (JWT Tokens)
- **CORS**: Flask-CORS 5.0 (Cross-Origin Support)
- **API Design**: RESTful (JSON Responses)

#### Business Logic Layer

- **NLP**: NLTK, TextBlob, VADER Sentiment
- **ML**: scikit-learn, Gensim (LDA)
- **Advanced NLP**: Transformers (BERT, optional)
- **Graph Analytics**: NetworkX

#### Data Processing Layer

- **Data Manipulation**: Pandas, NumPy
- **Text Processing**: Custom preprocessing modules
- **Time Series**: NumPy, Pandas (for forecasting)

#### Data Persistence Layer

- **File Storage**: CSV files (raw/processed data)
- **Model Storage**: Pickle files (.pkl)
- **Forecast Storage**: JSON files
- **Local Storage**: Browser localStorage (frontend)

### Security Architecture

```
┌─────────────────────────────────────────┐
│         Security Layers                 │
├─────────────────────────────────────────┤
│ 1. Authentication (JWT)                 │
│    - Token-based auth                   │
│    - Token expiration (24h)             │
│    - Secure token storage (localStorage)│
├─────────────────────────────────────────┤
│ 2. Authorization                        │
│    - Role-based access (Admin/User)     │
│    - Protected routes                   │
│    - API endpoint guards                │
├─────────────────────────────────────────┤
│ 3. Input Validation                     │
│    - Text input validation              │
│    - Robustness validator               │
│    - Error handling                     │
├─────────────────────────────────────────┤
│ 4. CORS Protection                      │
│    - Configured origins                 │
│    - Credential support                 │
└─────────────────────────────────────────┘
```

### Cognitive Computing Pillars Implementation

#### 🧠 UNDERSTAND Pillar

- **Location**: `src/models/sentiment_analyzer.py`, `src/utils/text_preprocessor.py`
- **Functions**:
  - Text preprocessing and cleaning
  - Sentiment analysis (multi-method)
  - Entity extraction
  - Topic prediction for text

#### 💭 REASON Pillar

- **Location**: `backend_api.py`, `src/models/cognitive_agent.py`
- **Functions**:
  - Topic modeling (LDA)
  - Knowledge graph queries
  - Predictive analytics (forecasting)
  - Insight generation

#### 📚 LEARN Pillar

- **Location**: `src/models/cognitive_agent.py`
- **Functions**:
  - Feedback collection
  - Performance tracking
  - Model improvement suggestions

#### 🤝 INTERACT Pillar

- **Location**: Frontend components, `backend_api.py` response formatting
- **Functions**:
  - User interface rendering
  - Response generation
  - Visualization creation
  - Report generation

### Deployment Architecture

#### Development Environment

```
Developer Machine
├── Backend (Flask)
│   └── Runs on: http://localhost:5000
├── Frontend (Vite Dev Server)
│   └── Runs on: http://localhost:5173
└── Data Storage
    └── Local file system
```

#### Production Considerations

- **Backend**: Can be deployed on cloud platforms (AWS, Azure, GCP)
- **Frontend**: Static build can be hosted on CDN or web server
- **Database**: Currently file-based; can migrate to PostgreSQL/MySQL
- **Model Storage**: Consider cloud storage (S3, Azure Blob)
- **Caching**: Redis for session management and API caching
- **Load Balancing**: Multiple backend instances for scalability

---

## 📡 API Documentation

### Base URL

```
http://localhost:5000/api
```

### Authentication Endpoints

| Method | Endpoint            | Description                | Auth Required |
| ------ | ------------------- | -------------------------- | ------------- |
| POST   | `/api/auth/login` | User login                 | No            |
| GET    | `/api/auth/me`    | Get current user info      | Yes           |
| GET    | `/api/auth/users` | Get all users (admin only) | Yes           |

### Analytics Endpoints

| Method | Endpoint                              | Description                | Auth Required |
| ------ | ------------------------------------- | -------------------------- | ------------- |
| POST   | `/api/sentiment/analyze`            | Analyze single text        | Yes           |
| POST   | `/api/sentiment/batch`              | Batch sentiment analysis   | Yes           |
| GET    | `/api/topics`                       | Get topic modeling results | Yes           |
| GET    | `/api/forecast`                     | Get trend forecasts        | Yes           |
| GET    | `/api/dashboard/stats`              | Get dashboard statistics   | Yes           |
| GET    | `/api/analytics/location-sentiment` | Location-based analytics   | Yes           |
| GET    | `/api/analytics/platform-sentiment` | Platform-based analytics   | Yes           |
| GET    | `/api/analytics/topic-sentiment`    | Topic-based analytics      | Yes           |

### Report & Export

| Method | Endpoint               | Description       | Auth Required |
| ------ | ---------------------- | ----------------- | ------------- |
| POST   | `/api/export/report` | Export PDF report | Yes           |

### Other Endpoints

| Method | Endpoint                         | Description               | Auth Required |
| ------ | -------------------------------- | ------------------------- | ------------- |
| GET    | `/api/health`                  | Health check              | No            |
| POST   | `/api/feedback`                | Submit feedback           | Yes           |
| GET    | `/api/learning/stats`          | Learning statistics       | Yes           |
| POST   | `/api/contact-admin`           | Contact administrator     | Yes           |
| GET    | `/api/notifications`           | Get notifications         | Yes           |
| POST   | `/api/notifications/mark-read` | Mark notification as read | Yes           |

For detailed API documentation, see [backend/README.md](backend/README.md)

## 🔐 Authentication

### Default Login Credentials

#### Admin Account

- **Email**: `admin@business.com`
- **Password**: `admin123`
- **Role**: Administrator (full access)

#### Regular User Accounts

- **Email**: `user1@business.com` through `user7@business.com`
- **Password**: `user123` (for all users)
- **Role**: User (standard access)

### Authentication Flow

1. User submits login credentials via `/api/auth/login`
2. Backend validates credentials and returns JWT token
3. Frontend stores token in localStorage
4. Token is included in `Authorization: Bearer <token>` header for protected routes
5. Token expires after 24 hours (configurable)

## 🎨 Features in Detail

### 1. Sentiment Analysis

- **Single Text Analysis**: Real-time sentiment analysis for individual texts
- **Batch Processing**: Analyze multiple texts simultaneously
- **Multi-Method Ensemble**: Combines VADER, TextBlob, and BERT for accuracy
- **Confidence Scoring**: Provides confidence levels for each prediction

### 2. Dashboard

- **Overview Statistics**: Total reviews, sentiment distribution
- **Interactive Charts**: Bar charts, pie charts, line graphs
- **Real-Time Updates**: Live data refresh capabilities
- **Filter Options**: Filter by date range, location, platform

### 3. Topic Analysis

- **LDA Topic Modeling**: Discover hidden topics in reviews
- **Topic Visualization**: Word clouds and topic distribution charts
- **Topic-Sentiment Mapping**: Understand sentiment per topic

### 4. Trends & Insights

- **Forecast Visualization**: Predictive trend charts
- **Historical Analysis**: Time-series sentiment trends
- **Pattern Recognition**: Identify recurring patterns

### 5. Report Export

- **PDF Generation**: Comprehensive analytics reports in PDF format
- **Automatic Email**: Reports automatically sent to administrator
- **Download Option**: Users can download reports directly

### 6. Notifications

- **Real-Time Alerts**: System notifications for important events
- **User-Specific**: Personalized notification feed
- **Mark as Read**: Notification management

## 📚 Documentation

Comprehensive documentation is available in the `documentation/` folder:

### Part A: System Design

- `01_Problem_Analysis_Document.md` - Problem statement and requirements
- `02_System_Architecture.md` - System architecture and design
- `03_Implementation_Plan.md` - Implementation roadmap

### Part C: Evaluation & Final Report

- `01_System_Evaluation_Report.md` - Performance evaluation
- `02_Ethical_Impact_Analysis.md` - Ethical considerations
- `03_Final_Report.md` - Comprehensive project report
- `04_Presentation_Slides.md` - Presentation materials
- `05_User_Manual.md` - User guide

### Additional Guides

- `BACKEND_SETUP.md` - Backend setup instructions
- `AUTHENTICATION_SETUP.md` - Authentication configuration
- `DATA_COLLECTION_GUIDE.md` - Data collection process

## 🛠️ Development

### Adding New Features

#### Backend

1. Add new endpoints in `backend/backend_api.py`
2. Create models in `backend/src/models/` if needed
3. Add utilities in `backend/src/utils/` if needed
4. Update `requirements.txt` if new packages are required

#### Frontend

1. Create new pages in `frontend/src/pages/`
2. Add reusable components in `frontend/src/components/`
3. Update routing in `frontend/src/App.jsx`
4. Add API calls in `frontend/src/services/api.js`

### Running Tests

```bash
# Backend tests (if available)
cd backend
python -m pytest tests/

# Frontend tests (if available)
cd frontend
npm test
```

### Code Style

- **Python**: Follow PEP 8 guidelines
- **JavaScript**: Follow ESLint configuration
- **React**: Use functional components with hooks

## 🧪 Running Milestone Notebooks

The project includes Jupyter notebooks for each milestone:

1. **Milestone 1**: Data Pipeline (`Cognitive Pillars/Milestone1/01_Data_Pipeline.ipynb`)

   - Data collection and preprocessing
   - Data validation and quality reports
2. **Milestone 2**: Understanding & Reasoning (`Cognitive Pillars/Milestone2/02_Understanding_Reasoning_Engine.ipynb`)

   - Sentiment analysis implementation
   - Topic modeling with LDA
   - Knowledge graph construction
3. **Milestone 3**: Interactive Prototype (`Cognitive Pillars/Milestone3/03_Interactive_Prototype.ipynb`)

   - Frontend-backend integration
   - API testing
4. **Milestone 4**: Evaluation & Ethics (`Cognitive Pillars/Milestone4/04_Evaluation_Ethical_Review.ipynb`)

   - System performance evaluation
   - Ethical impact analysis
5. **Milestone 5**: Final Documentation (`Cognitive Pillars/Milestone5/05_Final_Documentation.ipynb`)

   - Project statistics
   - Final visualizations

To run notebooks:

```bash
jupyter notebook
# or
jupyter lab
```

## 🐛 Troubleshooting

### Backend Issues

**ModuleNotFoundError**

```bash
# Ensure virtual environment is activated
cd backend
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate     # Linux/Mac

# Reinstall dependencies
pip install -r requirements.txt
```

**Port Already in Use**

```bash
# Change port in backend_api.py
app.run(host='0.0.0.0', port=5001)  # Use different port
```

### Frontend Issues

**npm install fails**

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**CORS Errors**

- Ensure backend CORS is configured correctly
- Check that backend is running on correct port

### Common Issues

1. **NLTK Data Missing**: Run `python -c "import nltk; nltk.download('all')"`
2. **Model Files Not Found**: Ensure models are trained and saved in `backend/data/models/`
3. **Email Not Sending**: Configure SMTP settings in backend (see `send_email` function)

## 🤝 Contributing

This is an educational project for the Cognitive Computing course. If you'd like to contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👥 Authors

Emmanuel Nsubuga [https://github.com/Cemputus] Developed for **DSC3112 Cognitive Computing** - Project-Based Learning

## 🙏 Acknowledgments

- **NLTK** - Natural Language Toolkit
- **Material-UI** - React component library
- **Flask** - Python web framework
- **React** - JavaScript library for building user interfaces
- **Gensim** - Topic modeling library
- **NetworkX** - Graph analysis library

## 📞 Support

For issues, questions, or contributions, please open an issue on the GitHub repository.

---

**Built for Cognitive Computing(Academic Reasons)**
