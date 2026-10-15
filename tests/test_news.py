
import unittest
from unittest.mock import patch

from app.news_api import _remove_duplicates, search_news


class TestNewsAPI(unittest.TestCase):

    def test_removes_duplicate_urls(self):
        articles = [
            {"url": "https://example.com/1", "title": "First"},
            {"url": "https://example.com/1", "title": "Duplicate"},
            {"url": "https://example.com/2", "title": "Second"},
            {"title": "Missing URL"},
        ]

        result = _remove_duplicates(articles)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["title"], "First")
        self.assertEqual(result[1]["title"], "Second")

    @patch("app.news_api._request")
    def test_empty_keyword_returns_empty_list(self, mock_request):
        result = search_news("   ")

        self.assertEqual(result, [])
        mock_request.assert_not_called()

    @patch("app.news_api._request")
    def test_search_returns_articles(self, mock_request):
        mock_request.return_value = {
            "articles": [
                {
                    "url": "https://example.com/apple",
                    "title": "Apple technology news",
                    "description": "Apple product updates",
                }
            ]
        }

        result = search_news("Apple")

        self.assertEqual(len(result), 1)
        self.assertIn("Apple", result[0]["title"])
        mock_request.assert_called_once()


if __name__ == "__main__":
    unittest.main()
