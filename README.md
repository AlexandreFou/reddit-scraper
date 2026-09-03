# 🚀 Reddit Opportunity Scraper & Analyzer

> **Pipeline automatisé quotidien : Reddit (Apify) → Pré-filtrage heuristique → Analyse structurée (LangChain) → Scoring sur 100 → GitHub Actions & Rapports Markdown.**

Ce projet extrait chaque matin les publications des 24 dernières heures sur **r/Entrepreneur**, **r/startups** et **r/smallbusiness**, filtre le spam et le contenu motivationnel, puis analyse les véritables problèmes exprimés par des entrepreneurs pour en dégager les **meilleures opportunités commerciales concrètes**, le tout sans jamais dépasser les quotas gratuits d'Apify.

---

## 📋 Table des matières

- [1. Architecture & Fonctionnement](#1-architecture--fonctionnement)
- [2. Grille de Notation (100 points)](#2-grille-de-notation-100-points)
- [3. Structure du Projet](#3-structure-du-projet)
- [4. Installation Locale](#4-installation-locale)
- [5. Configuration des Variables (.env)](#5-configuration-des-variables-env)
- [6. Configuration GitHub Actions & Secrets](#6-configuration-github-actions--secrets)
- [7. Déclenchement Automatique & Manuel](#7-déclenchement-automatique--manuel)
- [8. Dépannage & Erreurs Fréquentes](#8-dépannage--erreurs-fréquentes)
- [9. Initialisation du Repository Git](#9-initialisation-du-repository-git)

---

## 1. Architecture & Fonctionnement

```text
┌────────────────────────────────────────────────────────┐
│             GitHub Actions (06:00 UTC / 07:00 Paris)   │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
    ┌──────────────────────────────────────────────────┐
    │  1 SEUL RUN APIFY QUOTIDIEN (trudax/reddit-scraper)│
    │  - r/Entrepreneur                                │
    │  - r/startups                                    │
    │  - r/smallbusiness                               │
    └───────────────────────┬──────────────────────────┘
                            │ ~90 posts bruts
                            ▼
    ┌──────────────────────────────────────────────────┐
    │  PRÉ-FILTRAGE HEURISTIQUE EN PYTHON (0 coût LLM) │
    │  - Élimine : memes, grindset, pubs, airdrops     │
    │  - Détecte : "hate using", "Excel", "would pay"  │
    └───────────────────────┬──────────────────────────┘
                            │ ~25-30 posts qualifiés
                            ▼
    ┌──────────────────────────────────────────────────┐
    │  CHAÎNE LANGCHAIN + SORTIE STRUCTURÉE (Pydantic)  │
    │  - Fournisseur configurable (OmniRoute / OpenAI) │
    │  - Distingue faits observés vs hypothèses        │
    │  - Zéro hallucination de métriques               │
    └───────────────────────┬──────────────────────────┘
                            │
                            ▼
    ┌──────────────────────────────────────────────────┐
    │  DÉDUPLICATION, SCORING & CLASSEMENT TOP 10      │
    │  - Regroupement des signaux concordants          │
    │  - Validation de la grille sur 100 points        │
    └───────────────────────┬──────────────────────────┘
                            │
                            ▼
    ┌──────────────────────────────────────────────────┐
    │  SAUVEGARDE & COMMIT AUTOMATIQUE                 │
    │  - reports/YYYY-MM-DD.md (Rapport Markdown)      │
    │  - data/YYYY-MM-DD.json (Données structurées)    │
    └──────────────────────────────────────────────────┘
```

### 💡 Optimisation stricte des coûts :
1. **Un seul lancement Apify par jour** : les 3 subreddits sont passés en bloc (`startUrls`) dans un run unique, évitant la multiplication des sessions de calcul.
2. **Commentaires plafonnés à 5** : capture les objections et signaux de demande sans saturer la bande passante.
3. **Pré-filtrage Python local** : élimine 60% à 70% du bruit avant tout appel LLM.
4. **Modèle configurable** : compatible avec `gpt-4o-mini`, Gemini ou OmniRoute pour un coût de quelques centimes par mois.

---

## 2. Grille de Notation (100 points)

Chaque idée est évaluée selon la grille stricte du cahier des charges :

| Critère | Poids | Description |
|:---|:---:|:---|
| **Intensité du problème** | /20 | Le problème est-il réellement douloureux, coûteux et chronophage ? |
| **Demande observable** | /20 | Des utilisateurs cherchent-ils ou demandent-ils activement une solution ? |
| **Potentiel de monétisation** | /15 | Volonté et capacité de payer crédibles (B2B, SaaS, récurrent) |
| **Taille / niche du marché** | /15 | Le problème concerne-t-il un segment adressable suffisant ? |
| **Concurrence / saturation** | /10 | Marché accessible, mal servi par les logiciels existants |
| **Facilité de lancement** | /10 | Un solo-fondateur ou une petite équipe peut-il sortir un MVP en quelques semaines ? |
| **Potentiel IA / automatisation** | /10 | L'automatisation ou l'IA apporte-t-elle un gain d'efficacité décisif ? |
| **TOTAL** | **/100** | Somme exacte des 7 composantes |

---

## 3. Structure du Projet

```text
RedditScraper/
├── .github/
│   └── workflows/
│       └── daily.yml         # Workflow GitHub Actions quotidien & dispatch manuel
├── src/
│   ├── __init__.py
│   ├── config.py             # Chargement et validation de la configuration
│   ├── models.py             # Schémas Pydantic (Post, Scoring, Opportunity, Report)
│   ├── apify_client.py       # Exécution d'Apify en run unique + mock offline
│   ├── filtering.py          # Filtrage anti-bruit heuristique haute performance
│   ├── analysis.py           # Chaîne LangChain & structured output
│   ├── scoring.py            # Calcul du score /100 et déduplication intelligente
│   ├── report.py             # Générateur Markdown (tableaux, fiches, rejets)
│   └── main.py               # Orchestrateur CLI principal
├── tests/
│   ├── __init__.py
│   ├── test_models.py        # Validation des schémas Pydantic
│   ├── test_filtering.py     # Tests de filtrage de spam et motivation
│   └── test_scoring.py       # Tests du scoring /100 et de la déduplication
├── reports/
│   └── 2026-09-03.md         # Rapports quotidiens archivés
├── data/
│   └── 2026-09-03.json       # Données JSON brutes archivées
├── .env.example              # Modèle documenté de configuration
├── .gitignore                # Protection contre le commit de tokens ou secrets
├── requirements.txt          # Dépendances Python verrouillées
└── README.md                 # Documentation complète
```

---

## 4. Installation Locale

### Cloner le repository :
```bash
git clone https://github.com/AlexandreFou/RedditScraper.git
cd RedditScraper
```

### Créer un environnement virtuel :
- **Sur Linux / macOS :**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```
- **Sur Windows (PowerShell) :**
  ```powershell
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  ```

### Installer les dépendances :
```bash
pip install -r requirements.txt
```

### Lancer les tests unitaires (hors ligne, 0 crédit) :
```bash
pytest -v
# ou avec unittest standard :
python3 -m unittest discover -s tests -p "test_*.py" -v
```

### Tester l'exécution en mode simulation (Dry Run) :
```bash
python -m src.main --dry-run
```
Cette commande génère immédiatement un rapport d'exemple dans `reports/` sans utiliser de token Apify ni de clé LLM.

---

## 5. Configuration des Variables (.env)

Copiez `.env.example` en `.env` :
```bash
cp .env.example .env
```

Éditez les variables dans `.env` :

```env
# Token Apify (obtenu sur https://console.apify.com/)
APIFY_API_TOKEN=apify_api_votre_token

# Acteur Apify optimisé pour le run unique multi-subreddits
APIFY_ACTOR_ID=trudax/reddit-scraper

# Subreddits à surveiller (séparés par une virgule)
SUBREDDITS=Entrepreneur,startups,smallbusiness
POSTS_PER_SUBREDDIT=30

# Fournisseur LLM (Compatible OpenAI, OmniRoute, OpenRouter, Gemini)
LLM_API_KEY=votre_cle_api

# Base URL (Optionnel - pour OmniRoute, OpenRouter, etc.)
# Exemples :
# OmniRoute : https://api.omniroute.ai/v1
# OpenRouter : https://openrouter.ai/api/v1
# Gemini OpenAI compat : https://generativelanguage.googleapis.com/v1beta/openai/
LLM_BASE_URL=

# Modèle LLM (configurable pour éviter l'erreur "400 Invalid model")
LLM_MODEL=gpt-4o-mini

# Limites de traitement
MAX_POSTS_FOR_LLM=30
TOP_OPPORTUNITIES=10
TIMEZONE=Europe/Paris
```

---

## 6. Configuration GitHub Actions & Secrets

Pour que le bot s'exécute automatiquement chaque matin sur GitHub :

1. Allez sur votre repository GitHub : **https://github.com/AlexandreFou/RedditScraper**
2. Cliquez sur **Settings** (en haut à droite du repo).
3. Dans le menu de gauche, sélectionnez **Secrets and variables** > **Actions**.
4. Cliquez sur **New repository secret** et ajoutez :

| Nom du Secret | Description | Exemple de valeur |
|:---|:---|:---|
| `APIFY_API_TOKEN` | Token API de votre compte Apify | `apify_api_...` |
| `LLM_API_KEY` | Clé d'API du fournisseur d'IA | `sk-...` ou votre clé OmniRoute |
| `LLM_BASE_URL` *(optionnel)* | URL de base si vous utilisez OmniRoute | `https://api.omniroute.ai/v1` |
| `LLM_MODEL` *(optionnel)* | Modèle exact autorisé par votre compte | `gpt-4o-mini` |

5. Vérifiez les permissions de workflow :
   - Allez dans **Settings** > **Actions** > **General**.
   - Sous **Workflow permissions**, cochez **Read and write permissions**.
   - Cliquez sur **Save**.

---

## 7. Déclenchement Automatique & Manuel

- **Automatique :** Chaque matin à **06:00 UTC** (soit 07:00 en hiver / 08:00 en été à Paris), GitHub Actions déclenche le scraper, génère le rapport et effectue un `git commit` & `git push` sur la branche `main`.
- **Manuel :** 
  1. Allez dans l'onglet **Actions** de votre repository.
  2. Sélectionnez le workflow **Daily Reddit Opportunities Scraper**.
  3. Cliquez sur **Run workflow** > **Run workflow**.

---

## 8. Dépannage & Erreurs Fréquentes

### ❌ `API Error: 400 Invalid model. Please select a different model to continue.`
- **Cause :** Le nom du modèle renseigné dans `LLM_MODEL` n'est pas reconnu ou non supporté par votre clé / fournisseur (OmniRoute, OpenRouter).
- **Solution :** Modifiez la variable `LLM_MODEL` dans votre fichier `.env` ou dans les secrets GitHub pour spécifier un modèle valide (ex: `gpt-4o-mini`, `claude-3-5-haiku-20241022`, ou le nom de modèle OmniRoute attribué).

### ❌ `APIFY_API_TOKEN is missing`
- **Cause :** Le token Apify n'est pas détecté.
- **Solution :** Vérifiez que `APIFY_API_TOKEN` est bien déclaré dans votre `.env` local ou dans GitHub Secrets sous le nom exact.

### ❌ `git push` échoue dans GitHub Actions
- **Cause :** L'action GitHub n'a pas les droits d'écriture sur le repo.
- **Solution :** Activez **Read and write permissions** dans **Settings > Actions > General > Workflow permissions**.

---

## 9. Initialisation du Repository Git

Pour envoyer ce projet vers votre repository vide `https://github.com/AlexandreFou/RedditScraper.git` :

```bash
# 1. Initialiser le dépôt git local si ce n'est pas déjà fait
git init

# 2. Configurer la branche principale
git branch -M main

# 3. Lier au repository GitHub distant
git remote add origin https://github.com/AlexandreFou/RedditScraper.git

# 4. Ajouter tous les fichiers (le .gitignore protège les tokens)
git add .

# 5. Créer le commit initial
git commit -m "feat: initial commit - Reddit Opportunity Scraper with Apify, LangChain & GitHub Actions"

# 6. Pousser vers GitHub
git push -u origin main
```

Une fois poussé, vous retrouverez vos rapports quotidiens directement dans le dossier `reports/` chaque matin ! 🎉
