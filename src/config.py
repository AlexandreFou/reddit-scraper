"""
Configuration module for RedditScraper.
Loads environment variables from .env or system environment with sane defaults.
"""

import os
import re
from typing import List

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class Config:
    # --- Apify Settings ---
    APIFY_API_TOKEN: str = os.getenv("APIFY_API_TOKEN", "").strip()
    raw_actor = os.getenv("APIFY_ACTOR_ID", "").strip()
    # Note : trudax/reddit-scraper requiert désormais une location mensuelle payante ($20/mois).
    # harshmaur/reddit-scraper-pro utilise le pay-per-event standard sans abonnement et fonctionne directement avec les crédits gratuits Apify.
    if not raw_actor or "trudax/reddit-scraper" in raw_actor or "/" not in raw_actor:
        APIFY_ACTOR_ID: str = "harshmaur/reddit-scraper-pro"
    else:
        APIFY_ACTOR_ID: str = raw_actor
    
    # Subreddits à surveiller (supporte séparateurs virgule, espace ou point-virgule et retire 'r/')
    SUBREDDITS_RAW: str = os.getenv("SUBREDDITS", "Entrepreneur,startups,smallbusiness")
    SUBREDDITS: List[str] = [
        re.sub(r"^/?r/", "", s.strip())
        for s in re.split(r"[,;\s]+", SUBREDDITS_RAW)
        if s.strip()
    ]
    
    # Nombre max d'éléments à récupérer par subreddit dans le run unique
    POSTS_PER_SUBREDDIT: int = int(os.getenv("POSTS_PER_SUBREDDIT", "30"))
    
    # --- LLM / Groq / OmniRoute / OpenAI Settings ---
    raw_api_key = os.getenv("GROQ_API_KEY", "").strip() or os.getenv("LLM_API_KEY", "").strip()
    LLM_API_KEY: str = raw_api_key.strip("'\"")
    
    raw_base_url = os.getenv("LLM_BASE_URL", "").strip().strip("'\"")
    if raw_base_url.endswith("/chat/completions"):
        raw_base_url = raw_base_url[:-len("/chat/completions")].rstrip("/")
    
    # Auto-détection Groq via la clé d'API (commence toujours par 'gsk_')
    if LLM_API_KEY.startswith("gsk_") and (not raw_base_url or "openai.com" in raw_base_url):
        raw_base_url = "https://api.groq.com/openai/v1"
        
    LLM_BASE_URL: str = raw_base_url.rstrip("/")
    
    raw_model = os.getenv("LLM_MODEL", "").strip().strip("'\"")
    is_groq = "groq.com" in LLM_BASE_URL or LLM_API_KEY.startswith("gsk_")
    if is_groq:
        # Modèles Groq recommandés (Groq a retiré Llama 3.1/3.3 du free tier le 16 août 2026 au profit de Qwen 3.6 et GPT-OSS)
        if not raw_model or raw_model in ("gpt-4o-mini", "gpt-4o", "llama-3.3-70b-versatile", "llama-3.1-8b-instant", "gemma2-9b-it", "mixtral-8x7b-32768"):
            raw_model = "qwen/qwen3.6-27b"
    else:
        if not raw_model:
            raw_model = "gpt-4o-mini"
    LLM_MODEL: str = raw_model
    
    # --- Filtering & Pipeline Limits ---
    # Sur Groq Free tier, la limite TPM est de 8000 tokens/minute.
    # 15 posts soigneusement qualifiés consomment ~3000 tokens et évitent l'erreur 413 Payload Too Large.
    default_max_posts = 15 if is_groq else 30
    MAX_POSTS_FOR_LLM: int = int(os.getenv("MAX_POSTS_FOR_LLM", str(default_max_posts)))
    TOP_OPPORTUNITIES: int = int(os.getenv("TOP_OPPORTUNITIES", "10"))
    
    # --- Date & Timezone ---
    TIMEZONE: str = os.getenv("TIMEZONE", "Europe/Paris").strip()
    
    # Mode test/mock (pour éviter de consommer du quota lors du dev ou des tests)
    DRY_RUN: bool = os.getenv("DRY_RUN", "false").lower() in ("true", "1", "yes")

    @classmethod
    def validate(cls, check_llm: bool = True, check_apify: bool = True) -> None:
        """Vérifie que les clés obligatoires sont définies pour une exécution réelle."""
        errors = []
        if check_apify and not cls.APIFY_API_TOKEN and not cls.DRY_RUN:
            errors.append(
                "APIFY_API_TOKEN is missing. Please set it in .env or GitHub Secrets."
            )
        if check_llm and not cls.LLM_API_KEY and not cls.DRY_RUN:
            errors.append(
                f"LLM_API_KEY is missing. Model is set to '{cls.LLM_MODEL}'. "
                "Please configure LLM_API_KEY in .env or GitHub Secrets."
            )
        if errors:
            raise ValueError("\n".join(errors))


config = Config()
