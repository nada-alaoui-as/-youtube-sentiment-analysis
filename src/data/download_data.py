"""
Script to download and analyze the Reddit sentiment dataset
"""
import pandas as pd
import os
from pathlib import Path

# URLs and paths
DATASET_URL = "https://raw.githubusercontent.com/Himanshu-1703/reddit-sentiment-analysis/refs/heads/main/data/reddit.csv"
RAW_DATA_DIR = Path("data/raw")
RAW_DATA_PATH = RAW_DATA_DIR / "reddit.csv"

def download_dataset():
    """Download the Reddit sentiment dataset"""
    print("Downloading Reddit sentiment dataset...")
    
    # Create directory if it doesn't exist
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    try:
        # Download the dataset
        df = pd.read_csv(DATASET_URL)
        
        # Save to local file
        df.to_csv(RAW_DATA_PATH, index=False)
        print(f"Dataset downloaded successfully to {RAW_DATA_PATH}")
        
        return df
    
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        return None

def display_statistics(df):
    """Display dataset statistics"""
    print("\n" + "="*50)
    print("DATASET STATISTICS")
    print("="*50)
    
    # Basic info
    print(f"\nTotal comments: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    
    # Sentiment distribution
    print("\nSentiment Distribution:")
    sentiment_counts = df['category'].value_counts()
    for sentiment, count in sentiment_counts.items():
        percentage = (count / len(df)) * 100
        sentiment_label = {-1: "Negative", 0: "Neutral", 1: "Positive"}.get(sentiment, sentiment)
        print(f"   {sentiment_label:>10} ({sentiment:>2}): {count:>5} ({percentage:>5.2f}%)")
    
    # Text length statistics
    df['text_length'] = df['clean_comment'].astype(str).str.len()
    print(f"\nText Length Statistics:")
    print(f"   Average length: {df['text_length'].mean():.0f} characters")
    print(f"   Min length: {df['text_length'].min()}")
    print(f"   Max length: {df['text_length'].max()}")
    
    # Check for missing values
    print(f"\nMissing Values:")
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print("   No missing values")
    else:
        print(missing[missing > 0])
    
    # Sample comments
    print("\nSample Comments:")
    for sentiment in [-1, 0, 1]:
        sample = df[df['category'] == sentiment].iloc[0]['clean_comment']
        sentiment_label = {-1: "Negative", 0: "Neutral", 1: "Positive"}[sentiment]
        print(f"\n   {sentiment_label}: {sample[:100]}...")
    
    print("\n" + "="*50)

def main():
    """Main function"""
    # Check if dataset already exists
    if RAW_DATA_PATH.exists():
        print(f"Dataset already exists at {RAW_DATA_PATH}")
        print("Loading existing dataset...")
        df = pd.read_csv(RAW_DATA_PATH)
    else:
        df = download_dataset()
    
    if df is not None:
        display_statistics(df)
        print("\nData download and analysis complete!")
    else:
        print("\nFailed to load dataset")

if __name__ == "__main__":
    main()