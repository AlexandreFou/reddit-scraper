export interface ScoringBreakdown {
  problem_intensity: number;
  observable_demand: number;
  monetization_potential: number;
  market_size_niche: number;
  competition_saturation: number;
  launch_ease: number;
  ai_automation_potential: number;
  total_score: number;
  score_reasoning: string;
}

export interface OpportunityItem {
  id: string;
  title: string;
  problem: string;
  target_customer: string;
  opportunity: string;
  proposed_solution: string;
  why_now: string;
  monetization: string;
  launch_difficulty: string;
  ai_automation_potential: string;
  demand_signals: string[];
  risks: string[];
  validation_steps: string[];
  scoring: ScoringBreakdown;
  source_urls: string[];
  source_subreddits: string[];
  signal_count: number;
}

export interface RejectedItem {
  title_or_topic: string;
  reason: string;
  category: string;
}

export const SAMPLE_REPORT_DATA = {
  date: "2026-09-03",
  scraped_total: 86,
  filtered_total: 32,
  llm_analyzed: 25,
  subreddits: {
    "r/Entrepreneur": 34,
    "r/startups": 28,
    "r/smallbusiness": 24,
  },
  opportunities: [
    {
      id: "opp-1",
      title: "Logiciel de Réconciliation Factures & Bons de Livraison pour Artisans du Bâtiment",
      problem: "Les artisans et techniciens (plombiers, électriciens) égarent les reçus fournisseurs et utilisent des classeurs ou Excel. L'appairage manuel des tickets de caisse aux numéros de chantiers prend jusqu'à 2 jours par semaine au personnel administratif.",
      target_customer: "Entreprises artisanales du BTP et du dépannage de 3 à 20 ouvriers",
      opportunity: "Remplacer la saisie manuelle Excel/QuickBooks par une capture mobile 1-clic (ex: WhatsApp) qui extrait les lignes d'achats et les rattache au bon devis client.",
      proposed_solution: "Micro-SaaS avec bot WhatsApp/Telegram : le technicien prend en photo le reçu chez le fournisseur, l'OCR extrait montants et TVA, puis affecte les dépenses au dossier client en générant un projet de facture.",
      why_now: "Les modèles OCR/Vision légers permettent une extraction instantanée et précise des tickets froissés directement via messagerie sans installer une app lourde.",
      monetization: "Abonnement SaaS B2B : 79€ à 149€ / mois par entreprise selon le nombre de véhicules.",
      launch_difficulty: "Faible : MVP en 2 semaines combinant API WhatsApp Business, vision LLM et export comptable.",
      ai_automation_potential: "Élevé : extraction automatique des références articles, taux de TVA et affectation au bon chantier par similarité sémantique.",
      demand_signals: [
        "Artisan déclarant passer 15h/semaine sur Excel pour ses 8 techniciens",
        "Volonté explicite de payer déclarée : 150$/mois par le gérant",
        "Plusieurs commentaires confirmant le rejet des apps comptables lourdes (QuickBooks Mobile)"
      ],
      risks: [
        "Réticence au changement des techniciens de terrain",
        "Gestion des cas particuliers (tickets illisibles, retours fournisseurs)"
      ],
      validation_steps: [
        "Contacter 10 gérants d'entreprises de plomberie/électricité locales",
        "Tester manuellement le flux WhatsApp sur 3 entreprises pendant 1 semaine",
        "Vérifier si le gain de temps constaté justifie un paiement de 99€/mois"
      ],
      scoring: {
        problem_intensity: 19,
        observable_demand: 18,
        monetization_potential: 14,
        market_size_niche: 13,
        competition_saturation: 8,
        launch_ease: 9,
        ai_automation_potential: 9,
        total_score: 90,
        score_reasoning: "Problème très douloureux (15h/semaine perdues), volonté explicite de payer exprimée ($150/mois), solution MVP simple à déployer."
      },
      source_urls: ["https://www.reddit.com/r/Entrepreneur/comments/mock_ent_1/"],
      source_subreddits: ["r/Entrepreneur"],
      signal_count: 3
    },
    {
      id: "opp-2",
      title: "Veille Automatique des Hausses de Prix Fournisseurs pour Restaurants & Boulangeries",
      problem: "Les grossistes alimentaires modifient régulièrement leurs tarifs sur les bordereaux de livraison sans avertissement préalable. Les restaurateurs ne s'en aperçoivent que des semaines plus tard lors du bilan comptable.",
      target_customer: "Restaurateurs indépendants, boulangeries et traiteurs (1 à 3 établissements)",
      opportunity: "Détecter en temps réel les variations anormales de prix unitaires sur les ingrédients clés dès la réception des marchandises.",
      proposed_solution: "Application web qui analyse les factures scannées ou reçues par email, compare chaque ligne aux prix d'achat précédents et alerte le chef par notification en cas d'augmentation > 5%.",
      why_now: "Les solutions d'entreprise existantes (type Plate IQ) coûtent $400/mois/site et ciblent les grandes chaînes, laissant les indépendants sans outil accessible.",
      monetization: "Abonnement mensuel de 49€ à 89€ / mois par restaurant.",
      launch_difficulty: "Modérée : OCR des factures, parsing tabulaire et module de détection d'anomalies tarifaires.",
      ai_automation_potential: "Très élevé : normalisation des libellés d'articles fournisseurs disparates pour un même ingrédient.",
      demand_signals: [
        "Restaurateur témoignant de milliers d'euros de pertes silencieuses par trimestre",
        "Commentateurs soulignant l'inaccessibilité tarifaire des solutions pour grands comptes"
      ],
      risks: [
        "Qualité variable des scans de factures tachées en cuisine",
        "Diversité des formats de factures grossistes"
      ],
      validation_steps: [
        "Collecter 20 factures réelles auprès de 3 restaurateurs de quartier",
        "Identifier manuellement les hausses cachées et leur présenter le montant économisé",
        "Proposer une pré-inscription payante au service d'alerte"
      ],
      scoring: {
        problem_intensity: 18,
        observable_demand: 17,
        monetization_potential: 13,
        market_size_niche: 12,
        competition_saturation: 9,
        launch_ease: 8,
        ai_automation_potential: 9,
        total_score: 86,
        score_reasoning: "ROI direct et quantifiable pour le client (économies immédiates), douleur récurrente et niche mal servie par les logiciels existants."
      },
      source_urls: ["https://www.reddit.com/r/smallbusiness/comments/mock_ent_4/"],
      source_subreddits: ["r/smallbusiness"],
      signal_count: 2
    },
    {
      id: "opp-3",
      title: "Portail Simplifié de Conformité Sécurité (SOC2 / ISO) pour Freelances & Prestataires",
      problem: "Les éditeurs SaaS en croissance passent jusqu'à 3 jours de relances administratives par prestataire pour collecter NDA, attestations d'antécédents et conformité de poste de travail requises pour leurs audits de sécurité.",
      target_customer: "CTO et responsables sécurité de startups SaaS B2B de 10 à 80 salariés",
      opportunity: "Combler le vide entre les plateformes de conformité complètes (Vanta, Drata) qui gèrent mal les contractuels externes et le bricolage d'emails PDF.",
      proposed_solution: "Portail autonome en marque blanche où le contractuel téléverse ses documents, signe les politiques et valide les prérequis de sécurité en 5 minutes avec relances automatiques.",
      why_now: "Multiplication des audits de sécurité obligatoires exigés par les clients grands comptes des startups.",
      monetization: "49$ à 199$ / mois selon le volume de sous-traitants actifs.",
      launch_difficulty: "Modérée : interface web sécurisée, signature électronique et connecteurs d'export.",
      ai_automation_potential: "Moyen : vérification automatique de validité des pièces justificatives fournies.",
      demand_signals: [
        "CTO déclarant perdre 3 jours d'échanges d'emails par prestataire recruté",
        "Constat que les solutions actuelles coûtent plus de 10 000$/an et ignorent les freelances"
      ],
      risks: [
        "Intégration nécessaire avec les plateformes de conformité préexistantes",
        "Plafond de dépenses des petites équipes techniques"
      ],
      validation_steps: [
        "Publier un sondage et interviewer 10 CTOs de startups SaaS B2B sur LinkedIn/Reddit",
        "Valider le prix acceptable pour déléguer cette corvée administrative",
        "Concevoir une maquette interactive pour mesurer les taux de conversion"
      ],
      scoring: {
        problem_intensity: 16,
        observable_demand: 16,
        monetization_potential: 14,
        market_size_niche: 11,
        competition_saturation: 7,
        launch_ease: 7,
        ai_automation_potential: 7,
        total_score: 78,
        score_reasoning: "Problème B2B récurrent avec budget disponible, gain de temps direct pour les équipes d'ingénierie."
      },
      source_urls: ["https://www.reddit.com/r/startups/comments/mock_ent_3/"],
      source_subreddits: ["r/startups"],
      signal_count: 1
    }
  ] as OpportunityItem[],
  rejected_ideas: [
    {
      title_or_topic: "Motivational Monday: Never give up on your dreams!",
      reason: "Publication purement motivationnelle sans problème concret ni besoin commercial identifiable.",
      category: "Meme/Motivation"
    },
    {
      title_or_topic: "Check out my revolutionary new social network for crypto dogs!",
      reason: "Spam d'auto-promotion non sollicité sans expression de problème ou de demande réelle.",
      category: "Spam/Promo"
    }
  ] as RejectedItem[]
};

export const PROJECT_FILES = [
  { path: ".github/workflows/daily.yml", description: "Workflow GitHub Actions quotidien (cron 06:00 UTC) et dispatch manuel" },
  { path: "src/config.py", description: "Configuration centralisée, gestion .env et validation des variables" },
  { path: "src/models.py", description: "Modèles Pydantic pour posts Reddit, scoring /100, opportunités et rapports" },
  { path: "src/apify_client.py", description: "Scraping en 1 seul run Apify pour les 3 subreddits avec mode mock" },
  { path: "src/filtering.py", description: "Pré-filtrage heuristique en Python (élimination memes/spam, détection signaux forts)" },
  { path: "src/analysis.py", description: "Chaîne LangChain avec structured output (compatible OmniRoute / OpenAI / Gemini)" },
  { path: "src/scoring.py", description: "Calcul de la grille sur 100 points et déduplication des signaux concordants" },
  { path: "src/report.py", description: "Génération des rapports Markdown et archivage des données JSON" },
  { path: "src/main.py", description: "Orchestrateur CLI complet exécutant le pipeline de bout en bout" },
  { path: "tests/test_filtering.py", description: "Tests unitaires du filtrage anti-bruit" },
  { path: "tests/test_scoring.py", description: "Tests unitaires du calcul de score et de la déduplication" },
  { path: "tests/test_models.py", description: "Tests de validation des schémas Pydantic" },
  { path: "requirements.txt", description: "Dépendances Python nécessaires pour GitHub Actions et le dev local" },
  { path: ".env.example", description: "Template des variables d'environnement documenté" },
  { path: ".gitignore", description: "Protection contre le commit de tokens ou de secrets" },
  { path: "README.md", description: "Guide complet d'installation, configuration et déploiement" },
  { path: "reports/2026-09-03.md", description: "Rapport quotidien Markdown généré" },
  { path: "data/2026-09-03.json", description: "Données brutes structurées archivées au format JSON" }
];
