#!/usr/bin/env bash
# Get a free key at https://trendsapi.ai/#get-key
curl -X POST https://api.trendsapi.ai/api \
  -H "Authorization: Bearer $TRENDSAPI_KEY" \
  -H "Content-Type: application/json" \
  -d '{"mode": "get_top_trends", "type": "Google Trends", "limit": 10}'
