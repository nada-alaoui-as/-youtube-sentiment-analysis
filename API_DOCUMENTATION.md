# Documentation API

## Base URL
`https://nada-al-youtube-sentiment-api.hf.space`

## Endpoints

### GET /health
Vérifie l'état de l'API

**Exemple de réponse :**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "vectorizer_loaded": true
}
```

### POST /predict_batch
Analyse le sentiment de plusieurs commentaires

**Request Body :**
```json
{
  "comments": [
    {"text": "This is amazing!"},
    {"text": "Not good at all"}
  ]
}
```

**Response :**
```json
{
  "results": [...],
  "statistics": {
    "total_comments": 2,
    "positive": 1,
    "neutral": 0,
    "negative": 1,
    "positive_percentage": 50.0,
    ...
  },
  "processing_time_ms": 2.01
}
```
