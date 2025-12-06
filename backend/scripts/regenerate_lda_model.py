"""
Script to regenerate LDA model with current NumPy version
This fixes the NumPy version conflict issue
"""

import os
import sys
import pandas as pd
from gensim import corpora
from gensim.models import LdaModel
import numpy as np

# Add backend to path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.insert(0, backend_dir)

print("=" * 70)
print("REGENERATING LDA MODEL WITH CURRENT NUMPY VERSION")
print("=" * 70)
print(f"NumPy version: {np.__version__}")
print(f"Python version: {sys.version.split()[0]}")
print()

# Load review data
reviews_path = os.path.join(backend_dir, 'data', 'processed', 'reviews_with_sentiment.csv')
if not os.path.exists(reviews_path):
    print(f"❌ Error: {reviews_path} not found")
    print("Please run Milestone 1 and Milestone 2 notebooks first to generate the data.")
    sys.exit(1)

print(f"📊 Loading reviews from: {reviews_path}")
df_reviews = pd.read_csv(reviews_path)
print(f"✅ Loaded {len(df_reviews)} reviews")

# Prepare documents for LDA
print("\n📝 Preparing documents for topic modeling...")
if 'cleaned_text' in df_reviews.columns:
    documents = df_reviews['cleaned_text'].fillna('').astype(str).tolist()
else:
    print("⚠️  No 'cleaned_text' column found. Using 'text' column...")
    documents = df_reviews['text'].fillna('').astype(str).tolist()

# Tokenize documents (split by whitespace)
documents = [doc.split() for doc in documents if doc.strip()]
print(f"✅ Prepared {len(documents)} documents")

# Create dictionary and corpus
print("\n🔤 Creating dictionary and corpus...")
dictionary = corpora.Dictionary(documents)
dictionary.filter_extremes(no_below=2, no_above=0.5)  # Filter rare and common words
corpus = [dictionary.doc2bow(doc) for doc in documents]
print(f"✅ Dictionary created: {len(dictionary)} unique words")
print(f"✅ Corpus created: {len(corpus)} documents")

# Use 10 topics as specified
num_topics = 10
print(f"📊 Using {num_topics} topics for LDA model")

print(f"\n🎯 Training LDA model with {num_topics} topics...")
print("   This may take a few minutes...")

# Train LDA model
lda_model = LdaModel(
    corpus=corpus,
    id2word=dictionary,
    num_topics=num_topics,
    random_state=42,
    passes=10,
    alpha='auto',
    per_word_topics=True
)

print(f"✅ LDA model trained successfully!")

# Display topics
print(f"\n📊 Top {num_topics} topics identified:")
for idx, topic in lda_model.print_topics(-1, num_words=5):
    print(f"   Topic {idx}: {topic}")

# Save model
model_path = os.path.join(backend_dir, 'data', 'models', 'lda_model')
os.makedirs(os.path.dirname(model_path), exist_ok=True)

print(f"\n💾 Saving LDA model to: {model_path}")
lda_model.save(model_path)
print("✅ LDA model saved successfully!")

print("\n" + "=" * 70)
print("✅ MODEL REGENERATION COMPLETE!")
print("=" * 70)
print(f"Model saved at: {model_path}")
print(f"NumPy version used: {np.__version__}")
print("\nYou can now refresh the Topic Analysis page in the frontend.")
print("=" * 70)

