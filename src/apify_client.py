"""
Apify Client module for RedditScraper.
Optimized for 1 SINGLE Apify run per day across all 3 subreddits:
r/Entrepreneur, r/startups, r/smallbusiness.
Minimizes compute units to stay safely within Apify's free tier.
"""

import logging
from typing import List, Dict, Any
from .config import config
from .models import RedditPost

logger = logging.getLogger("RedditScraper.Apify")


def get_mock_posts() -> List[RedditPost]:
    """
    Fournit un jeu de données réaliste de test (mock) sans consommer de crédit Apify.
    Très utile lors des tests en local, du développement ou en mode DRY_RUN.
    """
    return [
        RedditPost(
            id="mock_ent_1",
            subreddit="r/Entrepreneur",
            title="I spend 15 hours a week chasing client invoices and receipts. Is there an automated tool for trade businesses?",
            selftext="I run a plumbing & heating company with 8 technicians. We currently use Excel and paper work orders. At the end of every week, our office manager spends nearly 2 full days matching receipts from suppliers to jobs and sending invoices. QuickBooks is too cumbersome for our field guys. We would gladly pay $150/month for something that automatically matches photos of receipts to job numbers and generates draft invoices.",
            url="https://www.reddit.com/r/Entrepreneur/comments/mock_ent_1/",
            author="plumber_boss_99",
            score=68,
            num_comments=34,
            created_utc=1756886400.0,
            comments=[
                "We have the exact same issue in our landscaping business. Tried Jobber, still too manual for receipts.",
                "I hate using QuickBooks Mobile, technicians refuse to use it.",
                "Would easily pay $100-200/mo for a WhatsApp-based receipt submission that auto-tags jobs."
            ]
        ),
        RedditPost(
            id="mock_ent_2",
            subreddit="r/smallbusiness",
            title="Frustrated with existing scheduling tools for multi-location dental/physio clinics",
            selftext="We operate 3 physiotherapy practices. Calendly and Acuity cannot handle practitioner rooms + specific medical equipment constraints (e.g., ultrasound machine can only be in Room 2). We are forced to use an ancient desktop software from 2008 with zero online booking. Patients keep calling because they can't book specific therapies online.",
            url="https://www.reddit.com/r/smallbusiness/comments/mock_ent_2/",
            author="physio_owner",
            score=45,
            num_comments=21,
            created_utc=1756890000.0,
            comments=[
                "Same here for our dental clinic with hygiene vs surgery rooms.",
                "Current software vendors charge $5,000 upfront + $300/mo maintenance for clunky UI."
            ]
        ),
        RedditPost(
            id="mock_ent_3",
            subreddit="r/startups",
            title="Why is subcontractor onboarding for SOC2 / ISO compliance still a manual PDF nightmare?",
            selftext="We are a B2B SaaS scaling up. Every time we hire a contractor or freelance developer, our security team sends 6 PDFs (NDA, security policies, background check consent, device compliance checklist). Collecting, verifying, and logging these in our compliance tool takes 3 days of back-and-forth per contractor. Is there an off-the-shelf portal that handles vendor & contractor security onboarding?",
            url="https://www.reddit.com/r/startups/comments/mock_ent_3/",
            author="saas_cto_alex",
            score=82,
            num_comments=41,
            created_utc=1756893600.0,
            comments=[
                "Vanta and Drata only track employees well, contractors are always forgotten.",
                "We built an internal Retool for this because nothing existed under $10k/yr."
            ]
        ),
        RedditPost(
            id="mock_ent_4",
            subreddit="r/smallbusiness",
            title="We waste thousands every month because supplier price hikes go unnoticed until invoice audit",
            selftext="Restaurant and bakery owner here. Food ingredient suppliers change prices weekly on invoices without warning. We don't realize olive oil or flour jumped 25% until our quarterly accountant review. Need an OCR tool that scans delivery notes and flags price increases against previous purchase orders.",
            url="https://www.reddit.com/r/smallbusiness/comments/mock_ent_4/",
            author="baker_mike",
            score=95,
            num_comments=58,
            created_utc=1756897200.0,
            comments=[
                "Plate IQ does this for big chains but charges $400/month per location, unaffordable for indie bistros.",
                "An AI tool reading invoice photos from email/scan would save me at least $800/month."
            ]
        ),
        RedditPost(
            id="mock_ent_5",
            subreddit="r/Entrepreneur",
            title="Motivational Monday: Never give up on your dreams! 🚀 Drop your goals below",
            selftext="Just remember that Elon Musk and Steve Jobs failed before they succeeded. Believe in yourself and grind 18 hours a day. Who is grinding today?",
            url="https://www.reddit.com/r/Entrepreneur/comments/mock_ent_5/",
            author="grindset_guru",
            score=12,
            num_comments=5,
            created_utc=1756900800.0,
            comments=["Thanks for the motivation!"]
        ),
        RedditPost(
            id="mock_ent_6",
            subreddit="r/startups",
            title="Check out my revolutionary new social network for crypto dogs! (Link in bio)",
            selftext="We just launched! Download our app and invite 10 friends to win free tokens. Best startup ever!",
            url="https://www.reddit.com/r/startups/comments/mock_ent_6/",
            author="spammer_xyz",
            score=0,
            num_comments=1,
            created_utc=1756904400.0,
            comments=[]
        )
    ]


def run_apify_reddit_scraper() -> List[RedditPost]:
    """
    Lance un UNIQUE run Apify pour scraper simultanément les 3 subreddits :
    r/Entrepreneur, r/startups, r/smallbusiness.
    
    Retourne la liste des objets RedditPost extraits.
    """
    if config.DRY_RUN or not config.APIFY_API_TOKEN:
        logger.info("[INFO] Mode DRY_RUN activé ou APIFY_API_TOKEN absent : utilisation du mock réaliste")
        return get_mock_posts()

    try:
        from apify_client import ApifyClient
    except ImportError:
        logger.error("Le package apify-client n'est pas installé. Lancez 'pip install apify-client'")
        raise

    logger.info(f"[INFO] Initialisation du client Apify avec l'acteur '{config.APIFY_ACTOR_ID}'")
    client = ApifyClient(config.APIFY_API_TOKEN)

    # Construction de l'input pour un run UNIQUE regroupant les 3 subreddits
    # Utilisation des URLs /new/ pour capter les dernières 24h
    start_urls = [
        {"url": f"https://www.reddit.com/r/{sub}/new/"}
        for sub in config.SUBREDDITS
    ]

    total_max_items = config.POSTS_PER_SUBREDDIT * len(config.SUBREDDITS)

    run_input = {
        "startUrls": start_urls,
        "maxItems": total_max_items,
        "maxCommentsPerPost": 5,      # Limité à 5 commentaires par post pour préserver la mémoire et le coût
        "scrollTimeout": 30,          # Évite les sessions traînantes
        "proxy": {"useApifyProxy": True}
    }

    logger.info(
        f"[INFO] Lancement du run Apify pour les subreddits {config.SUBREDDITS} "
        f"(max {total_max_items} posts au total)"
    )

    try:
        run = client.actor(config.APIFY_ACTOR_ID).call(run_input=run_input)
        dataset_id = run.get("defaultDatasetId")
        logger.info(f"[INFO] Run Apify terminé avec succès. Dataset ID: {dataset_id}")

        items = list(client.dataset(dataset_id).iterate_items())
        logger.info(f"[INFO] {len(items)} éléments bruts récupérés depuis le dataset Apify")

        posts: List[RedditPost] = []
        for item in items:
            post = _parse_apify_item(item)
            if post:
                posts.append(post)

        return posts

    except Exception as exc:
        logger.error(f"[ERROR] Échec lors de l'exécution d'Apify: {exc}")
        # En cas d'erreur réseau ou de quota, lever une exception claire
        raise RuntimeError(f"Erreur Apify: {exc}") from exc


def _parse_apify_item(item: Dict[str, Any]) -> RedditPost:
    """Parse un enregistrement brut d'Apify vers notre modèle RedditPost standardisé."""
    raw_sub = item.get("subreddit", "") or item.get("communityName", "")
    if not raw_sub.startswith("r/"):
        raw_sub = f"r/{raw_sub}"

    # Extraction des commentaires si présents
    comments_raw = item.get("comments", []) or []
    extracted_comments: List[str] = []
    for c in comments_raw[:5]:
        if isinstance(c, dict):
            text = c.get("body", "") or c.get("text", "")
        elif isinstance(c, str):
            text = c
        else:
            text = ""
        if text.strip():
            extracted_comments.append(text.strip()[:300])

    return RedditPost(
        id=str(item.get("id") or item.get("postId") or hash(item.get("url", ""))),
        subreddit=raw_sub,
        title=item.get("title", "").strip(),
        selftext=item.get("selftext", "") or item.get("body", "") or item.get("description", ""),
        url=item.get("url", "") or item.get("postUrl", ""),
        author=item.get("author", None),
        score=int(item.get("score", 0) or item.get("upVotes", 0) or 0),
        num_comments=int(item.get("numberOfComments", 0) or item.get("commentsCount", 0) or len(extracted_comments)),
        created_utc=float(item.get("createdUtc", 0) or item.get("createdAt", 0) or 0.0),
        comments=extracted_comments
    )
