"""
Markdown Report and JSON Data Generator.
Produces human-readable, beautifully structured Markdown reports formatted for GitHub,
and archives structured JSON records for historical analytics.
"""

import os
import json
import logging
from datetime import datetime
from typing import List, Dict

try:
    import pytz
except ImportError:
    pytz = None

from .config import config
from .models import Opportunity, RejectedIdea, DailyReportData

logger = logging.getLogger("RedditScraper.Report")


def get_current_date_str() -> str:
    """Retourne la date du jour selon le fuseau horaire configuré (ex: Europe/Paris)."""
    try:
        tz = pytz.timezone(config.TIMEZONE)
        return datetime.now(tz).strftime("%Y-%m-%d")
    except Exception:
        return datetime.utcnow().strftime("%Y-%m-%d")


def generate_markdown_report(
    date_str: str,
    opportunities: List[Opportunity],
    rejected_ideas: List[RejectedIdea],
    posts_scraped_total: int,
    posts_after_filtering: int,
    posts_sent_to_llm: int,
    subreddit_breakdown: Dict[str, int]
) -> str:
    """Génère le texte Markdown complet du rapport quotidien."""
    lines: List[str] = []

    # En-tête principal
    lines.append(f"# Reddit Entrepreneurial Opportunities — {date_str}")
    lines.append("")
    lines.append("## Résumé de la veille quotidienne")
    lines.append("")
    lines.append(f"- **Publications brutes analysées (dernières 24h)** : {posts_scraped_total}")
    lines.append(f"- **Publications qualifiées après filtrage anti-bruit** : {posts_after_filtering}")
    lines.append(f"- **Publications traitées par le LLM** : {posts_sent_to_llm}")
    lines.append(f"- **Opportunités entrepreneuriales validées** : {len(opportunities)}")
    lines.append("")
    lines.append("### Répartition par subreddit")
    for sub, count in subreddit_breakdown.items():
        lines.append(f"- **{sub}** : {count} publications")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Tableau récapitulatif
    lines.append("## Tableau de synthèse des opportunités")
    lines.append("")
    lines.append("| Rang | Opportunité | Score | Subreddit principal | Signal de demande |")
    lines.append("|:---:|:---|:---:|:---|:---|")

    medals = ["🥇 1", "🥈 2", "🥉 3"]
    for idx, opp in enumerate(opportunities):
        rank_label = medals[idx] if idx < len(medals) else f"**{idx + 1}**"
        sub_label = opp.source_subreddits[0] if opp.source_subreddits else "Reddit"
        signal_text = f"{opp.signal_count} post(s) / discussion active"
        if opp.demand_signals:
            signal_text = opp.demand_signals[0][:45] + "..." if len(opp.demand_signals[0]) > 45 else opp.demand_signals[0]
        lines.append(f"| {rank_label} | [{opp.title}](#opportunite-{idx + 1}) | **{opp.scoring.total_score}/100** | `{sub_label}` | {signal_text} |")

    lines.append("")
    lines.append("---")
    lines.append("")

    # Fiches détaillées pour chaque opportunité
    medal_emojis = ["🥇", "🥈", "🥉"]
    for idx, opp in enumerate(opportunities):
        rank_num = idx + 1
        prefix = f"{medal_emojis[idx]} Opportunité {rank_num}" if idx < len(medal_emojis) else f"Opportunité {rank_num}"
        anchor = f"opportunite-{rank_num}"

        lines.append(f"<a id=\"{anchor}\"></a>")
        lines.append(f"# {prefix} — {opp.title}")
        lines.append("")
        lines.append(f"**Score global : {opp.scoring.total_score}/100**  ")
        lines.append(f"*Justification du score : {opp.scoring.score_reasoning}*")
        lines.append("")

        # Tableau des notes détaillées
        b = opp.scoring
        lines.append("<details>")
        lines.append("<summary>📊 <b>Détail de la grille de notation (/100)</b></summary>")
        lines.append("")
        lines.append("| Critère | Note | Maximum | Appréciation |")
        lines.append("|:---|:---:|:---:|:---|")
        lines.append(f"| Intensité du problème | {b.problem_intensity} | 20 | Douleur réelle et coût de l'inaction |")
        lines.append(f"| Demande observable | {b.observable_demand} | 20 | Recherches actives et fréquence des requêtes |")
        lines.append(f"| Potentiel de monétisation | {b.monetization_potential} | 15 | Volonté et capacité de payer du client |")
        lines.append(f"| Taille / niche du marché | {b.market_size_niche} | 15 | Segment cible suffisant et accessible |")
        lines.append(f"| Concurrence / saturation | {b.competition_saturation} | 10 | Opportunité d'angle différencié |")
        lines.append(f"| Facilité de lancement | {b.launch_ease} | 10 | Rapidité de mise en place d'un MVP |")
        lines.append(f"| Potentiel IA / automatisation | {b.ai_automation_potential} | 10 | Avantage logiciel décisif |")
        lines.append(f"| **TOTAL** | **{b.total_score}** | **100** | **Score final pondéré** |")
        lines.append("")
        lines.append("</details>")
        lines.append("")

        lines.append("### 🎯 Problème")
        lines.append(opp.problem)
        lines.append("")

        lines.append("### 👥 Client cible")
        lines.append(opp.target_customer)
        lines.append("")

        lines.append("### 💡 Opportunité")
        lines.append(opp.opportunity)
        lines.append("")

        lines.append("### 🛠️ Solution possible")
        lines.append(opp.proposed_solution)
        lines.append("")

        lines.append("### ⏳ Pourquoi maintenant ?")
        lines.append(opp.why_now)
        lines.append("")

        lines.append("### 💰 Monétisation")
        lines.append(opp.monetization)
        lines.append("")

        lines.append("### 🚀 Difficulté de lancement")
        lines.append(opp.launch_difficulty)
        lines.append("")

        lines.append("### 🤖 Potentiel IA / automatisation")
        lines.append(opp.ai_automation_potential)
        lines.append("")

        lines.append("### 📈 Signaux de demande observés")
        for sig in opp.demand_signals:
            lines.append(f"- {sig}")
        lines.append("")

        lines.append("### ⚠️ Risques et obstacles")
        for rk in opp.risks:
            lines.append(f"- {rk}")
        lines.append("")

        lines.append("### ✅ Comment valider cette idée ? (Actions concrètes)")
        for step_idx, step in enumerate(opp.validation_steps, 1):
            lines.append(f"{step_idx}. {step}")
        lines.append("")

        lines.append("### 🔗 Sources Reddit")
        for u in opp.source_urls:
            lines.append(f"- [{u}]({u})")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Section : Idées rejetées (transparence)
    lines.append("# Idées et publications rejetées")
    lines.append("")
    lines.append("Afin d'éviter le bruit et les biais de confirmation, les publications ne répondant pas aux critères stricts de viabilité commerciale ont été filtrées :")
    lines.append("")
    if rejected_ideas:
        lines.append("| Type / Sujet rejeté | Catégorie | Motif du rejet |")
        lines.append("|:---|:---:|:---|")
        for rej in rejected_ideas:
            lines.append(f"| {rej.title_or_topic} | `{rej.category}` | {rej.reason} |")
    else:
        lines.append("Aucun post rejeté enregistré.")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"*Rapport généré automatiquement par RedditScraper le {date_str} via Apify & LangChain.*")

    return "\n".join(lines)


def save_daily_report(
    date_str: str,
    opportunities: List[Opportunity],
    rejected_ideas: List[RejectedIdea],
    posts_scraped_total: int,
    posts_after_filtering: int,
    posts_sent_to_llm: int,
    subreddit_breakdown: Dict[str, int],
    reports_dir: str = "reports",
    data_dir: str = "data"
) -> Dict[str, str]:
    """
    Sauvegarde le rapport Markdown dans reports/YYYY-MM-DD.md
    et les données structurées dans data/YYYY-MM-DD.json.
    """
    os.makedirs(reports_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)

    # 1. Sauvegarde Markdown
    md_content = generate_markdown_report(
        date_str=date_str,
        opportunities=opportunities,
        rejected_ideas=rejected_ideas,
        posts_scraped_total=posts_scraped_total,
        posts_after_filtering=posts_after_filtering,
        posts_sent_to_llm=posts_sent_to_llm,
        subreddit_breakdown=subreddit_breakdown
    )
    md_filename = os.path.join(reports_dir, f"{date_str}.md")
    with open(md_filename, "w", encoding="utf-8") as f:
        f.write(md_content)
    logger.info(f"[INFO] Rapport Markdown enregistré : {md_filename}")

    # 2. Sauvegarde JSON brut
    report_data = DailyReportData(
        date=date_str,
        generated_at=datetime.utcnow().isoformat() + "Z",
        posts_scraped_total=posts_scraped_total,
        posts_after_filtering=posts_after_filtering,
        posts_sent_to_llm=posts_sent_to_llm,
        subreddit_breakdown=subreddit_breakdown,
        opportunities=opportunities,
        rejected_ideas=rejected_ideas
    )
    json_filename = os.path.join(data_dir, f"{date_str}.json")
    with open(json_filename, "w", encoding="utf-8") as f:
        f.write(report_data.model_dump_json(indent=2))
    logger.info(f"[INFO] Données JSON enregistrées : {json_filename}")

    return {
        "markdown_path": md_filename,
        "json_path": json_filename
    }
