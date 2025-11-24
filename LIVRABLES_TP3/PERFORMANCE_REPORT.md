# Rapport de Performance du Modèle

## Métriques Globales
- **Accuracy** : 87.93%
- **F1-score (weighted)** : 0.8777
- **Temps d'inférence** : <1ms pour 50 commentaires

## Performance par Classe

| Classe | Precision | Recall | F1-Score | Support |
|--------|-----------|--------|----------|---------|
| Negative | 0.84 | 0.75 | 0.79 | 1647 |
| Neutral | 0.89 | 0.95 | 0.92 | 2529 |
| Positive | 0.89 | 0.89 | 0.89 | 3145 |

## Matrice de Confusion
```
           Predicted
         Neg  Neu  Pos
Actual Neg  1228  141  278
Actual Neu    54 2403   72
Actual Pos   186  153 2806
```

## Hyperparamètres Optimaux
- C: 10
- penalty: l2
- solver: lbfgs
- max_iter: 200

## Dataset
- Total commentaires : 36,602
- Train/Test split : 80/20
- Distribution : 43% positifs, 34.5% neutres, 22.5% négatifs
