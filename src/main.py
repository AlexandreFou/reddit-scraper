"""
Main orchestrator script for the Reddit Opportunity Scraper & Analyzer.
Coordinates Apify scraping, filtering, LangChain analysis, scoring, and reporting.
"""

import sys
import logging
import argparse
from collections import Counter
from .config import config
from .apify_client import run_apify_reddit_scraper
from .filtering import filter_and_rank_posts
from .analysis import analyze_posts_with_langchain
from .scoring import rank_opportunities
from .report import get_current_date_str, save_daily_report

# Configuration du formatage de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("RedditScraper")


def run_pipeline(dry_run: bool = False, custom_date: str = None) -> int:
    """Exécute l'ensemble du pipeline quotidien de veille entrepreneuriale."""
    if dry_run:
        config.DRY_RUN = True

    date_str = custom_date or get_current_date_str()

    logger.info("=" * 60)
    logger.info(f"[INFO] Démarrage du scraper Reddit quotidien - Date : {date_str}")
    logger.info(f"[INFO] Subreddits surveillés : {config.SUBREDDITS}")
    logger.info(f"[INFO] Modèle LLM configuré : '{config.LLM_MODEL}' (Base URL: '{config.LLM_BASE_URL or 'Default'}')")
    if config.DRY_RUN:
        logger.info("[INFO] MODE SIMULATION / DRY_RUN ACTIF (Aucun crédit externe consommé)")
    logger.info("=" * 60)

    # 1. Validation de la configuration (en mode réel)
    if not config.DRY_RUN:
        try:
            config.validate(check_llm=True, check_apify=True)
        except ValueError as err:
            logger.error(f"[ERROR] Problème de configuration :\n{err}")
            return 1

    # 2. Récupération des publications Reddit via Apify (1 seul run)
    logger.info("[INFO] Récupération des données Reddit via Apify (run unique optimisé)...")
    try:
        raw_posts = run_apify_reddit_scraper()
    except Exception as err:
        logger.error(f"[ERROR] Impossible de récupérer les publications Reddit : {err}")
        return 1

    total_scraped = len(raw_posts)
    logger.info(f"[INFO] {total_scraped} publications récupérées au total.")

    if not raw_posts:
        logger.warning("[WARN] Aucune publication trouvée aujourd'hui.")
        # Sauvegarde d'un rapport vide
        save_daily_report(
            date_str=date_str,
            opportunities=[],
            rejected_ideas=[],
            posts_scraped_total=0,
            posts_after_filtering=0,
            posts_sent_to_llm=0,
            subreddit_breakdown={}
        )
        return 0

    # Compter la répartition par subreddit
    sub_counts = Counter(p.subreddit for p in raw_posts)

    # 3. Filtrage heuristique anti-bruit (Python pur, 0 coût LLM)
    logger.info("[INFO] Filtrage heuristique des publications...")
    filtered_posts, rejected_ideas = filter_and_rank_posts(raw_posts)
    logger.info(f"[INFO] {len(filtered_posts)} publications retenues après filtrage.")

    if not filtered_posts:
        logger.warning("[WARN] Aucune publication n'a dépassé le seuil de pertinence heuristique.")
        save_daily_report(
            date_str=date_str,
            opportunities=[],
            rejected_ideas=rejected_ideas,
            posts_scraped_total=total_scraped,
            posts_after_filtering=0,
            posts_sent_to_llm=0,
            subreddit_breakdown=dict(sub_counts)
        )
        return 0

    # 4. Analyse et extraction d'opportunités via LangChain & LLM
    logger.info(f"[INFO] Envoi de {len(filtered_posts)} publications au LLM pour analyse structurée...")
    try:
        analysis_result = analyze_posts_with_langchain(filtered_posts)
    except Exception as err:
        logger.error(f"[ERROR] L'analyse LLM a échoué : {err}")
        logger.error(f"[DIAGNOSTIC] Vérifiez que le modèle '{config.LLM_MODEL}' est disponible sur votre clé/endpoint.")
        return 1

    raw_opportunities = analysis_result.opportunities
    combined_rejected = rejected_ideas + analysis_result.rejected_ideas
    logger.info(f"[INFO] {len(raw_opportunities)} opportunités extraites par le LLM.")

    # 5. Déduplication, validation des scores et classement Top N
    logger.info("[INFO] Déduplication, vérification des scores (/100) et classement...")
    ranked_opportunities = rank_opportunities(raw_opportunities)
    logger.info(f"[INFO] {len(ranked_opportunities)} opportunités retenues après déduplication.")

    # 6. Génération et écriture des rapports
    logger.info(f"[INFO] Génération du rapport Markdown et du fichier de données pour le {date_str}...")
    paths = save_daily_report(
        date_str=date_str,
        opportunities=ranked_opportunities,
        rejected_ideas=combined_rejected,
        posts_scraped_total=total_scraped,
        posts_after_filtering=len(filtered_posts),
        posts_sent_to_llm=len(filtered_posts),
        subreddit_breakdown=dict(sub_counts)
    )

    logger.info(f"[INFO] Rapport Markdown prêt : {paths['markdown_path']}")
    logger.info(f"[INFO] Données JSON enregistrées : {paths['json_path']}")
    logger.info("=" * 60)
    logger.info("[INFO] Workflow quotidien terminé avec succès !")
    logger.info("=" * 60)
    return 0


def main():
    parser = argparse.ArgumentParser(description="Reddit Opportunity Scraper & Analyzer")
    parser.add_argument(
        "--dry-run", "--mock",
        action="store_true",
        help="Exécute le pipeline en mode simulation avec données de test sans consommer de crédit"
    )
    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="Date personnalisée pour le rapport (format YYYY-MM-DD)"
    )
    args = parser.parse_args()

    exit_code = run_pipeline(dry_run=args.dry_run, custom_date=args.date)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
