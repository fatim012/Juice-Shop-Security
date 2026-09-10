# Configuration Trivy

Commande utilisée dans le pipeline Jenkins :
trivy image --format json --output trivy-report.json bkimminich/juice-shop

Type d'analyse : SCA (dépendances) + Secret Detection
Aucune règle personnalisée (.trivyignore) n'a été appliquée pour cet examen.
Configuration par défaut de l'outil.
