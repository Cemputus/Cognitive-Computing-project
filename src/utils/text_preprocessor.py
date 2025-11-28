"""
Text Preprocessing Utilities for Small Business Intelligence Analyst
Handles cleaning and preprocessing of unstructured text data from reviews and social media
"""

import re
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
except:
    pass


class TextPreprocessor:
    """Text preprocessing class for cleaning unstructured text data"""
    
    def __init__(self, language='english'):
        """
        Initialize text preprocessor
        
        Args:
            language: Language for stopwords (default: 'english')
        """
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words(language))
        
        # Ugandan-specific stopwords and expressions (expand as needed)
        self.ugandan_stopwords = {'kati', 'ne', 'era', 'nya', 'nnyo'}  # Luganda stopwords
        
    def clean_text(self, text):
        """
        Clean and preprocess text
        
        Args:
            text: Raw text string
            
        Returns:
            Cleaned text string
        """
        if pd.isna(text) or text is None:
            return ""
        
        # Convert to string
        text = str(text)
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove mentions and hashtags (but keep the text after #)
        text = re.sub(r'@\w+', '', text)
        text = re.sub(r'#(\w+)', r'\1', text)
        
        # Remove special characters but keep spaces and letters
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def tokenize_and_lemmatize(self, text):
        """
        Tokenize and lemmatize text
        
        Args:
            text: Cleaned text string
            
        Returns:
            List of lemmatized tokens
        """
        tokens = word_tokenize(text)
        tokens = [
            self.lemmatizer.lemmatize(token) 
            for token in tokens 
            if token not in self.stop_words 
            and token not in self.ugandan_stopwords
            and len(token) > 2
            and token.isalpha()
        ]
        return tokens
    
    def preprocess(self, text):
        """
        Complete preprocessing pipeline
        
        Args:
            text: Raw text string
            
        Returns:
            Preprocessed text string
        """
        cleaned = self.clean_text(text)
        tokens = self.tokenize_and_lemmatize(cleaned)
        return ' '.join(tokens)
    
    def preprocess_batch(self, texts):
        """
        Preprocess a batch of texts
        
        Args:
            texts: List or Series of text strings
            
        Returns:
            List of preprocessed text strings
        """
        return [self.preprocess(text) for text in texts]


def extract_features(text):
    """
    Extract basic features from text
    
    Args:
        text: Text string
        
    Returns:
        Dictionary of features
    """
    features = {
        'word_count': len(text.split()),
        'character_count': len(text),
        'has_question': '?' in text,
        'has_exclamation': '!' in text,
        'avg_word_length': np.mean([len(word) for word in text.split()]) if text.split() else 0
    }
    return features

