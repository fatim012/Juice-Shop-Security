# Configuration OWASP ZAP

Commande utilisée dans le pipeline Jenkins :
zap-baseline.py -t http://host.docker.internal:3000 -r zap-report.html

Type d'analyse : DAST (baseline scan)
Cible : application OWASP Juice Shop en fonctionnement sur le port 3000
Configuration par défaut de l'outil (aucun contexte personnalisé).
