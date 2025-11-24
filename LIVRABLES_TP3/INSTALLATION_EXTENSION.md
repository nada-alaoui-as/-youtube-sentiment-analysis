# Installation de l'Extension Chrome

## Étapes d'installation

1. Décompressez le fichier `chrome-extension.zip`

2. Ouvrez Google Chrome et allez sur `chrome://extensions/`

3. Activez le **"Mode développeur"** (toggle en haut à droite)

4. Cliquez sur **"Charger l'extension non empaquetée"**

5. Sélectionnez le dossier décompressé `chrome-extension`

6. L'extension est maintenant installée !

## Configuration

1. Cliquez sur l'icône de l'extension dans Chrome
2. Dans le champ "API URL", entrez : `https://nada-al-youtube-sentiment-api.hf.space`
3. Cliquez "Test Connection" pour vérifier
4. Si ✅, vous êtes prêt !

## Utilisation

1. Ouvrez une vidéo YouTube avec des commentaires
2. Scrollez pour charger quelques commentaires
3. Cliquez sur l'icône de l'extension
4. Cliquez "Analyze Comments"
5. Attendez quelques secondes
6. Les résultats s'affichent avec statistiques et détails

## Fonctionnalités

- ✅ Extraction automatique des commentaires YouTube
- ✅ Analyse de sentiment en temps réel via API cloud
- ✅ Statistiques globales (%, répartition)
- ✅ Liste détaillée avec confiance par commentaire
- ✅ Filtres par sentiment (positif/neutre/négatif)
- ✅ Mode sombre/clair
- ✅ Export des résultats en CSV

## Dépannage

**Erreur "No comments found"** : Scrollez sur la page YouTube pour charger les commentaires

**Erreur "Connection failed"** : Vérifiez que l'API URL est correcte et que vous avez internet

**Extension ne s'affiche pas** : Vérifiez que le mode développeur est activé dans chrome://extensions/
