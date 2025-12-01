"""
Cognitive Agent for Small Business Intelligence Analyst
Integrates understanding, reasoning, and interaction capabilities
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import networkx as nx


class BusinessIntelligenceAgent:
    """
    Cognitive Agent for Small Business Intelligence Analysis
    Implements the four cognitive pillars: Understand, Reason, Learn, Interact
    """
    
    def __init__(self, analyzer, preprocessor, knowledge_graph=None):
        """
        Initialize cognitive agent
        
        Args:
            analyzer: SentimentAnalyzer instance
            preprocessor: TextPreprocessor instance
            knowledge_graph: NetworkX graph (optional)
        """
        self.analyzer = analyzer
        self.preprocessor = preprocessor
        self.knowledge_graph = knowledge_graph
        self.interaction_history = []
        self.feedback_data = []  # Store user feedback for learning
        self.model_performance = {
            'accuracy_history': [],
            'feedback_count': 0,
            'last_retrain': None,
        }
        
    def process_query(self, user_input: str) -> Dict:
        """
        Complete cognitive cycle: Understand → Reason → Interact
        
        Args:
            user_input: User's text query or review
            
        Returns:
            Dictionary with analysis results and insights
        """
        # Step 1: Understand - Preprocess and analyze sentiment
        cleaned_text = self.preprocessor.preprocess(user_input)
        sentiment_result = self.analyzer.analyze(cleaned_text)
        
        # Step 2: Reason - Extract insights using knowledge graph
        insights = self._extract_insights(cleaned_text, sentiment_result)
        
        # Step 3: Interact - Generate response
        response = self._generate_response(sentiment_result, insights)
        
        result = {
            'input': user_input,
            'cleaned_text': cleaned_text,
            'sentiment': sentiment_result,
            'insights': insights,
            'response': response,
            'timestamp': pd.Timestamp.now()
        }
        
        # Store in history for learning
        self.interaction_history.append(result)
        
        return result
    
    def _extract_insights(self, text: str, sentiment_result: Dict) -> Dict:
        """
        Extract key insights from text using reasoning capabilities
        
        Args:
            text: Cleaned text
            sentiment_result: Sentiment analysis results
            
        Returns:
            Dictionary of insights
        """
        insights = {
            'key_phrases': [],
            'entities': [],
            'sentiment_strength': abs(sentiment_result.get('compound', 0)),
            'topics': []
        }
        
        # Simple keyword extraction (enhance with NER in production)
        business_keywords = {
            'service': ['service', 'delivery', 'support', 'customer service'],
            'product': ['product', 'quality', 'item', 'goods'],
            'price': ['price', 'cost', 'expensive', 'cheap', 'affordable'],
            'location': ['kampala', 'nakawa', 'kawempe', 'makindye'],
            'time': ['late', 'fast', 'quick', 'delay', 'on time']
        }
        
        text_lower = text.lower()
        for category, keywords in business_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                insights['key_phrases'].append(category)
                insights['entities'].append(category)
        
        # Query knowledge graph if available
        if self.knowledge_graph:
            insights['graph_insights'] = self._query_knowledge_graph(text_lower, sentiment_result)
        
        return insights
    
    def _query_knowledge_graph(self, text: str, sentiment_result: Dict) -> Dict:
        """
        Query knowledge graph for related insights
        
        Args:
            text: Cleaned text
            sentiment_result: Sentiment analysis results
            
        Returns:
            Dictionary of graph-based insights
        """
        if not self.knowledge_graph:
            return {}
        
        sentiment = sentiment_result.get('sentiment', 'neutral')
        graph_insights = {
            'related_entities': [],
            'sentiment_connections': []
        }
        
        # Find entities in text that exist in graph
        for node in self.knowledge_graph.nodes():
            if node in text and node != sentiment:
                graph_insights['related_entities'].append(node)
        
        # Find sentiment connections
        if sentiment in self.knowledge_graph.nodes():
            neighbors = list(self.knowledge_graph.neighbors(sentiment))
            graph_insights['sentiment_connections'] = neighbors
        
        return graph_insights
    
    def _generate_response(self, sentiment_result: Dict, insights: Dict) -> str:
        """
        Generate human-readable response (Interact pillar)
        
        Args:
            sentiment_result: Sentiment analysis results
            insights: Extracted insights
            
        Returns:
            Human-readable response string
        """
        sentiment = sentiment_result.get('sentiment', 'neutral')
        compound = sentiment_result.get('compound', 0)
        
        # Build response based on sentiment
        if sentiment == 'positive':
            response = f"✅ **Positive feedback detected** (sentiment score: {compound:.2f}). "
        elif sentiment == 'negative':
            response = f"⚠️ **Negative feedback detected** (sentiment score: {compound:.2f}). "
        else:
            response = f"➡️ **Neutral feedback** (sentiment score: {compound:.2f}). "
        
        # Add key topics
        if insights.get('key_phrases'):
            response += f"Key topics mentioned: {', '.join(insights['key_phrases'])}. "
        
        # Add business recommendations
        if sentiment == 'negative' and 'service' in insights.get('key_phrases', []):
            response += "Recommendation: Review customer service processes. "
        elif sentiment == 'positive' and 'product' in insights.get('key_phrases', []):
            response += "Recommendation: Consider highlighting this product strength in marketing. "
        
        response += "This insight can help inform your business decisions."
        
        return response
    
    def batch_process(self, texts: List[str]) -> pd.DataFrame:
        """
        Process multiple texts in batch
        
        Args:
            texts: List of text strings
            
        Returns:
            DataFrame with results
        """
        results = [self.process_query(text) for text in texts]
        return pd.DataFrame(results)
    
    def generate_report(self, df_results: pd.DataFrame) -> Dict:
        """
        Generate business intelligence report
        
        Args:
            df_results: DataFrame with analysis results
            
        Returns:
            Dictionary with report summary
        """
        report = {
            'total_reviews': len(df_results),
            'sentiment_distribution': {},
            'key_topics': [],
            'recommendations': []
        }
        
        if 'sentiment' in df_results.columns:
            report['sentiment_distribution'] = df_results['sentiment'].value_counts().to_dict()
        
        # Extract most common topics
        if 'insights' in df_results.columns:
            all_topics = []
            for insights in df_results['insights']:
                if isinstance(insights, dict) and 'key_phrases' in insights:
                    all_topics.extend(insights['key_phrases'])
            report['key_topics'] = pd.Series(all_topics).value_counts().head(5).to_dict()
        
        # Generate recommendations
        if 'sentiment' in df_results.columns:
            negative_count = (df_results['sentiment'] == 'negative').sum()
            if negative_count > len(df_results) * 0.3:
                report['recommendations'].append("High negative sentiment detected - review customer service")
        
        return report
    
    def collect_feedback(self, query_id: int, user_feedback: Dict) -> None:
        """
        Collect user feedback for learning (Learn pillar)
        
        Args:
            query_id: Index of the query in interaction_history
            user_feedback: Dictionary with feedback data
                - 'correct_sentiment': Actual sentiment label from user
                - 'helpful': Boolean indicating if response was helpful
                - 'comments': Optional comments
        """
        if query_id < len(self.interaction_history):
            feedback_entry = {
                'query_id': query_id,
                'predicted_sentiment': self.interaction_history[query_id]['sentiment'].get('sentiment'),
                'actual_sentiment': user_feedback.get('correct_sentiment'),
                'helpful': user_feedback.get('helpful', True),
                'comments': user_feedback.get('comments', ''),
                'timestamp': pd.Timestamp.now()
            }
            self.feedback_data.append(feedback_entry)
            self.model_performance['feedback_count'] += 1
            
            # Check if prediction was correct
            if feedback_entry['predicted_sentiment'] == feedback_entry['actual_sentiment']:
                self.model_performance['accuracy_history'].append(1)
            else:
                self.model_performance['accuracy_history'].append(0)
    
    def get_learning_stats(self) -> Dict:
        """
        Get learning statistics and performance metrics
        
        Returns:
            Dictionary with learning statistics
        """
        stats = {
            'total_feedback': len(self.feedback_data),
            'total_interactions': len(self.interaction_history),
            'feedback_rate': len(self.feedback_data) / max(len(self.interaction_history), 1),
            'last_retrain': self.model_performance.get('last_retrain'),
        }
        
        if self.model_performance['accuracy_history']:
            stats['accuracy'] = sum(self.model_performance['accuracy_history']) / len(self.model_performance['accuracy_history'])
            stats['recent_accuracy'] = sum(self.model_performance['accuracy_history'][-10:]) / min(10, len(self.model_performance['accuracy_history']))
        else:
            stats['accuracy'] = None
            stats['recent_accuracy'] = None
        
        return stats
    
    def should_retrain(self, min_feedback: int = 10, min_accuracy_drop: float = 0.1) -> bool:
        """
        Determine if model should be retrained based on feedback
        
        Args:
            min_feedback: Minimum number of feedback entries before considering retrain
            min_accuracy_drop: Minimum accuracy drop to trigger retrain
            
        Returns:
            Boolean indicating if retraining is recommended
        """
        if len(self.feedback_data) < min_feedback:
            return False
        
        if not self.model_performance['accuracy_history']:
            return False
        
        # Check if accuracy has dropped significantly
        if len(self.model_performance['accuracy_history']) >= 20:
            recent_acc = sum(self.model_performance['accuracy_history'][-10:]) / 10
            older_acc = sum(self.model_performance['accuracy_history'][-20:-10]) / 10
            if older_acc - recent_acc > min_accuracy_drop:
                return True
        
        # Check if overall accuracy is low
        overall_acc = sum(self.model_performance['accuracy_history']) / len(self.model_performance['accuracy_history'])
        if overall_acc < 0.7:  # Less than 70% accuracy
            return True
        
        return False
    
    def update_model_performance(self, new_accuracy: float) -> None:
        """
        Update model performance metrics after retraining
        
        Args:
            new_accuracy: New model accuracy after retraining
        """
        self.model_performance['last_retrain'] = pd.Timestamp.now()
        self.model_performance['accuracy_history'].append(new_accuracy)
    
    def export_feedback_data(self, filepath: str) -> None:
        """
        Export feedback data for analysis
        
        Args:
            filepath: Path to save feedback data
        """
        if self.feedback_data:
            df_feedback = pd.DataFrame(self.feedback_data)
            df_feedback.to_csv(filepath, index=False)
    
    def load_feedback_data(self, filepath: str) -> None:
        """
        Load feedback data from file
        
        Args:
            filepath: Path to load feedback data from
        """
        try:
            df_feedback = pd.read_csv(filepath)
            self.feedback_data = df_feedback.to_dict('records')
            self.model_performance['feedback_count'] = len(self.feedback_data)
        except FileNotFoundError:
            print(f"Feedback file not found: {filepath}")

