# Évaluation de sécurité — OWASP Juice Shop

Examen final pratique — Sécurité des données
Licence 3 Cybersécurité — Ndaté Ndiaye (INE : N02080320222)

## 1. Description du projet

Ce dépôt contient l'ensemble des livrables techniques de l'évaluation de sécurité menée sur
l'application volontairement vulnérable **OWASP Juice Shop**, dans le cadre de l'examen
"Sécurité des données". Il comprend :

- le pipeline Jenkins d'automatisation des contrôles de sécurité (SCA + DAST) ;
- les rapports générés par les outils ;
- les captures d'écran justifiant chaque vulnérabilité et chaque correction ;
- la configuration des outils de sécurité utilisés ;
- le code et les scripts de remédiation.

## 2. Structure du dépôt

```
project/
│
├── README.md            # ce fichier
├── Jenkinsfile           # pipeline CI/CD de sécurité (6 étapes)
├── reports/               # rapports générés par Trivy et OWASP ZAP
├── screenshots/           # preuves d'exploitation et de correction (figures 1 à 7 du rapport)
├── security-config/       # fichiers de configuration des outils (Trivy, ZAP)
└── remediation/           # code corrigé + scripts de vérification (ex. verify_sqli_fix.py)
```

## 3. Comment exécuter le projet

### Prérequis

- Docker Desktop (moteur WSL2 recommandé sous Windows)
- Jenkins installé localement (ou conteneurisé)
- Python 3.x (pour les scripts de vérification dans `remediation/`)

### Lancer l'application cible (Juice Shop)

```bash
docker pull bkimminich/juice-shop
docker run -d -p 3000:3000 bkimminich/juice-shop
```

L'application est ensuite accessible sur `http://localhost:3000`.

### Lancer le pipeline de sécurité

1. Créer un job Jenkins de type "Pipeline" pointant vers ce dépôt.
2. Vérifier que le `Jenkinsfile` à la racine est bien détecté.
3. Lancer un build ("Build Now").

Le pipeline exécute automatiquement les 6 étapes suivantes :

| Étape | Rôle |
|---|---|
| 1. Checkout | Récupération du code source du dépôt |
| 2. Build / Preparation | Préparation de l'environnement / build de l'image Docker |
| 3. Security Analysis (SCA) | Analyse des dépendances et de l'image avec **Trivy** |
| 4. Additional Security Check (DAST) | Analyse dynamique de l'application en fonctionnement avec **OWASP ZAP** |
| 5. Report Generation | Génération des rapports dans `reports/` |
| 6. Notification | Notification de fin de pipeline |

## 4. Outils de sécurité utilisés

| Outil | Catégorie | Analyse | Moment d'intervention |
|---|---|---|---|
| **Trivy** | SCA + Secret Detection | Analyse statique de l'image Docker et de ses composants (CVE, secrets) | Après le build de l'image, avant déploiement |
| **OWASP ZAP** | DAST | Analyse dynamique de l'application en fonctionnement (XSS, en-têtes, configuration) | Une fois l'application démarrée et accessible sur le port 3000 |

Les rapports bruts produits par ces deux outils sont disponibles dans `reports/`.

## 5. Remédiations vérifiées

Le dossier `remediation/` contient :

- le code corrigé de `routes/login.ts` (requête SQL paramétrée, correction de la vulnérabilité
  CWE-89) ;
- le script `verify_sqli_fix.py`, utilisé pour valider par un test avant/après que
  l'injection SQL ne fonctionne plus, sans casser l'authentification légitime ;
- la configuration de restriction d'accès appliquée au répertoire `/ftp` ;
- la configuration de blocage après échecs de connexion répétés (protection contre le
  brute force, CWE-307).

Pour rejouer la vérification de la correction SQL Injection :

```bash
cd remediation
python verify_sqli_fix.py
```

## 6. Décision de déploiement

Sur la base des résultats consolidés (vulnérabilités manuelles + résultats du pipeline),
la décision retenue est **Reject Deployment** : une vulnérabilité Critical (SQL Injection)
et deux vulnérabilités High (XSS, exposition de fichiers /ftp) doivent être corrigées et
revérifiées via le pipeline avant tout déploiement en production. Le détail de l'analyse
et de la justification se trouve dans le rapport de sécurité (`reports/rapport_securite.pdf`).

## 7. Limites

Les outils automatisés (Trivy, ZAP) ne couvrent pas la logique métier de l'application et
peuvent produire des faux positifs ou manquer des vulnérabilités non documentées (faux
négatifs). L'analyse humaine reste indispensable pour l'interprétation des résultats et la
décision finale — voir la section "Analyse critique" du rapport.
