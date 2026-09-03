"""
Scoring validation and deduplication engine for opportunities.
Enforces the 100-point evaluation matrix, clusters duplicate ideas,
and ranks the top entrepreneurial opportunities.
"""

import re
import logging
from typing import List, Set
from .config import config
from .models import Opportunity

logger = logging.getLogger("RedditScraper.Scoring")

# Mots de liaison à exclure pour éviter de fausses déduplications sur les prépositions
STOPWORDS: Set[str] = {
    "de", "des", "du", "le", "la", "les", "un", "une", "pour", "et", "en",
    "dans", "par", "sur", "au", "aux", "avec", "sans", "the", "a", "an",
    "for", "and", "in", "on", "of", "to", "with", "is", "are", "tool", "app"
}


def _extract_keywords(text: str) -> Set[str]:
    """Extrait les mots significatifs en éliminant les mots vides."""
    tokens = re.findall(r"\b[a-zA-ZÀ-ÿ0-9_-]{3,}\b", text.lower())
    return {w for w in tokens if w not in STOPWORDS}


def validate_and_recalc_score(opp: Opportunity) -> Opportunity:
    """
    S'assure que le total correspond exactement à la somme des 7 sous-critères
    et reste borné entre 0 et 100.
    """
    b = opp.scoring
    # Clamping de chaque critère aux bornes autorisées
    b.problem_intensity = max(0, min(20, b.problem_intensity))
    b.observable_demand = max(0, min(20, b.observable_demand))
    b.monetization_potential = max(0, min(15, b.monetization_potential))
    b.market_size_niche = max(0, min(15, b.market_size_niche))
    b.competition_saturation = max(0, min(10, b.competition_saturation))
    b.launch_ease = max(0, min(10, b.launch_ease))
    b.ai_automation_potential = max(0, min(10, b.ai_automation_potential))

    calculated_total = (
        b.problem_intensity
        + b.observable_demand
        + b.monetization_potential
        + b.market_size_niche
        + b.competition_saturation
        + b.launch_ease
        + b.ai_automation_potential
    )
    b.total_score = calculated_total
    return opp


def deduplicate_opportunities(opportunities: List[Opportunity]) -> List[Opportunity]:
    """
    Regroupe les opportunités traitant du même problème sous-jacent.
    Si deux opportunités partagent des mots-clés de titre ou de problème similaires,
    fusionne leurs signaux de demande et sources, puis incrémente signal_count.
    """
    if not opportunities:
        return []

    unique_opps: List[Opportunity] = []

    for opp in opportunities:
        opp = validate_and_recalc_score(opp)
        is_duplicate = False

        # Vérification avec les opportunités déjà retenues
        words_a = _extract_keywords(opp.title)
        for existing in unique_opps:
            words_b = _extract_keywords(existing.title)
            intersection = words_a.intersection(words_b)

            # Correspondance significative sur au moins 3 mots-clés distincts ou 2 mots avec cible identique
            if len(intersection) >= 3 or (
                opp.target_customer.strip().lower() == existing.target_customer.strip().lower()
                and len(intersection) >= 2
            ):
                is_duplicate = True
                # Fusion des signaux
                existing.signal_count += opp.signal_count
                for url in opp.source_urls:
                    if url not in existing.source_urls:
                        existing.source_urls.append(url)
                for sub in opp.source_subreddits:
                    if sub not in existing.source_subreddits:
                        existing.source_subreddits.append(sub)
                for p_id in opp.post_ids:
                    if p_id not in existing.post_ids:
                        existing.post_ids.append(p_id)
                for signal in opp.demand_signals:
                    if signal not in existing.demand_signals:
                        existing.demand_signals.append(signal)

                # Bonus léger sur la demande observable car observée dans plusieurs publications
                existing.scoring.observable_demand = min(20, existing.scoring.observable_demand + 1)
                validate_and_recalc_score(existing)
                logger.info(
                    f"[INFO] Regroupement de doublon pour : '{existing.title}' "
                    f"(Signal total: {existing.signal_count} publications)"
                )
                break

        if not is_duplicate:
            unique_opps.append(opp)

    return unique_opps


def rank_opportunities(opportunities: List[Opportunity]) -> List[Opportunity]:
    """
    Déduplique et classe les opportunités par score global décroissant.
    Retourne le Top N configuré (par exemple Top 10).
    """
    logger.info(f"[INFO] Déduplication et classement de {len(opportunities)} opportunités brutes...")
    deduped = deduplicate_opportunities(opportunities)

    # Tri décroissant par note totale
    deduped.sort(key=lambda o: o.scoring.total_score, reverse=True)

    ranked_top = deduped[:config.TOP_OPPORTUNITIES]

    logger.info(
        f"[INFO] Classement terminé : {len(ranked_top)} opportunités retenues dans le Top "
        f"(meilleur score: {ranked_top[0].scoring.total_score}/100)" if ranked_top else "[INFO] Aucune opportunité."
    )
    return ranked_top
