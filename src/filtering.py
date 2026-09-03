"""
Lightweight heuristic filtering module for Reddit posts.
Executes pure Python rules to eliminate spam, motivational fluff, and irrelevant posts
BEFORE calling the LLM, reducing LLM token consumption and costs drastically.
"""

import re
import logging
from typing import List, Tuple
from .config import config
from .models import RedditPost, RejectedIdea

logger = logging.getLogger("RedditScraper.Filtering")

# Mots-clés et expressions indiquant un signal fort d'opportunité entrepreneuriale
HIGH_INTENT_PATTERNS = [
    r"\bis there an? (?:tool|software|app|platform|solution|service)\b",
    r"\bi wish there (?:was|were)\b",
    r"\bdoes anyone know (?:a good|an alternative|how to)\b",
    r"\bhow do you (?:handle|solve|manage|automate|track)\b",
    r"\bi hate using\b",
    r"\blooking for (?:software|a tool|an alternative|a solution)\b",
    r"\bwould (?:gladly )?pay\b",
    r"\bwhy doesn'?t anyone\b",
    r"\bwe spend (?:hours|days|too much time)\b",
    r"\bwe currently use excel\b",
    r"\bour biggest (?:problem|pain point|challenge|headache)\b",
    r"\bdoes anyone have a solution\b",
    r"\bmanual process\b",
    r"\bnightmare to manage\b",
    r"\bclunky\b",
    r"\berror[- ]prone\b",
    r"\btime consuming\b",
    r"\bpricing is ridiculous\b",
    r"\bfrustrated with\b",
]

# Patterns de bruit à éliminer impérativement
NOISE_PATTERNS = [
    r"\bcheck out my\b",
    r"\bjoin my telegram\b",
    r"\bfree crypto\b",
    r"\bdrop your link\b",
    r"\bshoutout\b",
    r"\bmotivational monday\b",
    r"\bquote of the day\b",
    r"\bgrindset\b",
    r"\bnever give up\b",
    r"\brate my landing page\b",
    r"\bfree tokens?\b",
    r"\bairdrop\b",
    r"\bdiscord server\b",
    r"\bupvote for upvote\b",
    r"\bfollow for follow\b",
]

COMPILED_HIGH_INTENT = [re.compile(p, re.IGNORECASE) for p in HIGH_INTENT_PATTERNS]
COMPILED_NOISE = [re.compile(p, re.IGNORECASE) for p in NOISE_PATTERNS]


def calculate_relevance_score(post: RedditPost) -> Tuple[float, str]:
    """
    Calcule un score heuristique pour un post (0 à 100).
    Retourne (score, raison_ou_statut).
    """
    combined_text = f"{post.title} {post.selftext} {' '.join(post.comments)}".lower()

    # 1. Rejet immédiat si trop court
    if len(post.title.split()) < 4 and len(post.selftext.split()) < 5:
        return 0.0, "Post trop court ou vide pour identifier un besoin"

    # 2. Rejet des spams et posts d'auto-promo évidents
    for noise_regex in COMPILED_NOISE:
        if noise_regex.search(combined_text):
            return 0.0, "Spam, auto-promotion ou contenu purement motivationnel"

    # 3. Calcul du score selon les signaux d'intention
    score = 10.0  # Base line

    matched_intent_signals = 0
    for intent_regex in COMPILED_HIGH_INTENT:
        if intent_regex.search(combined_text):
            score += 15.0
            matched_intent_signals += 1

    # Bonus pour les discussions détaillées (description de problème opérationnel)
    word_count = len(post.selftext.split())
    if word_count > 60:
        score += 10.0
    if word_count > 150:
        score += 10.0

    # Bonus pour l'engagement de la communauté (commentaires exprimant des frustrations similaires)
    if post.num_comments >= 5:
        score += 5.0
    if post.num_comments >= 15:
        score += 10.0

    # Bonus si les commentaires contiennent aussi des mots-clés d'accord
    comment_text = " ".join(post.comments).lower()
    if any(term in comment_text for term in ["same issue", "same problem", "i agree", "exact same", "would pay", "too expensive"]):
        score += 15.0

    # Plafonner à 100
    score = min(score, 100.0)

    if score < 25.0:
        return score, "Signal entrepreneurial trop faible ou discussion trop générale"

    return score, "Candidat qualifié"


def filter_and_rank_posts(posts: List[RedditPost]) -> Tuple[List[RedditPost], List[RejectedIdea]]:
    """
    Filtre les posts bruts et retourne :
    1. Les posts qualifiés triés par pertinence (jusqu'à MAX_POSTS_FOR_LLM)
    2. Une sélection d'idées/posts rejetés représentatifs pour le rapport de transparence
    """
    qualified_posts: List[RedditPost] = []
    rejected_ideas: List[RejectedIdea] = []

    logger.info(f"[INFO] Début du filtrage heuristique sur {len(posts)} publications...")

    for post in posts:
        heuristic_score, reason = calculate_relevance_score(post)
        post.heuristic_score = heuristic_score
        post.rejection_reason = reason

        if heuristic_score >= 25.0:
            qualified_posts.append(post)
        else:
            # Enregistrer pour le rapport des idées rejetées (catégorisation)
            cat = "Général"
            if "Spam" in reason or "motivation" in reason:
                cat = "Spam/Motivation"
            elif "court" in reason:
                cat = "Contenu insuffisant"
            elif "faible" in reason:
                cat = "Pas de problème actionnable"

            # Limiter la liste des rejets stockés pour la concision
            if len(rejected_ideas) < 8:
                rejected_ideas.append(
                    RejectedIdea(
                        title_or_topic=post.title[:100] if post.title else "Publication sans titre",
                        reason=reason,
                        category=cat
                    )
                )

    # Trier les posts qualifiés par score heuristique décroissant
    qualified_posts.sort(key=lambda p: p.heuristic_score, reverse=True)

    # Limiter le nombre de posts envoyés au LLM
    top_candidates = qualified_posts[:config.MAX_POSTS_FOR_LLM]

    logger.info(
        f"[INFO] Filtrage terminé : {len(qualified_posts)} posts qualifiés. "
        f"{len(top_candidates)} retenus pour transmission au LLM (seuil max={config.MAX_POSTS_FOR_LLM})"
    )

    return top_candidates, rejected_ideas
