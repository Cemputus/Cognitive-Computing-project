"""
Robustness Validation Utilities
Provides validation and quality checks for model inputs and outputs
"""

import pandas as pd
import numpy as np
import re
from typing import Dict, List, Tuple, Optional


class RobustnessValidator:
    """Validates inputs and outputs for robustness"""
    
    def __init__(self):
        """Initialize validator"""
        self.min_text_length = 3
        self.max_text_length = 10000
        self.min_words = 1
        self.max_words = 2000
        
    def validate_text_input(self, text: str) -> Tuple[bool, Optional[str]]:
        """
        Validate text input for sentiment analysis
        
        Args:
            text: Text string to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if text is None:
            return False, "Text cannot be None"
        
        if not isinstance(text, str):
            try:
                text = str(text)
            except:
                return False, "Text must be convertible to string"
        
        text = text.strip()
        
        if len(text) == 0:
            return False, "Text cannot be empty"
        
        if len(text) < self.min_text_length:
            return False, f"Text too short (minimum {self.min_text_length} characters)"
        
        if len(text) > self.max_text_length:
            return False, f"Text too long (maximum {self.max_text_length} characters)"
        
        word_count = len(text.split())
        if word_count < self.min_words:
            return False, f"Text has too few words (minimum {self.min_words} word)"
        
        if word_count > self.max_words:
            return False, f"Text has too many words (maximum {self.max_words} words)"
        
        return True, None
    
    def validate_sentiment_result(self, result: Dict) -> Tuple[bool, Optional[str]]:
        """
        Validate sentiment analysis result
        
        Args:
            result: Sentiment analysis result dictionary
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not isinstance(result, dict):
            return False, "Result must be a dictionary"
        
        required_keys = ['sentiment']
        for key in required_keys:
            if key not in result:
                return False, f"Missing required key: {key}"
        
        sentiment = result.get('sentiment')
        valid_sentiments = ['positive', 'negative', 'neutral']
        if sentiment not in valid_sentiments:
            return False, f"Invalid sentiment: {sentiment}. Must be one of {valid_sentiments}"
        
        # Validate confidence if present
        if 'confidence' in result:
            confidence = result['confidence']
            if not isinstance(confidence, (int, float)):
                return False, "Confidence must be a number"
            if confidence < 0 or confidence > 1:
                return False, "Confidence must be between 0 and 1"
        
        return True, None
    
    def check_data_quality(self, df: pd.DataFrame, text_column: str = 'text') -> Dict:
        """
        Check data quality metrics
        
        Args:
            df: DataFrame to check
            text_column: Name of text column
            
        Returns:
            Dictionary with quality metrics
        """
        metrics = {
            'total_rows': len(df),
            'missing_values': 0,
            'empty_strings': 0,
            'too_short': 0,
            'too_long': 0,
            'quality_score': 0.0
        }
        
        if text_column not in df.columns:
            metrics['error'] = f"Column '{text_column}' not found"
            return metrics
        
        # Check missing values
        metrics['missing_values'] = df[text_column].isna().sum()
        
        # Check empty strings
        metrics['empty_strings'] = (df[text_column].astype(str).str.strip() == '').sum()
        
        # Check text length
        if metrics['total_rows'] > 0:
            text_lengths = df[text_column].astype(str).str.len()
            metrics['too_short'] = (text_lengths < self.min_text_length).sum()
            metrics['too_long'] = (text_lengths > self.max_text_length).sum()
            
            # Calculate quality score
            valid_rows = metrics['total_rows'] - metrics['missing_values'] - metrics['empty_strings'] - metrics['too_short'] - metrics['too_long']
            metrics['quality_score'] = valid_rows / metrics['total_rows'] if metrics['total_rows'] > 0 else 0.0
        
        return metrics
    
    def detect_anomalies(self, results: List[Dict]) -> List[Dict]:
        """
        Detect anomalous results that might indicate errors
        
        Args:
            results: List of sentiment analysis results
            
        Returns:
            List of detected anomalies
        """
        anomalies = []
        
        for i, result in enumerate(results):
            # Check for low confidence
            if 'confidence' in result:
                if result['confidence'] < 0.3:
                    anomalies.append({
                        'index': i,
                        'type': 'low_confidence',
                        'message': f"Very low confidence ({result['confidence']:.2f})",
                        'result': result
                    })
            
            # Check for conflicting signals
            if 'compound' in result and 'sentiment' in result:
                compound = result['compound']
                sentiment = result['sentiment']
                if (compound > 0.1 and sentiment == 'negative') or \
                   (compound < -0.1 and sentiment == 'positive'):
                    anomalies.append({
                        'index': i,
                        'type': 'conflicting_signals',
                        'message': f"Compound score ({compound:.2f}) conflicts with sentiment ({sentiment})",
                        'result': result
                    })
            
            # Check for errors
            if 'error' in result:
                anomalies.append({
                    'index': i,
                    'type': 'error',
                    'message': result['error'],
                    'result': result
                })
        
        return anomalies
    
    def get_robustness_report(self, results: List[Dict]) -> Dict:
        """
        Generate robustness report for batch results
        
        Args:
            results: List of sentiment analysis results
            
        Returns:
            Dictionary with robustness metrics
        """
        if not results:
            return {'error': 'No results provided'}
        
        total = len(results)
        valid_results = [r for r in results if 'error' not in r]
        error_count = total - len(valid_results)
        
        # Calculate confidence statistics
        confidences = [r.get('confidence', 0) for r in valid_results if 'confidence' in r]
        
        report = {
            'total_results': total,
            'valid_results': len(valid_results),
            'error_count': error_count,
            'error_rate': error_count / total if total > 0 else 0,
            'average_confidence': np.mean(confidences) if confidences else 0,
            'min_confidence': np.min(confidences) if confidences else 0,
            'max_confidence': np.max(confidences) if confidences else 0,
            'low_confidence_count': sum(1 for c in confidences if c < 0.5),
            'high_confidence_count': sum(1 for c in confidences if c >= 0.7),
        }
        
        # Detect anomalies
        anomalies = self.detect_anomalies(valid_results)
        report['anomalies'] = anomalies
        report['anomaly_count'] = len(anomalies)
        
        # Calculate robustness score (0-1)
        robustness_score = 1.0
        robustness_score -= report['error_rate'] * 0.5  # Penalize errors
        robustness_score -= (report['low_confidence_count'] / total) * 0.3 if total > 0 else 0  # Penalize low confidence
        robustness_score -= (len(anomalies) / total) * 0.2 if total > 0 else 0  # Penalize anomalies
        report['robustness_score'] = max(0, min(1, robustness_score))
        
        return report

