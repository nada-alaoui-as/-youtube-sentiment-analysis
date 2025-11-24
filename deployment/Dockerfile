FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir huggingface_hub

# Copy application
COPY app.py .

# Create models directory
RUN mkdir -p models

# Download models from Hugging Face at runtime
RUN python -c "from huggingface_hub import hf_hub_download; \
    hf_hub_download(repo_id='Nada-al/youtube-sentiment-models', filename='sentiment_model.joblib', local_dir='/app/models'); \
    hf_hub_download(repo_id='Nada-al/youtube-sentiment-models', filename='tfidf_vectorizer.joblib', local_dir='/app/models')"

EXPOSE 7860

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
