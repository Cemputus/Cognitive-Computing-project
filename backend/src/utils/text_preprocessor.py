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
        
    def clean_text(self, text, preserve_length=False):
        """
        Enhanced text cleaning with better edge case handling
        
        Args:
            text: Raw text string
            preserve_length: If True, preserves text length for very short texts
            
        Returns:
            Cleaned text string
        """
        # Handle None, NaN, empty strings
        if pd.isna(text) or text is None:
            return ""
        
        # Convert to string
        text = str(text)
        
        # Handle empty or whitespace-only strings
        if not text.strip():
            return ""
        
        original_length = len(text)
        
        # Remove URLs (more comprehensive pattern)
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text, flags=re.MULTILINE)
        text = re.sub(r'www\.\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
        
        # Remove mentions and hashtags (but keep the text after #)
        text = re.sub(r'@\w+', '', text)
        text = re.sub(r'#(\w+)', r'\1', text)
        
        # Handle emojis - convert to text or remove
        # Keep common positive/negative emojis as they carry sentiment
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map
            u"\U0001F1E0-\U0001F1FF"  # flags
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE)
        text = emoji_pattern.sub('', text)  # Remove emojis for now
        
        # Remove special characters but keep spaces, letters, numbers, and basic punctuation
        # Keep punctuation that might indicate sentiment (!, ?, ...)
        text = re.sub(r'[^\w\s!?.,;:()\-\']', ' ', text)
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # For very short texts, be more lenient
        if preserve_length and len(text) < 5 and original_length > 0:
            # Try to preserve at least some content
            text = text if text else "neutral"  # Fallback
        
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

