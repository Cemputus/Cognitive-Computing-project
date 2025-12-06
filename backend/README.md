# 🔧 CENAnalytics Backend API

Flask REST API backend for the CENAnalytics Business Intelligence Platform. Provides comprehensive endpoints for sentiment analysis, topic modeling, predictive analytics, and report generation.

## 📋 Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Data Models](#data-models)
- [Dependencies](#dependencies)
- [Running the Server](#running-the-server)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

The backend API is built with Flask and provides:

- **RESTful API** for frontend communication
- **JWT-based Authentication** for secure access
- **Sentiment Analysis** using multiple methods (VADER, TextBlob, Ensemble)
- **Topic Modeling** with LDA (Latent Dirichlet Allocation)
- **Predictive Analytics** with trend forecasting
- **Knowledge Graph** construction and analysis
- **PDF Report Generation** with automatic email delivery
- **Notification System** for user alerts

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Create Virtual Environment

```bash
cd backend
python -m venv venv
```

### Step 2: Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Download NLTK Data

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('vader_lexicon'); nltk.download('wordnet')"
```

### Step 5: Verify Installation

```bash
python -c "import flask, pandas, sklearn, nltk; print('All dependencies installed successfully!')"
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the `backend/` directory (optional):

```env
JWT_SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=True
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
ADMIN_EMAIL=ensubuga019@gmail.com
```

### Default Configuration

- **JWT Secret Key**: Set in `auth.py` (change in production!)
- **Token Expiration**: 24 hours (configurable in `auth.py`)
- **CORS**: Enabled for all origins (configure for production)
- **Port**: 5000 (default Flask port)

## 🚀 Running the Server

### Option 1: Using Start Script (Windows)

```powershell
# From project root
.\backend\scripts\start_backend.bat

# OR from backend/scripts/
cd backend\scripts
.\start_backend.bat
```

### Option 2: Using PowerShell Script

```powershell
.\backend\scripts\start_backend.ps1
```

### Option 3: Manual Start

```bash
cd backend
python backend_api.py
```

The server will start on `http://localhost:5000`

### Verify Server is Running

```bash
curl http://localhost:5000/api/health
# Expected response: {"status": "healthy", "message": "API is running"}
```

## 📡 API Endpoints

### Health Check

**GET** `/api/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

---

### Authentication

#### Login

**POST** `/api/auth/login`

Authenticate user and receive JWT token.

**Request Body:**
```json
{
  "email": "user1@business.com",
  "password": "user123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": "2",
    "email": "user1@business.com",
    "name": "Sarah Nakato",
    "role": "user"
  }
}
```

#### Get Current User

**GET** `/api/auth/me` 🔒

Get information about the currently authenticated user.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": "2",
  "email": "user1@business.com",
  "name": "Sarah Nakato",
  "role": "user"
}
```

#### Get All Users (Admin Only)

**GET** `/api/auth/users` 🔒

Get list of all users (admin access required).

**Headers:**
```
Authorization: Bearer <admin_token>
```

---

### Sentiment Analysis

#### Analyze Single Text

**POST** `/api/sentiment/analyze` 🔒

Analyze sentiment of a single text.

**Request Body:**
```json
{
  "text": "I love this product! It's amazing."
}
```

**Response:**
```json
{
  "sentiment": "positive",
  "confidence": 0.95,
  "scores": {
    "positive": 0.85,
    "negative": 0.05,
    "neutral": 0.10
  },
  "methods": {
    "vader": "positive",
    "textblob": "positive",
    "ensemble": "positive"
  }
}
```

#### Batch Analysis

**POST** `/api/sentiment/batch` 🔒

Analyze multiple texts at once.

**Request Body:**
```json
{
  "texts": [
    "Great product!",
    "Not satisfied with the service.",
    "It's okay, nothing special."
  ]
}
```

**Response:**
```json
{
  "results": [
    {
      "text": "Great product!",
      "sentiment": "positive",
      "confidence": 0.92
    },
    {
      "text": "Not satisfied with the service.",
      "sentiment": "negative",
      "confidence": 0.88
    },
    {
      "text": "It's okay, nothing special.",
      "sentiment": "neutral",
      "confidence": 0.75
    }
  ],
  "summary": {
    "total": 3,
    "positive": 1,
    "negative": 1,
    "neutral": 1
  }
}
```

---

### Analytics

#### Dashboard Statistics

**GET** `/api/dashboard/stats` 🔒

Get overall dashboard statistics.

**Response:**
```json
{
  "total_reviews": 1000,
  "positive_pct": 65.5,
  "negative_pct": 20.3,
  "neutral_pct": 14.2,
  "recent_trend": "improving"
}
```

#### Location-Based Sentiment

**GET** `/api/analytics/location-sentiment` 🔒

Get sentiment analysis grouped by location.

**Query Parameters:**
- `limit` (optional): Number of locations to return (default: 10)

**Response:**
```json
{
  "locations": [
    {
      "location": "Kampala",
      "total": 250,
      "positive_pct": 70.0,
      "negative_pct": 15.0,
      "neutral_pct": 15.0
    }
  ],
  "summary": {
    "total_locations": 5,
    "total_reviews": 1000
  }
}
```

#### Platform-Based Sentiment

**GET** `/api/analytics/platform-sentiment` 🔒

Get sentiment analysis grouped by platform (Google, Facebook, etc.).

**Response:**
```json
{
  "platforms": [
    {
      "platform": "Google",
      "total": 400,
      "positive_pct": 68.5,
      "negative_pct": 18.2,
      "neutral_pct": 13.3
    }
  ]
}
```

#### Topic-Based Sentiment

**GET** `/api/analytics/topic-sentiment` 🔒

Get sentiment analysis grouped by discovered topics.

**Response:**
```json
{
  "topics": [
    {
      "topic": 0,
      "topic_name": "Product Quality",
      "total": 300,
      "positive_pct": 75.0,
      "negative_pct": 20.0,
      "neutral_pct": 5.0,
      "keywords": ["quality", "product", "excellent"]
    }
  ]
}
```

---

### Topic Modeling

#### Get Topics

**GET** `/api/topics` 🔒

Get LDA topic modeling results.

**Query Parameters:**
- `num_topics` (optional): Number of topics (default: 5)
- `num_words` (optional): Words per topic (default: 10)

**Response:**
```json
{
  "topics": [
    {
      "topic_id": 0,
      "words": [
        {"word": "product", "weight": 0.15},
        {"word": "quality", "weight": 0.12}
      ]
    }
  ],
  "num_topics": 5
}
```

---

### Predictive Analytics

#### Get Forecasts

**GET** `/api/forecast` 🔒

Get trend forecasts for sentiment over time.

**Query Parameters:**
- `periods` (optional): Forecast periods (default: 7)

**Response:**
```json
{
  "forecast": [
    {
      "date": "2024-01-15",
      "predicted_sentiment": 0.72,
      "confidence": 0.85
    }
  ],
  "method": "ARIMA",
  "accuracy": 0.88
}
```

---

### Report Export

#### Export Report

**POST** `/api/export/report` 🔒

Generate and export analytics report as PDF. Automatically sends a copy to the administrator email.

**Request Body:**
```json
{
  "type": "dashboard"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Report exported and sent to admin",
  "pdf": "base64_encoded_pdf_string",
  "filename": "CENAnalytics_Report_20240115_143022.pdf",
  "notifications_created": 2
}
```

**Note:** The PDF is base64-encoded in the response. The frontend decodes it and triggers a download.

---

### Notifications

#### Get Notifications

**GET** `/api/notifications` 🔒

Get all notifications for the current user.

**Response:**
```json
{
  "notifications": [
    {
      "id": 1,
      "type": "success",
      "title": "Report Generated",
      "message": "Your analytics report has been generated successfully.",
      "timestamp": "2024-01-15T14:30:22",
      "read": false
    }
  ],
  "unread_count": 2
}
```

#### Mark Notification as Read

**POST** `/api/notifications/mark-read` 🔒

Mark a notification as read.

**Request Body:**
```json
{
  "notification_id": 1
}
```

---

### Feedback & Learning

#### Submit Feedback

**POST** `/api/feedback` 🔒

Submit feedback for model improvement.

**Request Body:**
```json
{
  "text": "The sentiment analysis was incorrect.",
  "correct_sentiment": "positive",
  "predicted_sentiment": "negative"
}
```

#### Learning Statistics

**GET** `/api/learning/stats` 🔒

Get statistics about the learning system.

**Response:**
```json
{
  "total_feedback": 50,
  "accuracy_improvement": 0.05,
  "model_updates": 3
}
```

---

### Contact Admin

**POST** `/api/contact-admin` 🔒

Send a message to the administrator.

**Request Body:**
```json
{
  "subject": "Question about analytics",
  "message": "I have a question about the dashboard."
}
```

---

## 🔐 Authentication

### JWT Token Format

Tokens are JWT (JSON Web Tokens) with the following structure:

**Header:**
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload:**
```json
{
  "sub": "user1@business.com",
  "exp": 1705324800,
  "role": "user"
}
```

### Using Tokens

Include the token in the `Authorization` header:

```
Authorization: Bearer <your_token_here>
```

### Token Expiration

- Default expiration: 24 hours
- Configurable in `auth.py`: `ACCESS_TOKEN_EXPIRE_MINUTES`

### Default Users

See main [README.md](../README.md) for default login credentials.

---

## 📊 Data Models

### Sentiment Analyzer

Located in `src/models/sentiment_analyzer.py`

- **Methods**: VADER, TextBlob, Ensemble
- **Output**: Sentiment label + confidence scores

### Cognitive Agent

Located in `src/models/cognitive_agent.py`

- Orchestrates sentiment analysis, topic modeling, and knowledge graph operations
- Provides high-level business intelligence insights

### Knowledge Graph

- Stored in `data/models/knowledge_graph.pkl`
- Built using NetworkX
- Contains entity-relationship mappings

---

## 📚 Dependencies

### Core Dependencies

- **flask** (2.3.0+): Web framework
- **flask-cors** (4.0.0+): CORS support
- **PyJWT** (2.8.0+): JWT authentication

### Data Processing

- **pandas** (1.5.0+): Data manipulation
- **numpy** (1.23.0+): Numerical computing

### Machine Learning

- **scikit-learn** (1.2.0+): ML algorithms
- **gensim** (4.3.0+): Topic modeling (LDA)

### NLP

- **nltk** (3.8+): Natural language processing
- **textblob** (0.17.1+): Text processing
- **vaderSentiment** (3.3.2+): Sentiment analysis
- **transformers** (4.30.0+): BERT models

### Visualization

- **matplotlib** (3.7.0+): Plotting
- **seaborn** (0.12.0+): Statistical visualization
- **plotly** (5.14.0+): Interactive plots
- **wordcloud** (1.9.2+): Word cloud generation

### Graph Analytics

- **networkx** (3.1+): Graph construction and analysis

### PDF Generation

- **reportlab** (4.0.0+): PDF report generation

### Utilities

- **python-dotenv** (1.0.0+): Environment variables
- **tqdm** (4.65.0+): Progress bars

See `requirements.txt` for complete list with versions.

---

## 🐛 Troubleshooting

### ModuleNotFoundError

**Problem:** `ModuleNotFoundError: No module named 'X'`

**Solution:**
```bash
# Ensure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

### Port Already in Use

**Problem:** `Address already in use`

**Solution:**
1. Find process using port 5000:
   ```bash
   # Windows
   netstat -ano | findstr :5000
   
   # Linux/Mac
   lsof -i :5000
   ```
2. Kill the process or change port in `backend_api.py`:
   ```python
   app.run(host='0.0.0.0', port=5001)
   ```

### NLTK Data Missing

**Problem:** `LookupError: Resource 'punkt' not found`

**Solution:**
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('vader_lexicon')"
```

### Model Files Not Found

**Problem:** `FileNotFoundError: knowledge_graph.pkl`

**Solution:**
- Ensure models are trained (run milestone notebooks)
- Models should be in `backend/data/models/`
- System will work without models but with limited functionality

### CORS Errors

**Problem:** CORS policy errors in browser

**Solution:**
- Check CORS configuration in `backend_api.py`
- Ensure frontend URL is allowed
- Verify backend is running on correct port

### Email Not Sending

**Problem:** PDF reports not being emailed

**Solution:**
1. Configure SMTP settings in `send_email` function
2. Use app-specific password for Gmail
3. Check firewall/network settings

---

## 📝 Code Structure

```
backend/
├── backend_api.py          # Main Flask application
├── auth.py                 # Authentication module
├── requirements.txt        # Dependencies
├── data/
│   ├── raw/               # Raw data files
│   ├── processed/         # Processed datasets
│   └── models/            # Trained models
├── src/
│   ├── models/
│   │   ├── sentiment_analyzer.py
│   │   └── cognitive_agent.py
│   └── utils/
│       ├── text_preprocessor.py
│       ├── wordcloud_generator.py
│       └── robustness_validator.py
└── scripts/
    ├── start_backend.bat
    └── start_backend.ps1
```

---

## 🔒 Security Notes

⚠️ **Important for Production:**

1. **Change JWT Secret Key**: Update `SECRET_KEY` in `auth.py`
2. **Use Environment Variables**: Store sensitive data in `.env`
3. **Configure CORS**: Restrict CORS to specific origins
4. **Use HTTPS**: Enable SSL/TLS in production
5. **Database**: Replace in-memory storage with proper database
6. **Password Hashing**: Use stronger hashing (bcrypt, argon2)
7. **Rate Limiting**: Implement rate limiting for API endpoints
8. **Input Validation**: Validate and sanitize all inputs

---

## 📞 Support

For backend-specific issues:

1. Check the [main README](../README.md)
2. Review error logs in console
3. Verify all dependencies are installed
4. Ensure data files and models are in place

---

**Backend API Documentation** | Part of CENAnalytics Platform
