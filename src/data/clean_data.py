"""
Script to clean and preprocess the Reddit sentiment dataset
"""
import pandas as pd
import re
from pathlib import Path

# Paths
RAW_DATA_PATH = Path("data/raw/reddit.csv")
PROCESSED_DATA_DIR = Path("data/processed")
PROCESSED_DATA_PATH = PROCESSED_DATA_DIR / "reddit_clean.csv"

def clean_text(text):
    """Clean individual text comment"""
    if pd.isna(text):
        return ""
    
    text = str(text)
    
    # Remove URLs
    text = re.sub(r'http\S+|www\.\S+', '', text)
    
    # Remove mentions (@username)
    text = re.sub(r'@\w+', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text

def clean_dataset():
    """Clean the entire dataset"""
    print("Loading raw dataset...")
    df = pd.read_csv(RAW_DATA_PATH)
    print(f"   Initial size: {len(df)} comments")
    
    # Remove missing values
    print("\nRemoving missing values...")
    df = df.dropna(subset=['clean_comment'])
    print(f"   After removing NaN: {len(df)} comments")
    
    # Clean text
    print("\nCleaning text (removing URLs, mentions, extra spaces)...")
    df['clean_comment'] = df['clean_comment'].apply(clean_text)
    
    # Remove very short comments (< 3 characters)
    print("\nFiltering short comments...")
    df['text_length'] = df['clean_comment'].str.len()
    df = df[df['text_length'] >= 3]
    print(f"   After filtering: {len(df)} comments")
    
    # Remove duplicates
    print("\nRemoving duplicates...")
    initial_len = len(df)
    df = df.drop_duplicates(subset=['clean_comment'])
    removed = initial_len - len(df)
    print(f"   Removed {removed} duplicates")
    print(f"   Final size: {len(df)} comments")
    
    # Display final distribution
    print("\nFinal Sentiment Distribution:")
    sentiment_counts = df['category'].value_counts()
    for sentiment, count in sentiment_counts.items():
        percentage = (count / len(df)) * 100
        sentiment_label = {-1: "Negative", 0: "Neutral", 1: "Positive"}.get(sentiment, sentiment)
        print(f"   {sentiment_label:>10} ({sentiment:>2}): {count:>5} ({percentage:>5.2f}%)")
    
    # Save cleaned data
    print(f"\nSaving cleaned data to {PROCESSED_DATA_PATH}...")
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    df[['clean_comment', 'category']].to_csv(PROCESSED_DATA_PATH, index=False)
    
    print("\nData cleaning complete!")
    return df

if __name__ == "__main__":
    clean_dataset()