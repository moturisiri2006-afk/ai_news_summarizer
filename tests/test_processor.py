
import unittest

from app.processor import prepare_article


class TestPrepareArticle(unittest.TestCase):

    def test_includes_title_and_description(self):
        article = {
            "title": "Apple announces a new device",
            "description": "The company revealed a new product.",
            "content": "More details about the product.",
        }

        result = prepare_article(article)

        self.assertIn("Apple announces a new device", result)
        self.assertIn("The company revealed a new product.", result)
        self.assertIn("More details about the product.", result)

    def test_handles_missing_fields(self):
        result = prepare_article({})

        self.assertEqual(result, "")

    def test_removes_duplicate_text(self):
        article = {
            "title": "Technology news",
            "description": "Technology news",
            "content": "",
        }

        result = prepare_article(article)

        self.assertEqual(result.count("Technology news"), 1)


if __name__ == "__main__":
    unittest.main()
