"""
Sentiment Analysis Module for Small Business Intelligence Analyst
Implements multiple sentiment analysis approaches
"""

import pandas as pd
import numpy as np
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline


class SentimentAnalyzer:
    """Sentiment analysis using multiple approaches"""
    
    def __init__(self, method='vader'):
        """
        Initialize sentiment analyzer
        
        Args:
            method: 'vader', 'textblob', or 'transformer'
        """
        self.method = method
        
        if method == 'vader':
            self.analyzer = SentimentIntensityAnalyzer()
        elif method == 'textblob':
            self.analyzer = None  # TextBlob doesn't need initialization
        elif method == 'transformer':
            try:
                self.analyzer = pipeline("sentiment-analysis", 
                                        model="nlptown/bert-base-multilingual-uncased-sentiment")
            except:
                print("Transformer model not available, falling back to VADER")
                self.analyzer = SentimentIntensityAnalyzer()
                self.method = 'vader'
    
    def analyze_vader(self, text):
        """Analyze sentiment using VADER"""
        scores = self.analyzer.polarity_scores(text)
        return {
            'compound': scores['compound'],
            'positive': scores['pos'],
            'negative': scores['neg'],
            'neutral': scores['neu'],
            'sentiment': 'positive' if scores['compound'] >= 0.05 else 
                        'negative' if scores['compound'] <= -0.05 else 'neutral'
        }
    
    def analyze_textblob(self, text):
        """Analyze sentiment using TextBlob"""
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        return {
            'polarity': polarity,
            'subjectivity': subjectivity,
            'sentiment': 'positive' if polarity > 0 else 'negative' if polarity < 0 else 'neutral'
        }
    
    def analyze_transformer(self, text):
        """Analyze sentiment using transformer model"""
        result = self.analyzer(text)[0]
        label = result['label']
        score = result['score']
        
        # Map label to sentiment
        sentiment_map = {
            '1 star': 'very_negative',
            '2 star': 'negative',
            '3 star': 'neutral',
            '4 star': 'positive',
            '5 star': 'very_positive'
        }
        
        return {
            'label': label,
            'score': score,
            'sentiment': sentiment_map.get(label, 'neutral')
        }
    
    def analyze(self, text):
        """
        Analyze sentiment of text using configured method
        
        Args:
            text: Text string to analyze
            
        Returns:
            Dictionary with sentiment scores and label
        """
        if self.method == 'vader':
            return self.analyze_vader(text)
        elif self.method == 'textblob':
            return self.analyze_textblob(text)
        elif self.method == 'transformer':
            return self.analyze_transformer(text)
        else:
            raise ValueError(f"Unknown method: {self.method}")
    
    def analyze_batch(self, texts):
        """
        Analyze sentiment for multiple texts
        
        Args:
            texts: List or Series of text strings
            
        Returns:
            DataFrame with sentiment analysis results
        """
        results = [self.analyze(text) for text in texts]
        return pd.DataFrame(results)

