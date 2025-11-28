# Task A2: System Architecture & Cognitive Design

**Marks**: 10/30  
**Status**: Template - To be completed

---

## 1. System Architecture Overview

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  User Interface Layer                        │
│  (Streamlit Web App / Chatbot Interface)                    │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              Cognitive Processing Layer                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Understand  │  │    Reason     │  │   Interact   │     │
│  │     (NLP)    │  │ (ML Models)   │  │  (Response)  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              Data Processing Layer                           │
│  (Preprocessing, Feature Extraction, Data Storage)            │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                  Data Sources                               │
│  (Customer Reviews, Social Media, Market Data)              │
└─────────────────────────────────────────────────────────────┘
```

[**YOUR TASK**: Create a detailed system architecture diagram using tools like Draw.io, Lucidchart, or PowerPoint. Include all components and data flows.]

---

## 2. Component Details

### 2.1 Data Sources
- **Customer Reviews**: CSV files, API feeds
- **Social Media Posts**: Twitter, Facebook data
- **Market Data**: Business news, market reports

### 2.2 Data Processing Layer
- **Text Preprocessor**: Cleaning, tokenization, lemmatization
- **Feature Extractor**: Entity extraction, keyword extraction
- **Data Storage**: Processed data in CSV/JSON format

### 2.3 Cognitive Processing Layer

#### Understanding Component
- **Natural Language Processing**
  - Text preprocessing
  - Sentiment analysis (VADER, TextBlob)
  - Entity recognition
- **Input**: Raw text data
- **Output**: Cleaned text, sentiment scores, entities

#### Reasoning Component
- **Knowledge Graph**
  - Entity-sentiment relationships
  - Topic-entity connections
- **Topic Modeling**
  - LDA model for topic extraction
- **Machine Learning Models**
  - Sentiment classification
  - Trend prediction (optional)
- **Input**: Processed text, entities
- **Output**: Topics, insights, predictions

#### Learning Component
- **Model Updates**: Retrain on new data
- **Feedback Loop**: User feedback incorporation
- **Performance Monitoring**: Track model accuracy

#### Interaction Component
- **Response Generation**: Human-readable insights
- **Visualization**: Charts and graphs
- **Report Generation**: Business intelligence reports

### 2.4 User Interface Layer
- **Streamlit Web Application**
  - Dashboard
  - Query interface
  - Results visualization
- **Alternative**: Chatbot interface

---

## 3. Cognitive Processing Pipeline

### 3.1 Detailed Pipeline Diagram

[**YOUR TASK**: Create a detailed cognitive processing pipeline diagram showing:]

```
INPUT (User Query/Review)
    │
    ▼
[Text Preprocessing]
    │
    ▼
[Sentiment Analysis] ──────► UNDERSTAND Pillar
    │
    ▼
[Entity Extraction]
    │
    ▼
[Knowledge Graph Query] ───► REASON Pillar
    │
    ▼
[Topic Modeling]
    │
    ▼
[Insight Generation]
    │
    ▼
[Response Formatting] ──────► INTERACT Pillar
    │
    ▼
OUTPUT (Business Intelligence Report)
```

### 3.2 Mapping to Cognitive Pillars

#### UNDERSTAND Pillar
**Components:**
- Text preprocessing (`TextPreprocessor` class)
- Sentiment analysis (`SentimentAnalyzer` class)
- Entity extraction

**How it works:**
1. Raw text input is cleaned and normalized
2. Sentiment scores are calculated
3. Key entities are identified
4. Context is extracted from unstructured text

**Output**: Structured understanding of text meaning and sentiment

#### REASON Pillar
**Components:**
- Knowledge graph (`NetworkX` graph)
- Topic modeling (`LDA` model)
- ML models for classification

**How it works:**
1. Entities are connected in knowledge graph
2. Topics are extracted from document corpus
3. Relationships are queried to generate insights
4. Patterns are identified across data

**Output**: Reasoning-based insights and recommendations

#### LEARN Pillar
**Components:**
- Model retraining pipeline
- Feedback collection mechanism
- Performance monitoring

**How it works:**
1. New data is collected over time
2. Models are periodically retrained
3. User feedback is incorporated
4. System performance improves

**Output**: Improved model accuracy and relevance

#### INTERACT Pillar
**Components:**
- Response generator
- Visualization engine
- Report formatter

**How it works:**
1. Insights are formatted for human understanding
2. Visualizations are generated
3. Reports are created
4. User-friendly interface presents results

**Output**: Clear, actionable business intelligence

---

## 4. Technology Stack

### 4.1 Core Technologies
- **Python 3.8+**: Main programming language
- **Jupyter Notebooks**: Development and analysis
- **Streamlit**: Web interface framework

### 4.2 NLP Libraries
- **NLTK**: Text preprocessing
- **VADER**: Sentiment analysis
- **TextBlob**: Alternative sentiment analysis
- **Gensim**: Topic modeling (LDA)
- **Transformers**: Advanced NLP (optional)

### 4.3 Data Processing
- **Pandas**: Data manipulation
- **NumPy**: Numerical operations
- **NetworkX**: Knowledge graph construction

### 4.4 Visualization
- **Matplotlib**: Basic plotting
- **Seaborn**: Statistical visualizations
- **Plotly**: Interactive charts
- **WordCloud**: Word visualizations

### 4.5 Model Persistence
- **Pickle**: Model serialization
- **Joblib**: Efficient model saving

---

## 5. Data Flow Architecture

### 5.1 Input Flow
```
Raw Data (Reviews/Social Media)
    ↓
Data Acquisition Module
    ↓
Text Preprocessing
    ↓
Feature Extraction
    ↓
Structured Data Storage
```

### 5.2 Processing Flow
```
Structured Data
    ↓
Understanding Engine (Sentiment Analysis)
    ↓
Reasoning Engine (Topic Modeling, Knowledge Graph)
    ↓
Insight Generation
    ↓
Response Formatting
```

### 5.3 Output Flow
```
Formatted Insights
    ↓
Visualization Generation
    ↓
Report Creation
    ↓
User Interface Display
```

---

## 6. System Components Diagram

[**YOUR TASK**: Create a component diagram showing:]

- **Data Layer**: Data sources, storage
- **Processing Layer**: Preprocessing, feature extraction
- **Cognitive Layer**: Understanding, reasoning, learning
- **Interface Layer**: Web app, API
- **Integration Points**: How components interact

---

## 7. Deployment Architecture

### 7.1 Development Environment
- Local Python environment
- Jupyter Notebooks for development
- Local data storage

### 7.2 Production Considerations
[**YOUR TASK**: Describe production deployment considerations:]
- Cloud deployment options
- Scalability considerations
- Performance optimization
- Security measures

---

## 8. Cognitive Design Rationale

### 8.1 Why This Architecture?
[**YOUR TASK**: Justify architectural decisions:]
- Modular design for maintainability
- Separation of concerns
- Scalability considerations
- Technology choices

### 8.2 Cognitive Principles Applied
[**YOUR TASK**: Explain how architecture supports cognitive computing:]
- How understanding is achieved
- How reasoning is implemented
- How learning is incorporated
- How interaction is facilitated

---

## 9. Diagrams to Create

[**YOUR TASK**: Create the following diagrams:]

1. **System Architecture Diagram** (High-level)
2. **Cognitive Processing Pipeline** (Detailed flow)
3. **Component Interaction Diagram** (How components communicate)
4. **Data Flow Diagram** (Data movement through system)
5. **Deployment Diagram** (If applicable)

**Tools for creating diagrams:**
- Draw.io (free, online)
- Lucidchart
- Microsoft Visio
- PowerPoint/Google Slides
- PlantUML (code-based)

---

## 10. Appendix

### 10.1 Glossary
- **Cognitive Computing**: Systems that mimic human thought processes
- **Sentiment Analysis**: Determining emotional tone in text
- **Topic Modeling**: Discovering hidden topics in documents
- **Knowledge Graph**: Network representation of entities and relationships

### 10.2 References
- Architecture patterns used
- Design principles followed
- Technology documentation

---

**Note**: This is a template. Create actual diagrams and fill in all sections with detailed descriptions. The architecture should clearly show how the four cognitive pillars are implemented.

