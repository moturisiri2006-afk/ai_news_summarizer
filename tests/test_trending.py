
import unittest

from app.trending import extract_keywords, extract_trending_topics


class TestTrendingTopics(unittest.TestCase):

    def test_removes_stop_words(self):
        keywords = extract_keywords("Apple launches new AI features")

        self.assertIn("apple", keywords)
        self.assertNotIn("launches", keywords)
        self.assertNotIn("new", keywords)

    def test_repeated_topics_are_ranked(self):
        articles = [
            {"title": "Apple launches AI features"},
            {"title": "Apple announces AI technology"},
            {"title": "Google develops AI tools"},
        ]

        topics = extract_trending_topics(articles)

        self.assertIn("apple", topics)
        self.assertIn("ai", topics)

    def test_empty_articles(self):
        self.assertEqual(extract_trending_topics([]), [])

    def test_missing_titles(self):
        topics = extract_trending_topics([{}, {"title": None}])

        self.assertEqual(topics, [])


if __name__ == "__main__":
    unittest.main()
