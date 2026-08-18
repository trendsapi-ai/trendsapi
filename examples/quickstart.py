"""Trends API quickstart. Get a free key at https://trendsapi.ai/#get-key"""
import json, os

import requests

res = requests.post(
    "https://api.trendsapi.ai/api",
    headers={"Authorization": f"Bearer {os.environ['TRENDSAPI_KEY']}"},
    json={"mode": "get_top_trends", "type": "Google Trends", "limit": 10},
    timeout=60,
)
res.raise_for_status()
env = res.json()
print(json.loads(env["body"]) if env.get("statusCode") == 200 else env)
