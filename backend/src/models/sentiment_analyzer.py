"""
Enhanced Sentiment Analysis Module for Small Business Intelligence Analyst
Implements multiple sentiment analysis approaches with robustness improvements
"""

import pandas as pd
import numpy as np
import re
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Optional import for transformer-based sentiment analysis
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    pipeline = None


class SentimentAnalyzer:
    """Enhanced sentiment analysis using multiple approaches with robustness features"""
    
    def __init__(self, method='ensemble', use_ensemble=True):
        """
        Initialize sentiment analyzer with enhanced robustness
        
        Args:
            method: 'vader', 'textblob', 'transformer', or 'ensemble'
            use_ensemble: If True, uses ensemble of methods for better accuracy
        """
        self.method = method
        self.use_ensemble = use_ensemble
        
        # Initialize all available analyzers for ensemble
        try:
            self.vader_analyzer = SentimentIntensityAnalyzer()
            self.vader_available = True
        except Exception as e:
            print(f"⚠️ VADER not available: {e}")
            self.vader_available = False
        
        self.textblob_available = True  # TextBlob doesn't need initialization
        
        self.transformer_available = False
        if (method == 'transformer' or use_ensemble) and TRANSFORMERS_AVAILABLE:
            try:
                self.transformer_analyzer = pipeline("sentiment-analysis", 
                                        model="nlptown/bert-base-multilingual-uncased-sentiment")
                self.transformer_available = True
            except Exception as e:
                print(f"⚠️ Transformer model not available: {e}")
                self.transformer_available = False
        elif (method == 'transformer' or use_ensemble) and not TRANSFORMERS_AVAILABLE:
            print("⚠️ Transformers library not installed. Transformer-based sentiment analysis will be disabled.")
            self.transformer_available = False
        
        # Sarcasm detection patterns
        self.sarcasm_patterns = [
            r'\b(oh|yeah|sure|right)\s+(great|wonderful|amazing|perfect)\b',
            r'\b(not|never)\s+(good|great|excellent|amazing)\b',
            r'\b(just|only)\s+(what|exactly)\s+(i|we)\s+(needed|wanted)\b',
            r'\b(thanks|thank you)\s+(for|a lot)\b.*\b(delay|problem|issue)\b',
        ]
        
        # Confidence thresholds
        self.confidence_thresholds = {
            'high': 0.7,
            'medium': 0.5,
            'low': 0.3
        }
    
    def _detect_sarcasm(self, text):
        """
        Detect potential sarcasm in text using pattern matching
        
        Args:
            text: Text string to check
            
        Returns:
            Boolean indicating if sarcasm is detected
        """
        text_lower = text.lower()
        for pattern in self.sarcasm_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return True
        return False
    
    def _handle_short_text(self, text, min_words=5):
        """
        Handle very short text by using more lenient thresholds
        
        Args:
            text: Text string
            min_words: Minimum words for normal processing
            
        Returns:
            Adjusted threshold multiplier
        """
        word_count = len(text.split())
        if word_count < min_words:
            # Use more lenient thresholds for short text
            return 0.7  # Reduce threshold by 30%
        return 1.0
    
    def _calculate_confidence(self, scores, method='vader'):
        """
        Calculate confidence score for prediction
        
        Args:
            scores: Sentiment scores dictionary
            method: Method used ('vader', 'textblob', 'ensemble')
            
        Returns:
            Confidence score (0-1)
        """
        if method == 'vader':
            # Confidence based on compound score magnitude
            compound = abs(scores.get('compound', 0))
            # Also consider how clear the classification is
            pos = scores.get('pos', 0)
            neg = scores.get('neg', 0)
            neu = scores.get('neu', 0)
            
            # High confidence if one sentiment dominates
            max_sentiment = max(pos, neg, neu)
            confidence = (compound * 0.6) + (max_sentiment * 0.4)
            return min(confidence, 1.0)
        
        elif method == 'textblob':
            polarity = abs(scores.get('polarity', 0))
            subjectivity = scores.get('subjectivity', 0)
            # Higher confidence for strong polarity and low subjectivity
            confidence = polarity * (1 - subjectivity * 0.5)
            return min(confidence, 1.0)
        
        elif method == 'ensemble':
            # Average confidence from multiple methods
            confidences = []
            if 'vader_confidence' in scores:
                confidences.append(scores['vader_confidence'])
            if 'textblob_confidence' in scores:
                confidences.append(scores['textblob_confidence'])
            if confidences:
                return np.mean(confidences)
            return 0.5  # Default medium confidence
        
        return 0.5
    
    def analyze_vader(self, text):
        """Analyze sentiment using VADER with enhanced robustness"""
        if not self.vader_available:
            raise ValueError("VADER analyzer not available")
        
        if not text or len(text.strip()) == 0:
            return {
                'compound': 0.0,
                'positive': 0.0,
                'negative': 0.0,
                'neutral': 1.0,
                'sentiment': 'neutral',
                'confidence': 0.0,
                'warning': 'Empty text input'
            }
        
        try:
            scores = self.vader_analyzer.polarity_scores(text)
            
            # Adjust thresholds for short text
            threshold_multiplier = self._handle_short_text(text)
            threshold = 0.05 * threshold_multiplier
            
            # Detect sarcasm
            is_sarcastic = self._detect_sarcasm(text)
            
            # Determine sentiment
            compound = scores['compound']
            if is_sarcastic and compound > 0:
                # If sarcastic and positive, likely negative
                sentiment = 'negative'
                compound = -abs(compound)  # Flip to negative
            else:
                sentiment = 'positive' if compound >= threshold else \
                          'negative' if compound <= -threshold else 'neutral'
            
            # Calculate confidence
            confidence = self._calculate_confidence(scores, 'vader')
            
            result = {
                'compound': compound,
                'pos': scores['pos'],
                'neu': scores['neu'],
                'neg': scores['neg'],
                'positive': scores['pos'],
                'negative': scores['neg'],
                'neutral': scores['neu'],
                'sentiment': sentiment,
                'confidence': confidence,
                'is_sarcastic': is_sarcastic,
                'word_count': len(text.split())
            }
            
            # Add warning for low confidence
            if confidence < self.confidence_thresholds['low']:
                result['warning'] = 'Low confidence prediction - text may be ambiguous'
            elif confidence < self.confidence_thresholds['medium']:
                result['warning'] = 'Medium confidence prediction'
            
            return result
            
        except Exception as e:
            # Fallback to neutral with error flag
            return {
                'compound': 0.0,
                'positive': 0.0,
                'negative': 0.0,
                'neutral': 1.0,
                'sentiment': 'neutral',
                'confidence': 0.0,
                'error': str(e),
                'warning': 'Error in VADER analysis'
            }
    
    def analyze_textblob(self, text):
        """Analyze sentiment using TextBlob with enhanced robustness"""
        if not text or len(text.strip()) == 0:
            return {
                'polarity': 0.0,
                'subjectivity': 0.0,
                'sentiment': 'neutral',
                'confidence': 0.0,
                'warning': 'Empty text input'
            }
        
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Adjust threshold for short text
            threshold_multiplier = self._handle_short_text(text)
            threshold = 0.1 * threshold_multiplier
            
            # Determine sentiment
            sentiment = 'positive' if polarity > threshold else \
                       'negative' if polarity < -threshold else 'neutral'
            
            # Calculate confidence
            scores = {'polarity': polarity, 'subjectivity': subjectivity}
            confidence = self._calculate_confidence(scores, 'textblob')
            
            result = {
                'polarity': polarity,
                'subjectivity': subjectivity,
                'sentiment': sentiment,
                'confidence': confidence,
                'word_count': len(text.split())
            }
            
            # Add warning for low confidence
            if confidence < self.confidence_thresholds['low']:
                result['warning'] = 'Low confidence prediction'
            
            return result
            
        except Exception as e:
            return {
                'polarity': 0.0,
                'subjectivity': 0.0,
                'sentiment': 'neutral',
                'confidence': 0.0,
                'error': str(e),
                'warning': 'Error in TextBlob analysis'
            }
    
    def analyze_transformer(self, text):
        """Analyze sentiment using transformer model with enhanced robustness"""
        if not self.transformer_available:
            raise ValueError("Transformer analyzer not available")
        
        if not text or len(text.strip()) == 0:
            return {
                'sentiment': 'neutral',
                'confidence': 0.0,
                'warning': 'Empty text input'
            }
        
        if not self.transformer_available or not hasattr(self, 'transformer_analyzer'):
            return {
                'sentiment': 'neutral',
                'confidence': 0.0,
                'warning': 'Transformer model not available'
            }
        
        try:
            result = self.transformer_analyzer(text)[0]
            label = result['label']
            score = result['score']
            
            # Map label to sentiment
            sentiment_map = {
                '1 star': 'negative',
                '2 star': 'negative',
                '3 star': 'neutral',
                '4 star': 'positive',
                '5 star': 'positive',
                'very_negative': 'negative',
                'negative': 'negative',
                'neutral': 'neutral',
                'positive': 'positive',
                'very_positive': 'positive'
            }
            
            sentiment = sentiment_map.get(label, 'neutral')
            confidence = score  # Transformer score is already a confidence
            
            return {
                'label': label,
                'score': score,
                'sentiment': sentiment,
                'confidence': confidence,
                'word_count': len(text.split())
            }
            
        except Exception as e:
            return {
                'sentiment': 'neutral',
                'confidence': 0.0,
                'error': str(e),
                'warning': 'Error in transformer analysis'
            }
    
    def analyze_ensemble(self, text):
        """
        Analyze sentiment using ensemble of multiple methods for robustness
        
        Args:
            text: Text string to analyze
            
        Returns:
            Dictionary with ensemble sentiment scores and label
        """
        results = []
        weights = []
        
        # Get results from all available methods
        if self.vader_available:
            try:
                vader_result = self.analyze_vader(text)
                results.append(vader_result)
                weights.append(0.5)  # VADER gets higher weight
            except:
                pass
        
        if self.textblob_available:
            try:
                textblob_result = self.analyze_textblob(text)
                results.append(textblob_result)
                weights.append(0.3)
            except:
                pass
        
        if self.transformer_available:
            try:
                transformer_result = self.analyze_transformer(text)
                results.append(transformer_result)
                weights.append(0.2)
            except:
                pass
        
        if not results:
            # Fallback if no methods available
            return {
                'sentiment': 'neutral',
                'confidence': 0.0,
                'error': 'No sentiment analyzers available',
                'warning': 'Unable to analyze sentiment'
            }
        
        # Normalize weights
        total_weight = sum(weights)
        weights = [w / total_weight for w in weights]
        
        # Aggregate sentiment predictions
        sentiment_votes = {'positive': 0, 'negative': 0, 'neutral': 0}
        total_confidence = 0
        
        for i, result in enumerate(results):
            sentiment = result.get('sentiment', 'neutral')
            confidence = result.get('confidence', 0.5)
            weight = weights[i]
            
            sentiment_votes[sentiment] += weight * confidence
            total_confidence += confidence * weight
        
        # Determine final sentiment (majority vote weighted by confidence)
        final_sentiment = max(sentiment_votes, key=sentiment_votes.get)
        final_confidence = total_confidence
        
        # Aggregate scores
        compound_scores = [r.get('compound', 0) for r in results if 'compound' in r]
        polarity_scores = [r.get('polarity', 0) for r in results if 'polarity' in r]
        
        ensemble_result = {
            'sentiment': final_sentiment,
            'confidence': final_confidence,
            'method': 'ensemble',
            'methods_used': len(results),
            'word_count': len(text.split()) if text else 0
        }
        
        # Add aggregated scores
        if compound_scores:
            ensemble_result['compound'] = np.mean(compound_scores)
        if polarity_scores:
            ensemble_result['polarity'] = np.mean(polarity_scores)
        
        # Add individual method results for transparency
        ensemble_result['vader_result'] = results[0] if self.vader_available and results else None
        ensemble_result['textblob_result'] = results[1] if self.textblob_available and len(results) > 1 else None
        
        # Add warnings
        if final_confidence < self.confidence_thresholds['low']:
            ensemble_result['warning'] = 'Low confidence - ensemble prediction may be uncertain'
        elif final_confidence < self.confidence_thresholds['medium']:
            ensemble_result['warning'] = 'Medium confidence prediction'
        
        # Check for sarcasm
        if any(r.get('is_sarcastic', False) for r in results):
            ensemble_result['is_sarcastic'] = True
            ensemble_result['warning'] = 'Potential sarcasm detected - interpretation may be uncertain'
        
        return ensemble_result
    
    def analyze(self, text):
        """
        Analyze sentiment of text using configured method with enhanced robustness
        
        Args:
            text: Text string to analyze
            
        Returns:
            Dictionary with sentiment scores, label, and confidence
        """
        # Validate input
        if not text or (isinstance(text, str) and len(text.strip()) == 0):
            return {
                'sentiment': 'neutral',
                'confidence': 0.0,
                'error': 'Empty or invalid input',
                'warning': 'Cannot analyze empty text'
            }
        
        # Convert to string if needed
        if not isinstance(text, str):
            text = str(text)
        
        # Use ensemble if requested
        if self.use_ensemble or self.method == 'ensemble':
            return self.analyze_ensemble(text)
        
        # Use single method
        if self.method == 'vader':
            return self.analyze_vader(text)
        elif self.method == 'textblob':
            return self.analyze_textblob(text)
        elif self.method == 'transformer':
            return self.analyze_transformer(text)
        else:
            # Fallback to ensemble
            return self.analyze_ensemble(text)
    
    def analyze_batch(self, texts, show_progress=False):
        """
        Analyze sentiment for multiple texts with enhanced error handling
        
        Args:
            texts: List or Series of text strings
            show_progress: If True, shows progress for large batches
            
        Returns:
            DataFrame with sentiment analysis results
        """
        if not texts or len(texts) == 0:
            return pd.DataFrame()
        
        results = []
        errors = []
        
        for i, text in enumerate(texts):
            try:
                result = self.analyze(text)
                result['index'] = i
                results.append(result)
                
                if show_progress and (i + 1) % 100 == 0:
                    print(f"Processed {i + 1}/{len(texts)} texts...")
                    
            except Exception as e:
                # Log error but continue processing
                error_result = {
                    'sentiment': 'neutral',
                    'confidence': 0.0,
                    'error': str(e),
                    'index': i,
                    'warning': 'Error processing this text'
                }
                results.append(error_result)
                errors.append((i, str(e)))
        
        if errors and show_progress:
            print(f"⚠️ Encountered {len(errors)} errors during batch processing")
        
        df_results = pd.DataFrame(results)
        
        # Add error summary if there were errors
        if errors:
            df_results['has_error'] = df_results['error'].notna()
        
        return df_results

