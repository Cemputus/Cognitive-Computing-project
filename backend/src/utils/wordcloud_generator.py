"""
WordCloud Visualization Utilities
Generate wordclouds for text analysis and visualization
"""

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from typing import List, Dict, Optional
import pandas as pd


class WordCloudGenerator:
    """Generate wordcloud visualizations for text analysis"""
    
    def __init__(self, width=800, height=400, max_words=100, background_color='white'):
        """
        Initialize wordcloud generator
        
        Args:
            width: Width of wordcloud image
            height: Height of wordcloud image
            max_words: Maximum number of words to display
            background_color: Background color
        """
        self.width = width
        self.height = height
        self.max_words = max_words
        self.background_color = background_color
    
    def generate_wordcloud(self, text: str, title: str = "Word Cloud", 
                          figsize=(12, 6), colormap='viridis') -> None:
        """
        Generate and display a wordcloud from text
        
        Args:
            text: Input text string
            title: Title for the plot
            figsize: Figure size (width, height)
            colormap: Colormap for wordcloud
        """
        if not text or len(text.strip()) == 0:
            print("⚠️ Empty text provided, cannot generate wordcloud")
            return
        
        # Generate wordcloud
        wordcloud = WordCloud(
            width=self.width,
            height=self.height,
            max_words=self.max_words,
            background_color=self.background_color,
            colormap=colormap,
            collocations=False,
            relative_scaling=0.5,
            random_state=42
        ).generate(text)
        
        # Display
        plt.figure(figsize=figsize)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(title, fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout(pad=0)
        plt.show()
    
    def generate_wordcloud_from_list(self, texts: List[str], title: str = "Word Cloud",
                                     figsize=(12, 6), colormap='viridis') -> None:
        """
        Generate wordcloud from list of texts
        
        Args:
            texts: List of text strings
            title: Title for the plot
            figsize: Figure size
            colormap: Colormap for wordcloud
        """
        # Combine all texts
        combined_text = ' '.join(str(text) for text in texts if text)
        self.generate_wordcloud(combined_text, title, figsize, colormap)
    
    def generate_wordcloud_from_dataframe(self, df: pd.DataFrame, text_column: str,
                                         title: str = "Word Cloud", 
                                         figsize=(12, 6), colormap='viridis',
                                         filter_by: Optional[str] = None,
                                         filter_value: Optional[str] = None) -> None:
        """
        Generate wordcloud from DataFrame column
        
        Args:
            df: DataFrame containing text
            text_column: Name of column containing text
            title: Title for the plot
            figsize: Figure size
            colormap: Colormap for wordcloud
            filter_by: Optional column to filter by
            filter_value: Value to filter by
        """
        # Filter if needed
        if filter_by and filter_value:
            df_filtered = df[df[filter_by] == filter_value]
            texts = df_filtered[text_column].dropna().tolist()
            title = f"{title} - {filter_by}: {filter_value}"
        else:
            texts = df[text_column].dropna().tolist()
        
        self.generate_wordcloud_from_list(texts, title, figsize, colormap)
    
    def generate_sentiment_wordclouds(self, df: pd.DataFrame, text_column: str,
                                     sentiment_column: str = 'sentiment',
                                     figsize=(16, 12)) -> None:
        """
        Generate separate wordclouds for each sentiment category
        
        Args:
            df: DataFrame with text and sentiment
            text_column: Column name for text
            sentiment_column: Column name for sentiment
            figsize: Figure size for subplots
        """
        if sentiment_column not in df.columns:
            print(f"⚠️ Column '{sentiment_column}' not found in DataFrame")
            return
        
        # Get unique sentiments
        sentiments = df[sentiment_column].unique()
        n_sentiments = len(sentiments)
        
        # Create subplots
        fig, axes = plt.subplots(1, n_sentiments, figsize=figsize)
        if n_sentiments == 1:
            axes = [axes]
        
        # Color map for each sentiment
        colormaps = {
            'positive': 'Greens',
            'negative': 'Reds',
            'neutral': 'Blues',
            'unknown': 'Purples'
        }
        
        for idx, sentiment in enumerate(sentiments):
            # Filter by sentiment
            df_sentiment = df[df[sentiment_column] == sentiment]
            texts = df_sentiment[text_column].dropna().tolist()
            
            if not texts:
                axes[idx].text(0.5, 0.5, f'No data for {sentiment}', 
                              ha='center', va='center', fontsize=14)
                axes[idx].axis('off')
                continue
            
            # Combine texts
            combined_text = ' '.join(str(text) for text in texts)
            
            # Generate wordcloud
            colormap = colormaps.get(sentiment.lower(), 'viridis')
            wordcloud = WordCloud(
                width=600,
                height=400,
                max_words=100,
                background_color='white',
                colormap=colormap,
                collocations=False,
                relative_scaling=0.5,
                random_state=42
            ).generate(combined_text)
            
            # Display
            axes[idx].imshow(wordcloud, interpolation='bilinear')
            axes[idx].axis('off')
            axes[idx].set_title(f'{sentiment.title()} Sentiment', 
                               fontsize=14, fontweight='bold', pad=10)
        
        plt.suptitle('Word Clouds by Sentiment', fontsize=16, fontweight='bold', y=0.98)
        plt.tight_layout()
        plt.show()
    
    def compare_wordclouds(self, text1: str, text2: str, 
                          title1: str = "Before", title2: str = "After",
                          figsize=(16, 6)) -> None:
        """
        Compare two wordclouds side by side
        
        Args:
            text1: First text
            text2: Second text
            title1: Title for first wordcloud
            title2: Title for second wordcloud
            figsize: Figure size
        """
        fig, axes = plt.subplots(1, 2, figsize=figsize)
        
        # Generate wordclouds
        wordcloud1 = WordCloud(
            width=600,
            height=400,
            max_words=100,
            background_color='white',
            colormap='Blues',
            collocations=False,
            random_state=42
        ).generate(text1 if text1 else "No data")
        
        wordcloud2 = WordCloud(
            width=600,
            height=400,
            max_words=100,
            background_color='white',
            colormap='Greens',
            collocations=False,
            random_state=42
        ).generate(text2 if text2 else "No data")
        
        # Display
        axes[0].imshow(wordcloud1, interpolation='bilinear')
        axes[0].axis('off')
        axes[0].set_title(title1, fontsize=14, fontweight='bold', pad=10)
        
        axes[1].imshow(wordcloud2, interpolation='bilinear')
        axes[1].axis('off')
        axes[1].set_title(title2, fontsize=14, fontweight='bold', pad=10)
        
        plt.tight_layout()
        plt.show()
    
    def get_top_words(self, text: str, n=20) -> Dict[str, int]:
        """
        Get top N most frequent words
        
        Args:
            text: Input text
            n: Number of top words to return
            
        Returns:
            Dictionary of word: count
        """
        # Split and count
        words = text.lower().split()
        word_counts = Counter(words)
        return dict(word_counts.most_common(n))

