import json
import unittest

import handler


class FakeTable:
    def __init__(self):
        self.items = {}

    def put_item(self, Item):
        self.items[Item["code"]] = Item

    def get_item(self, Key):
        item = self.items.get(Key["code"])
        return {"Item": item} if item else {}


def event(method, path, body=None):
    return {
        "rawPath": path,
        "requestContext": {"http": {"method": method}},
        "body": json.dumps(body) if body is not None else None,
    }


class QuickLinkTest(unittest.TestCase):
    def setUp(self):
        handler._table = FakeTable()

    def test_health(self):
        res = handler.lambda_handler(event("GET", "/health"), None)
        self.assertEqual(res["statusCode"], 200)
        self.assertEqual(json.loads(res["body"])["service"], "quicklink")

    def test_shorten_then_redirect(self):
        res = handler.lambda_handler(event("POST", "/shorten", {"url": "https://example.com/a"}), None)
        self.assertEqual(res["statusCode"], 201)
        code = json.loads(res["body"])["code"]
        res = handler.lambda_handler(event("GET", "/" + code), None)
        self.assertEqual(res["statusCode"], 301)
        self.assertEqual(res["headers"]["Location"], "https://example.com/a")

    def test_rejects_bad_scheme(self):
        res = handler.lambda_handler(event("POST", "/shorten", {"url": "javascript:alert(1)"}), None)
        self.assertEqual(res["statusCode"], 400)

    def test_unknown_code(self):
        res = handler.lambda_handler(event("GET", "/nope1234"), None)
        self.assertEqual(res["statusCode"], 404)


if __name__ == "__main__":
    unittest.main()
