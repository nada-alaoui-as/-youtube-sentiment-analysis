# TP3 : Projet ML Complet - YouTube Sentiment Analysis
## ALAOUI Nada - INDIA 2026

---

## ��� Contenu des Livrables

### 1. Code Source
- **GitHub** : https://github.com/nada-alaoui-as/youtube-sentiment-analysis
- Structure MLOps complète
- Scripts data pipeline, entraînement, API, extension

### 2. Modèles Entraînés
- **Hugging Face Models** : https://huggingface.co/Nada-al/youtube-sentiment-models
- `sentiment_model.joblib` : Modèle Logistic Regression
- `tfidf_vectorizer.joblib` : Vectoriseur TF-IDF
- Voir `PERFORMANCE_REPORT.md` pour les métriques

### 3. API Déployée
- **URL Live** : https://nada-al-youtube-sentiment-api.hf.space
- Endpoints : `/health`, `/predict_batch`
- Documentation : `API_DOCUMENTATION.md`
- Déployée sur Hugging Face Spaces avec Docker

### 4. Extension Chrome
- **Fichier** : `chrome-extension.zip`
- Instructions : `INSTALLATION_EXTENSION.md`
- Interface moderne avec statistiques, filtres, dark mode

### 5. Performance

#### Métriques Globales
- ✅ **Accuracy** : 87.93% (requis: >80%)
- ✅ **F1-score** : 0.8777 (requis: >0.75)
- ✅ **Temps d'inférence** : <1ms pour 50 commentaires (requis: <100ms)

#### Dataset
- 36,602 commentaires (après nettoyage)
- Distribution : 43% positifs, 34.5% neutres, 22.5% négatifs
- Source : Reddit Sentiment Analysis

### 6. Architecture Technique
```
┌─────────────────────┐
│  Chrome Extension   │  (Frontend : JavaScript, HTML, CSS)
│   (popup.html)      │
└──────────┬──────────┘
           │ HTTP POST
           ▼
┌─────────────────────┐
│   FastAPI Backend   │  (Python, uvicorn)
│  Hugging Face Space │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   ML Model Engine   │  (scikit-learn)
│ TF-IDF + Logistic   │
│    Regression       │
└─────────────────────┘
```

### 7. Technologies Utilisées

**Backend :**
- Python 3.10
- FastAPI 0.121.3
- scikit-learn 1.7.2
- pandas, numpy

**ML :**
- TF-IDF (5000 features, ngrams 1-2)
- Logistic Regression (C=10, L2 penalty)
- GridSearchCV pour hyperparameter tuning

**Frontend :**
- JavaScript (Chrome Extension API)
- HTML5/CSS3
- Fetch API pour communication backend

**DevOps :**
- Docker (containerization)
- Git/GitHub (version control)
- Hugging Face Spaces (déploiement)
- Git LFS (stockage modèles)

---

## ��� Démonstration

Pour tester le système complet :

1. Installer l'extension (voir `INSTALLATION_EXTENSION.md`)
2. Ouvrir une vidéo YouTube
3. Lancer l'analyse
4. Observer les résultats en temps réel

---

## ���‍��� Auteur

**Nada ALAOUI**
- ENSAM Rabat - INDIA 2026
- Email : alaouinada49@gmail.com
- GitHub : https://github.com/nada-alaoui-as
- Hugging Face : https://huggingface.co/Nada-al

---

Date de soumission : 24 Novembre 2025
Module : Virtualisation & Cloud Computing
Professeur : Maria Zemzami
