"""
Data Collection Utilities for Small Business Intelligence Analyst
Includes web scraping and synthetic data generation
"""

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import warnings
warnings.filterwarnings('ignore')


class DataCollector:
    """Collect customer review data from various sources"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Diverse review templates for synthetic data
        self.review_templates = {
            'positive': [
                "Great service! Very fast delivery in Kampala. Highly recommend!",
                "Amazing quality products. Will definitely buy again from this shop.",
                "Excellent customer support. They responded quickly to my questions.",
                "Best prices in Nakawa area. Great value for money.",
                "Love the product quality. Fast shipping and good packaging.",
                "Outstanding service! The staff was very helpful and friendly.",
                "Top-notch quality. Exceeded my expectations completely.",
                "Great experience overall. Will be a returning customer.",
                "Fast delivery, good quality, fair prices. What more could you ask for?",
                "Excellent business! Highly professional and reliable.",
                "Great products at affordable prices. Very satisfied with my purchase.",
                "Quick response time and excellent customer care. Highly recommended!",
                "Best shop in Kawempe. Quality products and great service.",
                "Amazing experience! The product arrived on time and in perfect condition.",
                "Outstanding quality and service. Will definitely shop here again.",
                "Great value for money. Fast delivery and excellent packaging.",
                "Professional service and high-quality products. Very happy!",
                "Excellent communication and fast delivery. Highly satisfied!",
                "Best customer service I've experienced. Products are top quality.",
                "Great prices and even better service. Highly recommend this business!",
                "Fast shipping, good quality, and excellent customer support.",
                "Love shopping here! Always get great deals and quality products.",
                "Outstanding business! Professional, reliable, and customer-focused.",
                "Great experience from start to finish. Will shop here again!",
                "Excellent products and service. Best in the area!",
                "Very satisfied with my purchase. Great quality and fast delivery.",
                "Amazing service! The team went above and beyond to help me.",
                "Top quality products at reasonable prices. Highly recommended!",
                "Great business with excellent customer care. Very professional.",
                "Best shopping experience! Quality products and great prices."
            ],
            'negative': [
                "Product was damaged on arrival. Poor packaging quality.",
                "Very slow delivery. Took over a week to arrive in Kampala.",
                "Customer service was unresponsive. Had to wait days for a reply.",
                "Product quality was disappointing. Not as described on the website.",
                "Overpriced compared to other shops in Nakawa area.",
                "Poor customer service. Staff was rude and unhelpful.",
                "Product broke after just one week of use. Very poor quality.",
                "Delivery was delayed multiple times. Very frustrating experience.",
                "Not satisfied with the product. Quality is below expectations.",
                "Terrible experience. Would not recommend this business to anyone.",
                "Product arrived damaged and customer service refused to help.",
                "Very disappointed with the quality. Not worth the money paid.",
                "Slow response time and poor communication from the business.",
                "Product was different from what was advertised. Misleading description.",
                "Poor packaging led to damaged goods. Very unprofessional.",
                "Customer service is terrible. No one responds to complaints.",
                "Overpriced products with low quality. Not good value for money.",
                "Delivery issues. Package arrived late and damaged.",
                "Very disappointed. Product quality is poor and service is worse.",
                "Would not buy from here again. Poor experience overall.",
                "Product didn't work as expected. Waste of money.",
                "Terrible customer service. No help when I had an issue.",
                "Poor quality products. Broke within days of purchase.",
                "Very slow delivery and unresponsive customer support.",
                "Not satisfied at all. Product quality is below standard.",
                "Disappointing experience. Would not recommend this shop.",
                "Poor value for money. Better options available elsewhere.",
                "Customer service needs major improvement. Very unprofessional.",
                "Product was defective but they refused to refund. Bad business.",
                "Worst shopping experience. Poor quality and terrible service."
            ],
            'neutral': [
                "Product is okay. Nothing special but serves its purpose.",
                "Average quality. Price is reasonable for what you get.",
                "Delivery was on time. Product is as expected.",
                "Standard service. No complaints but nothing exceptional either.",
                "Product works fine. Decent quality for the price paid.",
                "Okay experience. Nothing to complain about but not impressed either.",
                "Average product quality. Meets basic expectations.",
                "Fair prices and acceptable quality. Nothing outstanding.",
                "Product is functional. Does what it's supposed to do.",
                "Standard delivery time. Product quality is average.",
                "Okay service. Nothing special but gets the job done.",
                "Average experience overall. Product is fine but not great.",
                "Decent quality products. Price is fair for what you receive.",
                "Product works as expected. No major issues or complaints.",
                "Standard business service. Acceptable but not exceptional.",
                "Average product quality. Meets basic needs adequately.",
                "Okay delivery time. Product is functional and usable.",
                "Fair value for money. Quality is acceptable but not premium.",
                "Standard experience. Product does what it needs to do.",
                "Average quality. Nothing special but nothing wrong either.",
                "Product is fine. Meets expectations without exceeding them.",
                "Decent service. No major complaints but nothing impressive.",
                "Okay product quality. Price matches the value received.",
                "Standard delivery. Product works but quality is average.",
                "Fair experience overall. Nothing exceptional but acceptable.",
                "Average quality products. Functional but not impressive.",
                "Okay service. Product meets basic requirements.",
                "Standard quality. Nothing to complain about or praise.",
                "Decent value. Product works as expected.",
                "Average experience. Product is functional and adequate."
            ]
        }
        
        # Business-related keywords for variety
        self.business_keywords = [
            'restaurant', 'shop', 'store', 'service', 'delivery', 'product',
            'quality', 'price', 'customer', 'staff', 'business', 'order',
            'purchase', 'shipping', 'packaging', 'support', 'experience'
        ]
        
        # Kampala locations
        self.locations = [
            'Kampala', 'Nakawa', 'Kawempe', 'Makindye', 'Lubaga', 
            'Central', 'Kololo', 'Ntinda', 'Bukoto', 'Muyenga'
        ]
        
        # Data sources
        self.sources = ['Facebook', 'Google', 'Twitter', 'Instagram', 'Website', 'WhatsApp']
    
    def generate_synthetic_reviews(self, n_reviews: int = 5000) -> pd.DataFrame:
        """
        Generate diverse synthetic customer reviews
        
        Args:
            n_reviews: Number of reviews to generate
            
        Returns:
            DataFrame with reviews
        """
        print(f"Generating {n_reviews} synthetic reviews...")
        
        reviews = []
        start_date = datetime(2023, 1, 1)
        
        # Determine sentiment distribution (realistic: 60% positive, 25% neutral, 15% negative)
        sentiment_dist = {
            'positive': int(n_reviews * 0.60),
            'neutral': int(n_reviews * 0.25),
            'negative': int(n_reviews * 0.15)
        }
        
        review_id = 1
        
        for sentiment, count in sentiment_dist.items():
            templates = self.review_templates[sentiment]
            for _ in range(count):
                # Select random template
                base_text = random.choice(templates)
                
                # Add variation
                if random.random() < 0.3:  # 30% chance to add location
                    location_mention = random.choice(self.locations)
                    base_text = f"{base_text} Located in {location_mention}."
                
                if random.random() < 0.2:  # 20% chance to add business keyword
                    keyword = random.choice(self.business_keywords)
                    base_text = f"{base_text} Great {keyword}!"
                
                # Generate date (spread over time)
                days_offset = random.randint(0, 730)  # Last 2 years
                review_date = start_date + timedelta(days=days_offset)
                
                reviews.append({
                    'review_id': review_id,
                    'text': base_text,
                    'date': review_date.strftime('%Y-%m-%d'),
                    'source': random.choice(self.sources),
                    'location': random.choice(self.locations),
                    'sentiment_label': sentiment  # For validation
                })
                review_id += 1
        
        # Shuffle reviews
        random.shuffle(reviews)
        
        # Reset review_id after shuffle
        for i, review in enumerate(reviews, 1):
            review['review_id'] = i
        
        df = pd.DataFrame(reviews)
        print(f"✅ Generated {len(df)} synthetic reviews")
        return df
    
    def scrape_reddit_reviews(self, subreddit: str = 'reviews', limit: int = 100) -> Optional[pd.DataFrame]:
        """
        Attempt to scrape reviews from Reddit (public data)
        Note: Respects rate limits and uses public API
        
        Args:
            subreddit: Subreddit to scrape
            limit: Maximum number of posts
            
        Returns:
            DataFrame with reviews or None if scraping fails
        """
        print(f"Attempting to scrape reviews from Reddit (r/{subreddit})...")
        
        try:
            # Use Reddit's public JSON API (no authentication needed for public data)
            url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                posts = data.get('data', {}).get('children', [])
                
                reviews = []
                for post in posts:
                    post_data = post.get('data', {})
                    title = post_data.get('title', '')
                    selftext = post_data.get('selftext', '')
                    
                    # Combine title and text
                    review_text = f"{title} {selftext}".strip()
                    
                    if len(review_text) > 20:  # Filter very short posts
                        reviews.append({
                            'review_id': len(reviews) + 1,
                            'text': review_text,
                            'date': datetime.fromtimestamp(
                                post_data.get('created_utc', time.time())
                            ).strftime('%Y-%m-%d'),
                            'source': 'Reddit',
                            'location': 'Online',  # Reddit doesn't have location
                            'sentiment_label': 'unknown'
                        })
                
                if reviews:
                    df = pd.DataFrame(reviews)
                    print(f"✅ Scraped {len(df)} reviews from Reddit")
                    return df
                else:
                    print("⚠️ No reviews found on Reddit")
                    return None
            else:
                print(f"⚠️ Reddit API returned status code: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"⚠️ Error scraping Reddit: {e}")
            print("   Continuing with synthetic data only...")
            return None
    
    def scrape_news_api(self, query: str = "customer review", limit: int = 50) -> Optional[pd.DataFrame]:
        """
        Attempt to get review-related articles from news API
        Falls back gracefully if API is unavailable
        
        Args:
            query: Search query
            limit: Maximum articles
            
        Returns:
            DataFrame or None
        """
        print("Attempting to fetch review-related articles...")
        
        # Note: This would require an API key for most news APIs
        # For now, we'll skip this and use synthetic data
        print("⚠️ News API requires authentication. Skipping...")
        return None
    
    def collect_all_data(self, n_synthetic: int = 5000, 
                        try_reddit: bool = True, 
                        reddit_limit: int = 200) -> pd.DataFrame:
        """
        Collect data from all available sources and merge
        
        Args:
            n_synthetic: Number of synthetic reviews to generate
            try_reddit: Whether to attempt Reddit scraping
            reddit_limit: Maximum Reddit posts to scrape
            
        Returns:
            Merged DataFrame with all reviews
        """
        print("=" * 60)
        print("Starting Data Collection")
        print("=" * 60)
        
        all_dataframes = []
        
        # 1. Generate synthetic data
        df_synthetic = self.generate_synthetic_reviews(n_synthetic)
        all_dataframes.append(df_synthetic)
        print(f"✅ Synthetic data: {len(df_synthetic)} reviews")
        
        # 2. Try to scrape Reddit (if enabled)
        if try_reddit:
            time.sleep(1)  # Be respectful with rate limiting
            df_reddit = self.scrape_reddit_reviews(limit=reddit_limit)
            if df_reddit is not None:
                all_dataframes.append(df_reddit)
                print(f"✅ Reddit data: {len(df_reddit)} reviews")
        
        # 3. Merge all dataframes
        if len(all_dataframes) > 1:
            print("\nMerging all data sources...")
            df_merged = pd.concat(all_dataframes, ignore_index=True)
            
            # Reset review_id to be sequential
            df_merged['review_id'] = range(1, len(df_merged) + 1)
            
            print(f"✅ Merged dataset: {len(df_merged)} total reviews")
        else:
            df_merged = all_dataframes[0]
            print(f"✅ Final dataset: {len(df_merged)} reviews")
        
        # Display summary
        print("\n" + "=" * 60)
        print("Data Collection Summary")
        print("=" * 60)
        print(f"Total reviews: {len(df_merged)}")
        print(f"\nSource distribution:")
        print(df_merged['source'].value_counts())
        print(f"\nLocation distribution:")
        print(df_merged['location'].value_counts())
        if 'sentiment_label' in df_merged.columns:
            print(f"\nSentiment distribution:")
            print(df_merged['sentiment_label'].value_counts())
        
        return df_merged

