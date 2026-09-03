"""
Unit tests for scoring matrix and deduplication in src/scoring.py.
"""

import unittest
from src.models import Opportunity, ScoringBreakdown
from src.scoring import validate_and_recalc_score, deduplicate_opportunities, rank_opportunities


def make_opportunity(title: str, total_score: int, target: str = "Small business", url: str = "https://reddit.com/1") -> Opportunity:
    # Répartit proportionnellement le score sur les 7 composantes
    factor = total_score / 100.0
    intensity = int(round(20 * factor))
    demand = int(round(20 * factor))
    monetization = int(round(15 * factor))
    market = int(round(15 * factor))
    competition = int(round(10 * factor))
    launch = int(round(10 * factor))
    remaining = total_score - (intensity + demand + monetization + market + competition + launch)
    ai_pot = max(0, min(10, remaining))

    return Opportunity(
        title=title,
        problem="High friction manual work",
        target_customer=target,
        opportunity="Software solution",
        proposed_solution="Automated web app",
        why_now="New APIs",
        monetization="SaaS",
        launch_difficulty="Easy",
        ai_automation_potential="High",
        demand_signals=["Multiple user complaints"],
        risks=["Low barrier to entry"],
        validation_steps=["Interview 5 customers"],
        scoring=ScoringBreakdown(
            problem_intensity=intensity,
            observable_demand=demand,
            monetization_potential=monetization,
            market_size_niche=market,
            competition_saturation=competition,
            launch_ease=launch,
            ai_automation_potential=ai_pot,
            total_score=total_score,
            score_reasoning="Calculated score"
        ),
        source_urls=[url],
        source_subreddits=["r/startups"]
    )



class TestScoring(unittest.TestCase):

    def test_recalc_score(self):
        opp = make_opportunity("Tool A", 50)
        opp.scoring.problem_intensity = 20
        opp.scoring.observable_demand = 20
        opp.scoring.monetization_potential = 15
        opp.scoring.market_size_niche = 15
        opp.scoring.competition_saturation = 10
        opp.scoring.launch_ease = 10
        opp.scoring.ai_automation_potential = 10
        validated = validate_and_recalc_score(opp)
        self.assertEqual(validated.scoring.total_score, 100)

    def test_deduplication(self):
        opp1 = make_opportunity("Invoice Reconciliation for Plumbers", 85, target="Plumbers", url="https://reddit.com/post_1")
        opp2 = make_opportunity("Invoice Reconciliation for Plumbers & Trades", 82, target="Plumbers", url="https://reddit.com/post_2")

        deduped = deduplicate_opportunities([opp1, opp2])
        self.assertEqual(len(deduped), 1)
        self.assertEqual(deduped[0].signal_count, 2)
        self.assertIn("https://reddit.com/post_1", deduped[0].source_urls)
        self.assertIn("https://reddit.com/post_2", deduped[0].source_urls)

    def test_ranking_order(self):
        opp_low = make_opportunity("Marketing Automation for Dentists", 60, target="Dentists", url="https://reddit.com/dentists")
        opp_high = make_opportunity("Subcontractor Safety Compliance Tool", 92, target="General Contractors", url="https://reddit.com/contractors")

        ranked = rank_opportunities([opp_low, opp_high])
        self.assertEqual(len(ranked), 2)
        self.assertEqual(ranked[0].title, "Subcontractor Safety Compliance Tool")
        self.assertGreater(ranked[0].scoring.total_score, ranked[1].scoring.total_score)


if __name__ == "__main__":
    unittest.main()
