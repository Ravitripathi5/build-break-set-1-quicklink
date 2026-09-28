"""QuickLink - a tiny URL shortener that runs on AWS Lambda behind a Function URL."""
import base64
import hashlib
import json
import os
import time

TABLE_NAME = os.environ.get("TABLE_NAME", "")
APP_VERSION = os.environ.get("APP_VERSION", "dev")

_table = None


def table():
    global _table
    if _table is None:
        import boto3

        _table = boto3.resource("dynamodb").Table(TABLE_NAME)
    return _table


def make_code(url):
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:8]


def response(status, body=None, headers=None):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json", **(headers or {})},
        "body": json.dumps(body if body is not None else {}),
    }


def read_body(event):
    raw = event.get("body") or "{}"
    if event.get("isBase64Encoded"):
        raw = base64.b64decode(raw).decode("utf-8")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


def lambda_handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method", "GET")
    path = event.get("rawPath", "/")

    if path == "/health":
        return response(200, {"status": "ok", "service": "quicklink", "version": APP_VERSION})

    if path == "/shorten" and method == "POST":
        url = str(read_body(event).get("url", ""))
        if not url.startswith(("https://", "http://")) or len(url) > 2048:
            return response(400, {"error": "url must start with http:// or https://"})
        code = make_code(url)
        table().put_item(Item={"code": code, "url": url, "created": int(time.time())})
        return response(201, {"code": code})

    if method == "GET" and len(path) > 1:
        item = table().get_item(Key={"code": path.lstrip("/")}).get("Item")
        if not item:
            return response(404, {"error": "not found"})
        return response(301, {"location": item["url"]}, {"Location": item["url"]})

    return response(404, {"error": "not found"})
