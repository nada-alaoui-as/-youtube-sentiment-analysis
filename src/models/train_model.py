"""
Script to train and evaluate sentiment analysis models
"""
import pandas as pd
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score
import time

# Paths
PROCESSED_DATA_PATH = Path("data/processed/reddit_clean.csv")
MODELS_DIR = Path("models")
VECTORIZER_PATH = MODELS_DIR / "tfidf_vectorizer.joblib"
MODEL_PATH = MODELS_DIR / "sentiment_model.joblib"

def load_data():
    """Load cleaned dataset"""
    print("Loading cleaned dataset...")
    df = pd.read_csv(PROCESSED_DATA_PATH)
    print(f"   Loaded {len(df)} comments")
    return df

def split_data(df, test_size=0.2, random_state=42):
    """Split data into train and test sets"""
    print(f"\nSplitting data (train: {int((1-test_size)*100)}%, test: {int(test_size*100)}%)...")
    
    X = df['clean_comment']
    y = df['category']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    print(f"   Train size: {len(X_train)}")
    print(f"   Test size: {len(X_test)}")
    
    return X_train, X_test, y_train, y_test

def create_vectorizer(X_train):
    """Create and fit TF-IDF vectorizer"""
    print("\nCreating TF-IDF vectorizer...")
    
    vectorizer = TfidfVectorizer(
        max_features=5000,      # Top 5000 words
        ngram_range=(1, 2),     # Unigrams and bigrams
        min_df=2,               # Ignore terms appearing in < 2 documents
        max_df=0.9,             # Ignore terms appearing in > 90% documents
        strip_accents='unicode'
    )
    
    print("   Fitting vectorizer on training data...")
    X_train_vec = vectorizer.fit_transform(X_train)
    
    print(f"   Vocabulary size: {len(vectorizer.vocabulary_)}")
    print(f"   Feature matrix shape: {X_train_vec.shape}")
    
    return vectorizer, X_train_vec

def train_model(X_train_vec, y_train):
    """Train Logistic Regression model with hyperparameter tuning"""
    print("\nTraining Logistic Regression model...")
    
    # Define parameter grid for GridSearchCV
    param_grid = {
        'C': [0.1, 1, 10],
        'penalty': ['l2'],
        'solver': ['lbfgs'],
        'max_iter': [200]
    }
    
    # Create base model
    lr = LogisticRegression(random_state=42)
    
    # Grid search with cross-validation
    print("   Performing GridSearchCV (this may take a moment)...")
    grid_search = GridSearchCV(
        lr, param_grid, cv=3, scoring='f1_weighted', n_jobs=-1, verbose=1
    )
    
    start_time = time.time()
    grid_search.fit(X_train_vec, y_train)
    training_time = time.time() - start_time
    
    print(f"\n   Training completed in {training_time:.2f} seconds")
    print(f"   Best parameters: {grid_search.best_params_}")
    print(f"   Best cross-validation F1-score: {grid_search.best_score_:.4f}")
    
    return grid_search.best_estimator_

def evaluate_model(model, vectorizer, X_test, y_test):
    """Evaluate model on test set"""
    print("\nEvaluating model on test set...")
    
    # Transform test data
    X_test_vec = vectorizer.transform(X_test)
    
    # Make predictions
    y_pred = model.predict(X_test_vec)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    f1_weighted = f1_score(y_test, y_pred, average='weighted')
    
    print(f"\n   Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"    F1-score (weighted): {f1_weighted:.4f}")
    
    # Classification report
    print("\nClassification Report:")
    target_names = ['Negative', 'Neutral', 'Positive']
    print(classification_report(y_test, y_pred, target_names=target_names))
    
    # Confusion matrix
    print("Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred, labels=[-1, 0, 1])
    print("           Predicted")
    print("         Neg  Neu  Pos")
    for i, row in enumerate(cm):
        label = ['Neg', 'Neu', 'Pos'][i]
        print(f"Actual {label}  {row[0]:>4} {row[1]:>4} {row[2]:>4}")
    
    # Inference time test
    print("\nTesting inference speed...")
    test_comments = X_test.iloc[:50]
    test_vec = vectorizer.transform(test_comments)
    
    start = time.time()
    predictions = model.predict(test_vec)
    inference_time = (time.time() - start) * 1000  # Convert to ms
    
    print(f"   Time for 50 comments: {inference_time:.2f}ms")
    print(f"   Average per comment: {inference_time/50:.2f}ms")
    
    return accuracy, f1_weighted

def save_models(model, vectorizer):
    """Save trained model and vectorizer"""
    print("\nSaving model and vectorizer...")
    
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    
    print(f"   Model saved to {MODEL_PATH}")
    print(f"   Vectorizer saved to {VECTORIZER_PATH}")

def main():
    """Main training pipeline"""
    print("="*60)
    print("SENTIMENT ANALYSIS MODEL TRAINING PIPELINE")
    print("="*60)
    
    # Load data
    df = load_data()
    
    # Split data
    X_train, X_test, y_train, y_test = split_data(df)
    
    # Create vectorizer
    vectorizer, X_train_vec = create_vectorizer(X_train)
    
    # Train model
    model = train_model(X_train_vec, y_train)
    
    # Evaluate model
    accuracy, f1_score = evaluate_model(model, vectorizer, X_test, y_test)
    
    # Check if model meets requirements
    print("\n" + "="*60)
    print("PERFORMANCE REQUIREMENTS CHECK:")
    print("="*60)
    
    accuracy_pass = "✅" if accuracy >= 0.80 else "❌"
    f1_pass = "✅" if f1_score >= 0.75 else "❌"
    
    print(f"   {accuracy_pass} Accuracy >= 80%: {accuracy*100:.2f}%")
    print(f"   {f1_pass} F1-score >= 0.75: {f1_score:.4f}")
    
    if accuracy >= 0.80 and f1_score >= 0.75:
        print("\nModel meets all performance requirements!")
        save_models(model, vectorizer)
    else:
        print("\nModel doesn't meet requirements yet.")
        print("   Consider: more data, different features, or model tuning")
        # Save anyway for experimentation
        save_models(model, vectorizer)
    
    print("\n" + "="*60)
    print("TRAINING PIPELINE COMPLETE!")
    print("="*60)

if __name__ == "__main__":
    main()