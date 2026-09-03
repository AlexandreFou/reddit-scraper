"""
Unit tests for Pydantic models in src/models.py.
Verifies validation rules, default values, and schema integrity without any external API calls.
"""

import unittest
from src.models import (
    RedditPost,
    ScoringBreakdown,
    Opportunity,
    RejectedIdea,
    DailyReportData
)


class TestModels(unittest.TestCase):

    def test_reddit_post_creation(self):
        post = RedditPost(
            id="test_1",
            subreddit="r/startups",
            title="Need software for managing freelancer compliance",
            url="https://reddit.com/r/startups/test_1",
            score=42,
            num_comments=10
        )
        self.assertEqual(post.id, "test_1")
        self.assertEqual(post.subreddit, "r/startups")
        self.assertEqual(post.selftext, "")
        self.assertEqual(post.comments, [])
        self.assertEqual(post.score, 42)

    def test_scoring_breakdown_bounds(self):
        breakdown = ScoringBreakdown(
            problem_intensity=18,
            observable_demand=17,
            monetization_potential=14,
            market_size_niche=13,
            competition_saturation=8,
            launch_ease=9,
            ai_automation_potential=9,
            total_score=88,
            score_reasoning="High pain point and direct willingness to pay"
        )
        self.assertEqual(breakdown.total_score, 88)
        self.assertGreaterEqual(breakdown.problem_intensity, 0)
        self.assertLessEqual(breakdown.problem_intensity, 20)

    def test_opportunity_structure(self):
        opp = Opportunity(
            title="Invoice OCR for Trades",
            problem="Too many manual receipts",
            target_customer="Plumbers and electricians",
            opportunity="WhatsApp receipt matching bot",
            proposed_solution="Lightweight OCR + WhatsApp",
            why_now="Vision AI is accurate and cheap",
            monetization="$99/mo SaaS",
            launch_difficulty="Low (1 week)",
            ai_automation_potential="High",
            demand_signals=["User spends 15h a week", "Willing to pay $150"],
            risks=["Technician reluctance"],
            validation_steps=["Call 10 plumbers", "Test manual WhatsApp bot"],
            scoring=ScoringBreakdown(
                problem_intensity=19,
                observable_demand=18,
                monetization_potential=14,
                market_size_niche=13,
                competition_saturation=8,
                launch_ease=9,
                ai_automation_potential=9,
                total_score=90,
                score_reasoning="Strong demand"
            ),
            source_urls=["https://reddit.com/r/Entrepreneur/1"],
            source_subreddits=["r/Entrepreneur"]
        )
        self.assertEqual(opp.signal_count, 1)
        self.assertEqual(len(opp.demand_signals), 2)
        self.assertEqual(opp.scoring.total_score, 90)

    def test_rejected_idea(self):
        rej = RejectedIdea(
            title_or_topic="Crypto dog meme",
            reason="Spam without business problem",
            category="Spam/Promo"
        )
        self.assertEqual(rej.category, "Spam/Promo")


if __name__ == "__main__":
    unittest.main()
