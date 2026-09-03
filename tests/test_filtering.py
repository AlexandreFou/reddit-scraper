"""
Unit tests for heuristic filtering in src/filtering.py.
Verifies spam rejection, motivation post elimination, and intent detection.
"""

import unittest
from src.models import RedditPost
from src.filtering import calculate_relevance_score, filter_and_rank_posts


class TestFiltering(unittest.TestCase):

    def test_noise_and_spam_rejected(self):
        spam_post = RedditPost(
            id="spam_1",
            subreddit="r/startups",
            title="Check out my new dog crypto token! Free airdrop!",
            selftext="Join our telegram and get free tokens right now! To the moon!",
            url="https://reddit.com/r/startups/spam_1"
        )
        score, reason = calculate_relevance_score(spam_post)
        self.assertEqual(score, 0.0)
        self.assertIn("Spam", reason)

    def test_motivational_fluff_rejected(self):
        motivation_post = RedditPost(
            id="mot_1",
            subreddit="r/Entrepreneur",
            title="Motivational Monday: Never give up on your dreams!",
            selftext="Grindset mindset! Steve Jobs and Elon Musk never stopped grinding.",
            url="https://reddit.com/r/Entrepreneur/mot_1"
        )
        score, reason = calculate_relevance_score(motivation_post)
        self.assertLess(score, 25.0)

    def test_high_intent_problem_qualified(self):
        problem_post = RedditPost(
            id="prob_1",
            subreddit="r/smallbusiness",
            title="We spend hours every week because our biggest pain point is matching invoices. Is there a tool for this?",
            selftext="I hate using Excel and our manual process is completely error-prone. We would gladly pay $150 a month for any software that automates invoice matching.",
            url="https://reddit.com/r/smallbusiness/prob_1",
            num_comments=16,
            comments=["Exact same problem in our agency!", "We would pay for this too."]
        )
        score, reason = calculate_relevance_score(problem_post)
        self.assertGreaterEqual(score, 50.0)
        self.assertEqual(reason, "Candidat qualifié")

    def test_filter_and_rank_posts(self):
        posts = [
            RedditPost(
                id="1",
                subreddit="r/Entrepreneur",
                title="Is there a software to automate subcontractor compliance?",
                selftext="We spend hours every week managing manual PDFs. Would pay 200/mo.",
                url="https://reddit.com/1",
                num_comments=20,
                comments=["Same issue here!"]
            ),
            RedditPost(
                id="2",
                subreddit="r/startups",
                title="Join my telegram for crypto signals",
                selftext="Free tokens",
                url="https://reddit.com/2"
            )
        ]
        qualified, rejected = filter_and_rank_posts(posts)
        self.assertEqual(len(qualified), 1)
        self.assertEqual(qualified[0].id, "1")
        self.assertGreaterEqual(len(rejected), 1)


if __name__ == "__main__":
    unittest.main()
