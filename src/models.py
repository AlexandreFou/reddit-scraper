"""
Data models for Reddit Scraper and Opportunity Analyzer using Pydantic.
Ensures rigorous schema validation and structured LLM outputs.
"""

from typing import List, Optional, Dict, Any

try:
    from pydantic import BaseModel, Field
except ImportError:
    # Fallback pour exécution locale sans pip installé dans le conteneur
    class BaseModel:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        def model_dump_json(self, indent: int = 2) -> str:
            import json
            def _serialize(obj):
                if hasattr(obj, "__dict__"):
                    return {k: _serialize(v) for k, v in obj.__dict__.items()}
                elif isinstance(obj, list):
                    return [_serialize(item) for item in obj]
                elif isinstance(obj, dict):
                    return {k: _serialize(v) for k, v in obj.items()}
                return obj
            return json.dumps(_serialize(self), indent=indent, ensure_ascii=False)

    def Field(default=None, default_factory=None, **kwargs):
        if default_factory is not None:
            return default_factory()
        return default


class RedditPost(BaseModel):
    """Représentation standardisée d'une publication Reddit extraite via Apify."""
    id: str = Field(description="Identifiant unique du post Reddit")
    subreddit: str = Field(description="Nom du subreddit d'origine (ex: r/startups)")
    title: str = Field(description="Titre de la publication")
    selftext: str = Field(default="", description="Contenu texte de la publication")
    url: str = Field(description="Lien direct vers la publication Reddit")
    author: Optional[str] = Field(default=None, description="Auteur du post")
    score: int = Field(default=0, description="Nombre d'upvotes")
    num_comments: int = Field(default=0, description="Nombre de commentaires")
    created_utc: float = Field(default=0.0, description="Timestamp UTC de création")
    comments: List[str] = Field(default_factory=list, description="Extraits des meilleurs commentaires")
    
    # Métadonnées calculées lors du pré-filtrage
    heuristic_score: float = Field(default=0.0, description="Score de pertinence heuristique")
    rejection_reason: Optional[str] = Field(default=None, description="Raison du rejet si écarté")


class ScoringBreakdown(BaseModel):
    """Détail de la note sur 100 points selon la grille du cahier des charges."""
    problem_intensity: int = Field(
        ..., ge=0, le=20,
        description="Intensité du problème (/20) : le problème est-il réellement douloureux et coûteux ?"
    )
    observable_demand: int = Field(
        ..., ge=0, le=20,
        description="Demande observable (/20) : des personnes cherchent-elles ou demandent-elles activement une solution ?"
    )
    monetization_potential: int = Field(
        ..., ge=0, le=15,
        description="Potentiel de monétisation (/15) : existe-t-il une volonté de payer crédible (B2B, abonnement, service) ?"
    )
    market_size_niche: int = Field(
        ..., ge=0, le=15,
        description="Taille/niche du marché (/15) : le problème concerne-t-il un segment adressable suffisant ?"
    )
    competition_saturation: int = Field(
        ..., ge=0, le=10,
        description="Concurrence / saturation (/10) : note élevée si le marché est accessible ou mal desservi"
    )
    launch_ease: int = Field(
        ..., ge=0, le=10,
        description="Facilité de lancement (/10) : un solo-fondateur ou petite équipe peut-il lancer un MVP rapidement ?"
    )
    ai_automation_potential: int = Field(
        ..., ge=0, le=10,
        description="Potentiel d'automatisation / IA (/10) : le problème se prête-t-il à un outil logiciel ou d'automatisation ?"
    )
    total_score: int = Field(
        ..., ge=0, le=100,
        description="Total calculé sur 100 points"
    )
    score_reasoning: str = Field(
        ..., description="Explication concise et factuelle justifiant la note attribuée"
    )


class Opportunity(BaseModel):
    """Opportunité entrepreneuriale détectée et structurée par l'IA."""
    title: str = Field(
        description="Nom court et évocateur de l'opportunité (ex: 'SaaS d'onboarding sous-traitants BTP')"
    )
    problem: str = Field(
        description="Description factuelle du problème exprimé par les utilisateurs"
    )
    target_customer: str = Field(
        description="Client cible spécifique (ex: 'Agences web de 3 à 15 salariés', 'Plombiers indépendants')"
    )
    opportunity: str = Field(
        description="Opportunité entrepreneuriale identifiée (angle business précis)"
    )
    proposed_solution: str = Field(
        description="Solution logicielle, service ou MVP recommandé"
    )
    why_now: str = Field(
        description="Pourquoi maintenant ? (évolution des outils, nouvelle réglementation, saturation d'un acteur existant)"
    )
    monetization: str = Field(
        description="Modèle de monétisation recommandé (SaaS mensuel, commission, paiement à l'usage, prestation packagée)"
    )
    launch_difficulty: str = Field(
        description="Niveau d'effort pour un premier MVP (ex: 'Faible : No-Code/Make en 1 semaine', 'Modéré : SaaS complet en 1 mois')"
    )
    ai_automation_potential: str = Field(
        description="Comment l'IA ou l'automatisation apporte un avantage décisif"
    )
    demand_signals: List[str] = Field(
        description="Signaux factuels de demande observés dans les publications ou commentaires"
    )
    risks: List[str] = Field(
        description="Risques majeurs et obstacles potentiels"
    )
    validation_steps: List[str] = Field(
        description="3 à 5 actions concrètes pour valider l'idée avant d'écrire la moindre ligne de code"
    )
    scoring: ScoringBreakdown = Field(
        description="Grille d'évaluation détaillée sur 100 points"
    )
    source_urls: List[str] = Field(
        default_factory=list, description="URLs des posts Reddit sources à l'origine du signal"
    )
    source_subreddits: List[str] = Field(
        default_factory=list, description="Subreddits d'où provient le signal"
    )
    post_ids: List[str] = Field(
        default_factory=list, description="IDs des posts Reddit analysés pour cette idée"
    )
    signal_count: int = Field(
        default=1, description="Nombre de publications ou signaux concordants regroupés"
    )


class RejectedIdea(BaseModel):
    """Exemple de publication ou type d'idée écartée pour assurer la transparence."""
    title_or_topic: str = Field(description="Titre ou sujet écarté")
    reason: str = Field(description="Pourquoi cette publication a été écartée (manque de douleur réelle, spam, trop générique, etc.)")
    category: str = Field(default="Filtrage", description="Catégorie de rejet (ex: 'Spam/Promo', 'Meme/Motivation', 'Pas de problème actionnable')")


class OpportunityAnalysisOutput(BaseModel):
    """Schéma de sortie attendu pour LangChain / Structured Output."""
    opportunities: List[Opportunity] = Field(
        default_factory=list,
        description="Liste des opportunités entrepreneuriales extraites et scorées"
    )
    rejected_ideas: Optional[List[RejectedIdea]] = Field(
        default_factory=list,
        description="Sélection représentative de publications ou idées écartées (optionnel)"
    )


class DailyReportData(BaseModel):
    """Données complètes du rapport quotidien enregistrées dans data/YYYY-MM-DD.json."""
    date: str = Field(description="Date du rapport (YYYY-MM-DD)")
    generated_at: str = Field(description="Horodatage ISO de génération")
    posts_scraped_total: int = Field(description="Nombre total de posts récupérés via Apify")
    posts_after_filtering: int = Field(description="Nombre de posts conservés après filtrage heuristique")
    posts_sent_to_llm: int = Field(description="Nombre de posts effectivement soumis au LLM")
    subreddit_breakdown: Dict[str, int] = Field(default_factory=dict, description="Répartition des posts par subreddit")
    opportunities: List[Opportunity] = Field(default_factory=list, description="Top opportunités retenues")
    rejected_ideas: List[RejectedIdea] = Field(default_factory=list, description="Exemples d'idées écartées")
