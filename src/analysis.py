"""
LangChain Analysis Engine for RedditScraper.
Extracts actionable business opportunities using structured LLM output.
Adheres strictly to the rule: distinguish observable facts from deducted hypotheses,
and never hallucinate market size figures or revenues.
"""

import logging
from typing import List
from .config import config
from .models import (
    RedditPost,
    Opportunity,
    RejectedIdea,
    OpportunityAnalysisOutput,
    ScoringBreakdown
)

logger = logging.getLogger("RedditScraper.Analysis")

SYSTEM_PROMPT = """Tu es un analyste entrepreneurial et venture researcher chevronné.
Ton rôle N'EST PAS d'inventer des idées de startups génériques en apesanteur.
Ton rôle est d'analyser méticuleusement les VRAIS problèmes et frustrations exprimés par des entrepreneurs et chefs d'entreprise dans les publications Reddit suivantes.

RÈGLES FONDAMENTALES :
1. DISTINGUER STRICTEMENT LES FAITS DES DÉDUCTIONS :
   - FAITS : Ce qui est explicitement dit dans la publication ou les commentaires (outils actuels comme Excel, heures perdues, montant mentionné, citations exactes).
   - HYPOTHÈSES : Tes déductions analytiques (solution possible, opportunité produit, modèle de monétisation).
2. AUCUNE INVENTION OU HALLUCINATION :
   - N'invente JAMAIS un chiffre d'affaires potentiel (ex: 'marché de 50 millions'), un nombre d'utilisateurs ou une statistique de marché si elle n'est pas dans le texte.
   - Indique clairement 'À valider par étude de marché' si la taille exacte n'est pas connue.
3. CRITÈRES DE NOTATION SUR 100 POINTS :
   - Intensité du problème : /20 (douleur réelle, coûteux, bloquant)
   - Demande observable : /20 (personnes demandant activement une solution, commentaires concordants)
   - Potentiel de monétisation : /15 (crédibilité d'un paiement B2B/SaaS/service)
   - Taille / niche du marché : /15 (taille du segment adressable)
   - Concurrence / saturation : /10 (note élevée si le marché est accessible ou mal desservi)
   - Facilité de lancement : /10 (MVP réalisable par un solo/petite équipe)
   - Potentiel IA / automatisation : /10 (gain d'efficacité via logiciel/IA)
   -> Total = Somme exacte des 7 critères (entre 0 et 100).
4. VALIDATION CONCRÈTE :
   - Propose toujours des actions concrètes et mesurables (parler à 10 gérants, créer une page de pré-commande, tester un flux manuel).
"""


def _get_mock_analysis(posts: List[RedditPost]) -> OpportunityAnalysisOutput:
    """
    Génère une analyse réaliste structurée sans appel LLM externe.
    Utilisé en mode DRY_RUN, lors des tests unitaires ou si LLM_API_KEY n'est pas configurée.
    """
    logger.info("[INFO] Mode MOCK / DRY_RUN actif : génération de l'analyse synthétique validée")
    
    opportunities = [
        Opportunity(
            title="Logiciel de Réconciliation Factures & Bons de Livraison pour Artisans du Bâtiment",
            problem="Les artisans et techniciens (plombiers, électriciens) égarent les reçus fournisseurs et utilisent des classeurs ou Excel. L'appairage manuel des tickets de caisse aux numéros de chantiers prend jusqu'à 2 jours par semaine au personnel administratif.",
            target_customer="Entreprises artisanales du BTP et du dépannage de 3 à 20 ouvriers",
            opportunity="Remplacer la saisie manuelle Excel/QuickBooks par une capture ultra-simple sur mobile (ex: WhatsApp ou web-app 1 clic) qui extrait les lignes d'achats et les rattache au bon devis client.",
            proposed_solution="Micro-SaaS avec bot WhatsApp/Telegram : le technicien prend en photo le reçu de chez le fournisseur, l'OCR extrait les montants et affecte les dépenses au dossier client en générant un projet de facture.",
            why_now="Les modèles OCR/Vision légers permettent désormais une extraction précise des tickets de caisse froissés directement via messagerie sans installer une app lourde.",
            monetization="Abonnement SaaS B2B : 79€ à 149€ / mois par entreprise selon le nombre de véhicules.",
            launch_difficulty="Faible : MVP en 2 semaines combinant API WhatsApp Business, vision LLM et intégration export comptable.",
            ai_automation_potential="Élevé : extraction automatique des références articles, taux de TVA et affectation au bon chantier par similarité sémantique.",
            demand_signals=[
                "Artisan déclarant passer 15h/semaine sur Excel pour ses 8 techniciens",
                "Volonté de payer déclarée : 150$/mois par le gérant",
                "Plusieurs commentaires confirmant le rejet des apps comptables lourdes (QuickBooks Mobile)"
            ],
            risks=[
                "Réticence au changement des techniciens de terrain",
                "Gestion des cas particuliers (tickets illisibles, retours fournisseurs)"
            ],
            validation_steps=[
                "Contacter 10 gérants d'entreprises de plomberie/électricité locales",
                "Tester manuellement le flux WhatsApp sur 3 entreprises pendant 1 semaine",
                "Vérifier si le gain de temps constaté justifie un paiement de 99€/mois"
            ],
            scoring=ScoringBreakdown(
                problem_intensity=19,
                observable_demand=18,
                monetization_potential=14,
                market_size_niche=13,
                competition_saturation=8,
                launch_ease=9,
                ai_automation_potential=9,
                total_score=90,
                score_reasoning="Problème très douloureux (15h/semaine perdues), volonté explicite de payer exprimée ($150/mois), solution MVP simple à déployer."
            ),
            source_urls=["https://www.reddit.com/r/Entrepreneur/comments/mock_ent_1/"],
            source_subreddits=["r/Entrepreneur"],
            post_ids=["mock_ent_1"],
            signal_count=3
        ),
        Opportunity(
            title="Veille Automatique des Hausses de Prix Fournisseurs pour Restaurants & Boulangeries",
            problem="Les grossistes alimentaires modifient régulièrement leurs tarifs sur les bordereaux de livraison sans avertissement préalable. Les restaurateurs ne s'en aperçoivent que des semaines plus tard lors du bilan comptable.",
            target_customer="Restaurateurs indépendants, boulangeries et traiteurs (1 à 3 établissements)",
            opportunity="Détecter en temps réel les variations anormales de prix unitaires sur les ingrédients clés dès la réception des marchandises.",
            proposed_solution="Application web qui analyse les factures scannées ou reçues par email, compare chaque ligne aux prix d'achat précédents et alerte le chef par notification en cas d'augmentation > 5%.",
            why_now="Les solutions d'entreprise existantes (type Plate IQ) coûtent $400/mois/site et ciblent les grandes chaînes, laissant les indépendants sans outil accessible.",
            monetization="Abonnement mensuel de 49€ à 89€ / mois par restaurant.",
            launch_difficulty="Modérée : OCR des factures, parsing tabulaire et module de détection d'anomalies tarifaires.",
            ai_automation_potential="Très élevé : normalisation des libellés d'articles fournisseurs disparates pour un même ingrédient.",
            demand_signals=[
                "Restaurateur témoignant de milliers d'euros de pertes silencieuses par trimestre",
                "Commentateurs soulignant l'inaccessibilité tarifaire des solutions pour grands comptes"
            ],
            risks=[
                "Qualité variable des scans de factures tachées en cuisine",
                "Diversité des formats de factures grossistes"
            ],
            validation_steps=[
                "Collecter 20 factures réelles auprès de 3 restaurateurs de quartier",
                "Identifier manuellement les hausses cachées et leur présenter le montant économisé",
                "Proposer une pré-inscription payante au service d'alerte"
            ],
            scoring=ScoringBreakdown(
                problem_intensity=18,
                observable_demand=17,
                monetization_potential=13,
                market_size_niche=12,
                competition_saturation=9,
                launch_ease=8,
                ai_automation_potential=9,
                total_score=86,
                score_reasoning="ROI direct et quantifiable pour le client (économies immédiates), douleur récurrente et niche mal servie par les logiciels existants."
            ),
            source_urls=["https://www.reddit.com/r/smallbusiness/comments/mock_ent_4/"],
            source_subreddits=["r/smallbusiness"],
            post_ids=["mock_ent_4"],
            signal_count=2
        ),
        Opportunity(
            title="Portail Simplifié de Conformité Sécurité (SOC2 / ISO) pour Freelances & Prestataires",
            problem="Les éditeurs SaaS en croissance passent jusqu'à 3 jours de relances administratives par prestataire pour collecter NDA, attestations d'antécédents et conformité de poste de travail requises pour leurs audits de sécurité.",
            target_customer="CTO et responsables sécurité de startups SaaS B2B de 10 à 80 salariés",
            opportunity="Combler le vide entre les plateformes de conformité complètes (Vanta, Drata) qui gèrent mal les contractuels externes et le bricolage d'emails PDF.",
            proposed_solution="Portail autonome en marque blanche où le contractuel téléverse ses documents, signe les politiques et valide les prérequis de sécurité en 5 minutes avec relances automatiques.",
            why_now="Multiplication des audits de sécurité obligatoires exigés par les clients grands comptes des startups.",
            monetization="49$ à 199$ / mois selon le volume de sous-traitants actifs.",
            launch_difficulty="Modérée : interface web sécurisée, signature électronique et connecteurs d'export.",
            ai_automation_potential="Moyen : vérification automatique de validité des pièces justificatives fournies.",
            demand_signals=[
                "CTO déclarant perdre 3 jours d'échanges d'emails par prestataire recruté",
                "Constat que les solutions actuelles coûtent plus de 10 000$/an et ignorent les freelances"
            ],
            risks=[
                "Intégration nécessaire avec les plateformes de conformité préexistantes",
                "Plafond de dépenses des petites équipes techniques"
            ],
            validation_steps=[
                "Publier un sondage et interviewer 10 CTOs de startups SaaS B2B sur LinkedIn/Reddit",
                "Valider le prix acceptable pour déléguer cette corvée administrative",
                "Concevoir une maquette interactive pour mesurer les taux de conversion"
            ],
            scoring=ScoringBreakdown(
                problem_intensity=16,
                observable_demand=16,
                monetization_potential=14,
                market_size_niche=11,
                competition_saturation=7,
                launch_ease=7,
                ai_automation_potential=7,
                total_score=78,
                score_reasoning="Problème B2B récurrent avec budget disponible, gain de temps direct pour les équipes d'ingénierie."
            ),
            source_urls=["https://www.reddit.com/r/startups/comments/mock_ent_3/"],
            source_subreddits=["r/startups"],
            post_ids=["mock_ent_3"],
            signal_count=1
        )
    ]

    rejected = [
        RejectedIdea(
            title_or_topic="Motivational Monday: Never give up on your dreams!",
            reason="Publication purement motivationnelle sans problème concret ni besoin commercial identifiable.",
            category="Meme/Motivation"
        ),
        RejectedIdea(
            title_or_topic="Check out my revolutionary new social network for crypto dogs!",
            reason="Spam d'auto-promotion non sollicité sans expression de problème ou de demande réelle.",
            category="Spam/Promo"
        )
    ]

    return OpportunityAnalysisOutput(opportunities=opportunities, rejected_ideas=rejected)


def analyze_posts_with_langchain(posts: List[RedditPost]) -> OpportunityAnalysisOutput:
    """
    Exécute l'analyse LangChain avec sortie structurée Pydantic.
    Prend en charge tout fournisseur compatible OpenAI (OmniRoute, OpenRouter, OpenAI, Gemini).
    """
    if config.DRY_RUN or not config.LLM_API_KEY:
        logger.info("[INFO] DRY_RUN ou LLM_API_KEY absente : exécution de l'analyse avec les données de référence.")
        return _get_mock_analysis(posts)

    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.prompts import ChatPromptTemplate
    except ImportError:
        logger.error("LangChain n'est pas installé. Exécutez 'pip install langchain langchain-openai'")
        raise

    logger.info(
        f"[INFO] Initialisation du modèle LLM : '{config.LLM_MODEL}' "
        f"(Base URL: {config.LLM_BASE_URL or 'OpenAI Default'})"
    )

    # Configuration du client LLM compatible OpenAI (OmniRoute, OpenAI, OpenRouter, Gemini)
    llm_kwargs = {
        "model": config.LLM_MODEL,
        "api_key": config.LLM_API_KEY,
        "temperature": 0.2,
    }
    if config.LLM_BASE_URL:
        llm_kwargs["base_url"] = config.LLM_BASE_URL

    try:
        llm = ChatOpenAI(**llm_kwargs)
        # Utilisation de la méthode moderne with_structured_output de LangChain
        structured_llm = llm.with_structured_output(OpportunityAnalysisOutput)
    except Exception as exc:
        logger.error(
            f"[ERROR] Échec d'initialisation du LLM avec le modèle '{config.LLM_MODEL}'. "
            f"Détail : {exc}\n"
            "Vérifiez que LLM_MODEL est compatible avec votre fournisseur (OmniRoute, OpenAI, etc.)."
        )
        raise

    # Préparation du prompt d'entrée avec les publications Reddit filtrées
    formatted_posts_text = []
    for idx, post in enumerate(posts, 1):
        comments_preview = "\n  - ".join(post.comments[:3]) if post.comments else "Aucun commentaire pertinent"
        formatted_posts_text.append(
            f"--- POST {idx} [{post.subreddit}] (Upvotes: {post.score}, Comms: {post.num_comments}) ---\n"
            f"Titre: {post.title}\n"
            f"URL: {post.url}\n"
            f"Contenu: {post.selftext[:800]}\n"
            f"Commentaires clés:\n  - {comments_preview}\n"
        )

    posts_content = "\n".join(formatted_posts_text)

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", "Voici les publications Reddit à analyser pour aujourd'hui :\n\n{posts_content}\n\n"
                 "Extrais les meilleures opportunités entrepreneuriales, attribue les notes sur 100 "
                 "selon la grille stricte, et liste les types d'idées écartées.")
    ])

    logger.info(f"[INFO] Envoi de {len(posts)} publications au LLM pour extraction structurée...")

    try:
        chain = prompt_template | structured_llm
        result: OpportunityAnalysisOutput = chain.invoke({"posts_content": posts_content})

        logger.info(
            f"[INFO] Analyse terminée avec succès : {len(result.opportunities)} opportunités extraites, "
            f"{len(result.rejected_ideas)} idées rejetées répertoriées."
        )
        return result

    except Exception as exc:
        logger.error(
            f"[ERROR] Échec lors de l'appel LLM: {exc}\n"
            f"Modèle testé : LLM_MODEL='{config.LLM_MODEL}', Base URL='{config.LLM_BASE_URL}'"
        )
        raise RuntimeError(
            f"Erreur d'appel LLM avec le modèle '{config.LLM_MODEL}': {exc}"
        ) from exc
