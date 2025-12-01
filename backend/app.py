"""
Streamlit Web Application for Small Business Intelligence Analyst
Interactive interface for querying business intelligence insights
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.models.sentiment_analyzer import SentimentAnalyzer
from src.utils.text_preprocessor import TextPreprocessor

# Page configuration
st.set_page_config(
    page_title="Small Business Intelligence Analyst",
    page_icon="📊",
    layout="wide"
)

# Initialize session state
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = SentimentAnalyzer(method='vader')
    st.session_state.preprocessor = TextPreprocessor()

def main():
    """Main application function"""
    
    st.title("📊 Small Business Intelligence Analyst")
    st.markdown("### Cognitive Intelligence System for Business Insights")
    st.markdown("---")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Choose a page",
        ["Home", "Sentiment Analysis", "Topic Analysis", "Trends & Insights", "About"]
    )
    
    if page == "Home":
        show_home_page()
    elif page == "Sentiment Analysis":
        show_sentiment_analysis()
    elif page == "Topic Analysis":
        show_topic_analysis()
    elif page == "Trends & Insights":
        show_trends_insights()
    elif page == "About":
        show_about_page()

def show_home_page():
    """Display home page"""
    st.header("Welcome to Your Business Intelligence Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Reviews", "1,234", "↑ 12%")
    
    with col2:
        st.metric("Avg Sentiment", "Positive", "↑ 5%")
    
    with col3:
        st.metric("Key Topics", "8", "→")
    
    st.markdown("---")
    
    st.subheader("Quick Actions")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("💬 **Analyze Reviews**: Upload customer reviews or paste text for sentiment analysis")
        st.info("📈 **View Trends**: Explore sentiment trends over time")
    
    with col2:
        st.info("🔍 **Topic Discovery**: Identify key topics in customer feedback")
        st.info("📊 **Generate Report**: Create comprehensive business intelligence reports")

def show_sentiment_analysis():
    """Display sentiment analysis interface"""
    st.header("Sentiment Analysis")
    
    tab1, tab2 = st.tabs(["Single Text Analysis", "Batch Analysis"])
    
    with tab1:
        st.subheader("Analyze Single Text")
        text_input = st.text_area("Enter text to analyze:", height=100)
        
        if st.button("Analyze Sentiment"):
            if text_input:
                result = st.session_state.analyzer.analyze(text_input)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Sentiment", result.get('sentiment', 'N/A').title())
                
                with col2:
                    compound = result.get('compound', 0)
                    st.metric("Compound Score", f"{compound:.3f}")
                
                with col3:
                    if 'positive' in result:
                        st.metric("Positive Score", f"{result['positive']:.3f}")
                
                # Visualization
                if 'positive' in result:
                    fig = go.Figure(data=[
                        go.Bar(name='Positive', x=['Positive'], y=[result['positive']], marker_color='green'),
                        go.Bar(name='Neutral', x=['Neutral'], y=[result['neutral']], marker_color='gray'),
                        go.Bar(name='Negative', x=['Negative'], y=[result['negative']], marker_color='red')
                    ])
                    fig.update_layout(barmode='stack', title='Sentiment Distribution')
                    st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Batch Analysis")
        st.info("Upload a CSV file with a 'text' column for batch analysis")
        
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.dataframe(df.head())
            
            if 'text' in df.columns:
                if st.button("Analyze All Texts"):
                    with st.spinner("Analyzing sentiments..."):
                        results = st.session_state.analyzer.analyze_batch(df['text'])
                        df_results = pd.concat([df, results], axis=1)
                        st.dataframe(df_results)
                        
                        # Download button
                        csv = df_results.to_csv(index=False)
                        st.download_button(
                            label="Download Results",
                            data=csv,
                            file_name="sentiment_analysis_results.csv",
                            mime="text/csv"
                        )

def show_topic_analysis():
    """Display topic analysis interface"""
    st.header("Topic Analysis")
    st.info("Topic modeling functionality will be implemented here")
    
    # Placeholder for topic modeling implementation
    st.text("This feature will identify key topics in customer feedback using LDA or BERTopic")

def show_trends_insights():
    """Display trends and insights"""
    st.header("Trends & Insights")
    st.info("Trend analysis and predictive insights will be displayed here")
    
    # Placeholder for trends visualization
    st.text("This feature will show sentiment trends over time and predictive insights")

def show_about_page():
    """Display about page"""
    st.header("About This System")
    
    st.markdown("""
    ### Small Business Intelligence Analyst
    
    A cognitive computing system designed to help small business owners in Kampala, Uganda 
    understand customer sentiment and market trends through intelligent analysis of reviews 
    and social media data.
    
    #### Features:
    - **Sentiment Analysis**: Understand customer feelings and opinions
    - **Topic Modeling**: Identify key themes in feedback
    - **Trend Analysis**: Track sentiment and topic trends over time
    - **Predictive Insights**: Forecast market trends
    
    #### Cognitive Pillars:
    1. **Understand**: Natural Language Processing
    2. **Reason**: Knowledge graphs and ML models
    3. **Learn**: Model refinement from feedback
    4. **Interact**: Intuitive web interface
    
    #### Technology Stack:
    - Python 3.8+
    - Streamlit for web interface
    - Transformers for NLP
    - Scikit-learn for ML models
    """)

if __name__ == "__main__":
    main()



