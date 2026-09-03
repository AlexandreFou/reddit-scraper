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
    APIFY_ACTOR_ID: str = raw_actor if raw_actor and "/" in raw_actor else "trudax/reddit-scraper"
    
    # Subreddits à surveiller (supporte séparateurs virgule, espace ou point-virgule et retire 'r/')
    SUBREDDITS_RAW: str = os.getenv("SUBREDDITS", "Entrepreneur,startups,smallbusiness")
    SUBREDDITS: List[str] = [
        re.sub(r"^/?r/", "", s.strip())
        for s in re.split(r"[,;\s]+", SUBREDDITS_RAW)
        if s.strip()
    ]
    
    # Nombre max d'éléments à récupérer par subreddit dans le run unique
    POSTS_PER_SUBREDDIT: int = int(os.getenv("POSTS_PER_SUBREDDIT", "30"))
    
    # --- LLM / OmniRoute / OpenAI / Gemini Settings ---
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "").strip()
    LLM_BASE_URL: str = os.getenv("LLM_BASE_URL", "").strip()
    LLM_MODEL: str = os.getenv("LLM_MODEL", "").strip() or "gpt-4o-mini"
    
    # --- Filtering & Pipeline Limits ---
    MAX_POSTS_FOR_LLM: int = int(os.getenv("MAX_POSTS_FOR_LLM", "30"))
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
