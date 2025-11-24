"""
FastAPI application for sentiment analysis
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
import joblib
from pathlib import Path
import time

# Paths
MODEL_PATH = Path("/app/models/sentiment_model.joblib")
VECTORIZER_PATH = Path("/app/models/tfidf_vectorizer.joblib")

# Initialize FastAPI app
app = FastAPI(
    title="YouTube Sentiment Analysis API",
    description="Real-time sentiment analysis for YouTube comments",
    version="1.0.0"
)

# Configure CORS (allow requests from Chrome extension)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model and vectorizer
model = None
vectorizer = None

# Pydantic models for request/response validation
class Comment(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000, description="Comment text")

class BatchRequest(BaseModel):
    comments: List[Comment] = Field(..., min_items=1, max_items=500, description="List of comments to analyze")

class SentimentResult(BaseModel):
    text: str
    sentiment: str
    sentiment_score: int
    confidence: float

class BatchResponse(BaseModel):
    results: List[SentimentResult]
    statistics: dict
    processing_time_ms: float

@app.on_event("startup")
async def load_model():
    """Load model and vectorizer on startup"""
    global model, vectorizer
    
    print("Loading model and vectorizer...")
    
    try:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
        if not VECTORIZER_PATH.exists():
            raise FileNotFoundError(f"Vectorizer not found at {VECTORIZER_PATH}")
        
        model = joblib.load(MODEL_PATH)
        vectorizer = joblib.load(VECTORIZER_PATH)
        
        print("Model and vectorizer loaded successfully!")
        
    except Exception as e:
        print(f"Error loading model: {e}")
        raise

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "YouTube Sentiment Analysis API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "predict": "/predict_batch",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    if model is None or vectorizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "vectorizer_loaded": vectorizer is not None,
        "timestamp": time.time()
    }

@app.post("/predict_batch", response_model=BatchResponse)
async def predict_batch(request: BatchRequest):
    """
    Analyze sentiment for a batch of comments
    
    Returns sentiment predictions with statistics
    """
    if model is None or vectorizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    start_time = time.time()
    
    try:
        # Extract texts from comments
        texts = [comment.text for comment in request.comments]
        
        # Vectorize texts
        X = vectorizer.transform(texts)
        
        # Predict sentiments
        predictions = model.predict(X)
        probabilities = model.predict_proba(X)
        
        # Map sentiment scores to labels
        sentiment_map = {-1: "negative", 0: "neutral", 1: "positive"}
        
        # Prepare results
        results = []
        for text, pred, proba in zip(texts, predictions, probabilities):
            results.append(SentimentResult(
                text=text[:100] + "..." if len(text) > 100 else text,  # Truncate long texts
                sentiment=sentiment_map[pred],
                sentiment_score=int(pred),
                confidence=float(max(proba))
            ))
        
        # Calculate statistics
        sentiment_counts = {
            "positive": sum(1 for r in results if r.sentiment == "positive"),
            "neutral": sum(1 for r in results if r.sentiment == "neutral"),
            "negative": sum(1 for r in results if r.sentiment == "negative")
        }
        
        total = len(results)
        statistics = {
            "total_comments": total,
            "positive": sentiment_counts["positive"],
            "neutral": sentiment_counts["neutral"],
            "negative": sentiment_counts["negative"],
            "positive_percentage": round((sentiment_counts["positive"] / total) * 100, 2),
            "neutral_percentage": round((sentiment_counts["neutral"] / total) * 100, 2),
            "negative_percentage": round((sentiment_counts["negative"] / total) * 100, 2),
            "average_confidence": round(sum(r.confidence for r in results) / total, 4)
        }
        
        processing_time = (time.time() - start_time) * 1000  # Convert to ms
        
        return BatchResponse(
            results=results,
            statistics=statistics,
            processing_time_ms=round(processing_time, 2)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
