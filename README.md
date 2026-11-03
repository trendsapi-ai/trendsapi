# Trends API

`POST https://api.trendsapi.ai/api` returns trend data for Google, TikTok, YouTube, Amazon, Pinterest, Reddit, X, Steam, npm and more: 53 data sets from 27 platforms.

Five operations (`mode`): history, growth, live ranks, context (what people are posting about a keyword) and top posts for a hashtag. One Bearer key covers all of them.

[Get a free key](https://trendsapi.ai/account) · [Pricing](https://trendsapi.ai/pricing) · [llms.txt](https://trendsapi.ai/llms.txt)

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![REST](https://img.shields.io/badge/REST-POST%20%2Fapi-blue.svg)](https://trendsapi.ai/docs)
[![Free tier](https://img.shields.io/badge/free-100%20req%2Fmo-orange.svg)](https://trendsapi.ai/pricing)

## Table of contents

* [Authentication](#authentication)
* [Quickstart](#quickstart)
* [HTTP response](#http-response)
* [Methods](#methods)
* [Request fields](#request-fields)
* [Keyword sources](#keyword-sources)
* [Live boards](#live-boards)
* [get_time_series](#get_time_series)
* [get_growth](#get_growth)
* [get_top_trends](#get_top_trends)
* [get_context](#get_context)
* [get_top_posts](#get_top_posts)
* [Errors](#errors)
* [Quota](#quota)
* [SDKs](#sdks)
* [Raw HTTP](#raw-http)
* [Per-source guides](#per-source-guides)

## Authentication

| Item | Value |
|---|---|
| Header | `Authorization: Bearer <key>` |
| Key | Issued at [trendsapi.ai/#get-key](https://trendsapi.ai/account) |
| Free quota | 100 successful calls / month, no card |

Do not put the key in client-side JavaScript or a public repo.

## Quickstart

Prefer a client. It returns decoded objects. You do not parse `body`.

```bash
pip install trendsapi
export TRENDSAPI_KEY=your_key
```

```python
from trendsapi import TrendsAPI

client = TrendsAPI()
print(client.get_top_trends(type="Google Trends", limit=5))
```

```bash
npm install trendsapi
```

```js
import { TrendsAPI } from "trendsapi";
const client = new TrendsAPI({ apiKey: process.env.TRENDSAPI_KEY });
console.log(await client.getTopTrends({ type: "Google Trends", limit: 5 }));
```

Same call over HTTP:

```bash
curl -sS -X POST https://api.trendsapi.ai/api \
  -H "Authorization: Bearer $TRENDSAPI_KEY" \
  -H "Content-Type: application/json" \
  -d '{"mode":"get_top_trends","type":"Google Trends","limit":5}'
```

If you skip the SDK, read [HTTP response](#http-response) before you parse anything.

## HTTP response

Successful JSON always looks like this:

| Field | Type | Meaning |
|---|---|---|
| `statusCode` | integer | Application status. `200` means the payload in `body` is usable |
| `body` | **string** | JSON text. Parse it a second time |

```json
{
  "statusCode": 200,
  "body": "[{\"date\":\"2026-03-21\",\"value\":47,\"keyword\":\"bitcoin\",\"source\":\"google search\"}]"
}
```

Python: `data = json.loads(res.json()["body"])`  
Node: `const data = JSON.parse((await res.json()).body)`

A missing key answers HTTP 401 (`missing_api_key`) and a wrong key HTTP 403 (`invalid_api_key`), with the error object as the body. A gateway timeout can return HTML (504). Check HTTP status before `.json()`. Only envelope `statusCode == 200` counts against quota.

## Methods

One URL. The JSON field `mode` selects the operation.

| `mode` | Returns | Required | Cost |
|---|---|---|---|
| `get_time_series` | About five years of weekly history for one keyword on one source, as a 0 to 100 index plus volume where the source has it. | `keyword`, `source` | 1 request per call |
| `get_growth` | Point-to-point growth over one or more windows, on one source or several in the same call. | `keyword`, `source` | 1 request per call, every window included |
| `get_top_trends` | A live ranked board with no keyword: the current leaders, or the biggest climbers against an earlier snapshot. | `type` | MCP: 1 request per 10 rows, at most 10 per call. REST: 1 request per call |
| `get_context` | What people are posting, reading and betting about a keyword right now: posts, videos, stories, comments and markets from each source, with engagement. | `keyword`, `source` | MCP: 1 request per source, at most 5 per call. REST: one source per call, 1 request |
| `get_top_posts` | Live top posts for one hashtag, fetched on every call. Business plan. | `keyword`, `source` | 1 request per call |

`get_top_posts` needs the Business plan. `get_trends` is an alias of `get_time_series`. Use `get_time_series` in new code.

Not available: related queries, related topics, hourly series.

## Request fields

| Field | Type | Used by | Required | Notes |
|---|---|---|---|---|
| `mode` | string | all | yes | One of the five values above |
| `source` | string | time series, growth, context, top posts | yes | See [keyword sources](#keyword-sources) and [get_context](#get_context) |
| `keyword` | string | time series, growth, context, top posts | yes | Format depends on `source` |
| `percent_growth` | array | growth | no | Default `["12M"]`. Strings and/or `{recent, baseline, name}` objects |
| `country` | string | time series, growth, top trends | no | ISO code (`US`, `GB`, `JP`). Google, YouTube, TikTok, Pinterest and some boards |
| `resolution` | string | time series, growth | no | Google and YouTube sources: `weekly` (default, about 5 years) or `daily` (last 90 days) |
| `language` | string | time series, growth | no | Wikipedia edition (`en`, `de`, `ja`) |
| `type` | string | top trends | yes | Exact board name. See [live boards](#live-boards) |
| `limit` | integer | top trends, context, top posts | no | Top trends 1 to 200 (default 25); context 1 to 20 per source (default 10); top posts 1 to 20 (default 20) |
| `offset` | integer | top trends | no | Default 0 |
| `sort` | string | top trends | no | `rank` (default) or `rank_change` for climbers |
| `window` | string | top trends | no | With `rank_change`: `1d` `3d` `7d` `14d` `30d` |
| `category` | string | top trends | no | The `by Category` boards and `Top Websites` |
| `days` | integer | context | no | Look back 1 to 30 days. Default 7 |
| `comments` | integer | context | no | Top comments for the first N items (0 to 5, default 2) |

`source` and `type` are different catalogs. `source: "Google Trends"` is 400. `type: "google search"` is 400.

## Keyword sources

`source` on `get_time_series` and `get_growth` (14). One source per time-series call. Growth may take a comma-separated list (`"amazon, tiktok, youtube"`).

| `source` | Returns | `keyword` |
|---|---|---|
| `Google Search` | Search interest as a 0–100 index, about 5 years | Any name or phrase (`electric vehicles`) |
| `Google Images` | Image search interest as a 0–100 index, about 5 years | Any name or phrase (`electric vehicles`) |
| `Google News` | News search interest as a 0–100 index, about 5 years | Any name or phrase (`electric vehicles`) |
| `Google Shopping` | Shopping search interest as a 0–100 index, about 5 years | Any name or phrase (`running shoes`) |
| `YouTube` | YouTube search interest as a 0–100 index, about 5 years | Any name or phrase (`stanley cup`) |
| `Wikipedia` | Article page views as a 0–100 index, plus raw views | Any name or phrase (`Bitcoin`) |
| `TikTok` | Hashtag views as a 0–100 index, plus raw views | Any name or phrase (`booktok`) |
| `Amazon` | Product search volume as a 0–100 index, plus raw volume | Any name or phrase (`air fryer`) |
| `Pinterest` | Pinterest search interest as a 0–100 index, about 2 years | Any name or phrase (`matcha`) |
| `npm` | Package downloads as a 0–100 index, plus raw downloads | Exact npmjs.com package name, case-sensitive (`langchain`) |
| `Python` | Package downloads as a 0–100 index, plus raw downloads | Exact PyPI project name (`pandas`) |
| `Steam` | Concurrent players as a 0–100 index, plus raw players | Game display name in plain English, not a Steam App ID (`Elden Ring`) |
| `App Downloads` | Android app downloads as a 0–100 index, plus raw downloads | Android bundle ID only (the id= value on Google Play) (`com.openai.chatgpt`) |
| `App Rankings` | Android chart rank as a 0–100 index, plus raw rank | Android bundle ID only (the id= value on Google Play) (`com.openai.chatgpt`) |

`chatgpt` on `App Downloads` is 404. Use the Play Store id after `?id=`.

Reddit, X, iOS charts, GitHub, Spotify, IMDb, Open Library, Substack, Polymarket and site rank are [live boards](#live-boards) (and some are [context sources](#get_context)), not `source` values for history.

## Live boards

`type` on `get_top_trends` (27). No `keyword`. Match spelling and capitalization exactly.

| `type` | Returns | Updated |
|---|---|---|
| `Amazon Best Sellers Top Rated` | Top-rated best sellers across all categories | Daily |
| `Amazon Best Sellers by Category` | Best sellers per product category | Daily |
| `App Store Top Free` | Top free iOS apps | Daily |
| `App Store Top Paid` | Top paid iOS apps | Daily |
| `GitHub` | Daily trending repositories | Daily |
| `Google News Top News` | Top news stories | Live |
| `Google Play` | Top Android apps | Daily |
| `Google Trends` | Trending searches right now | Live |
| `Google Trends by Category` | Trending searches per topic board | Live |
| `IMDb MOVIEmeter` | Most popular movies by user activity | Daily |
| `Open Library Trending Books` | Daily trending books | Daily |
| `Pinterest Trending` | Top Pinterest searches this month | Live |
| `Pinterest Trending by Category` | Top Pinterest searches this month per category | Live |
| `Polymarket Top Markets` | Prediction markets with the most money traded in the last 24 hours | Live |
| `Reddit Hot Posts` | Hottest posts on the front page | Live |
| `Reddit World News` | Top posts in r/worldnews | Live |
| `Top Websites` | Most-visited websites by traffic rank | Monthly |
| `Spotify Top Podcasts` | Top podcasts | Daily |
| `Steam Most Played` | Games by concurrent live players | Live |
| `Substack` | Top newsletters overall | Daily |
| `Substack by Category` | Top newsletters per category | Daily |
| `TikTok Trending Hashtags` | Trending hashtags | Daily |
| `TikTok Trending Hashtags by Category` | Trending hashtags per industry board | Daily |
| `TikTok Trending Searches` | Trending search terms | Daily |
| `Wikipedia Trending` | Most-viewed articles today | Daily |
| `X (Twitter) Trending` | Trending topics | Live |
| `YouTube Trending` | Trending videos | Daily |

Category names per board: [data catalog](https://trendsapi.ai/data-catalog.md).

## get_time_series

Weekly history for one `source` + `keyword`.

```json
{"mode": "get_time_series", "source": "google search", "keyword": "bitcoin"}
```

Parsed `body` is an **array of points**.

| Field | Type | Present | Meaning |
|---|---|---|---|
| `date` | string | always | ISO date (`YYYY-MM-DD`) |
| `value` | number | always | 0-100 index for this series (100 = peak in the returned window) |
| `keyword` | string | always | Echo of the request |
| `volume` | number | when the pipeline has it | Absolute volume (search, pageviews, downloads, and similar) |
| `source` | string | Google / YouTube / TikTok / Reddit-style series | Echo of `source` |
| `datatype` | string | Wikipedia / Amazon / npm / app series | Same role as `source` on those pipelines |
| `volume_cumulative` | number | `app downloads` | Cumulative downloads when provided |

Read `date` and `value` in application code. Treat `source` / `datatype` / `volume` as optional extras.

Every plan, Free included, gets the full history: about five years weekly.

## get_growth

Point-to-point percent change. Several windows in one call still count as **one** request.

```json
{
  "mode": "get_growth",
  "source": "google search",
  "keyword": "nike",
  "percent_growth": ["12M", "3M", "YTD"]
}
```

**Window strings:** `7D`, `14D`, `30D`, `1M`, `2M`, `3M`, `6M`, `9M`, `12M` (`1Y`), `18M`, `24M` (`2Y`), `36M` (`3Y`), `48M`, `60M` (`5Y`), `MTD`, `QTD`, `YTD`.

Custom window: `{"name": "Launch", "recent": "2024-06-01", "baseline": "2024-01-01"}`.

Default if omitted: `["12M"]`.

Parsed `body` object:

| Field | Type | Meaning |
|---|---|---|
| `search_term` | string | Keyword |
| `data_source` | string | Source |
| `results` | array | One object per requested window |
| `metadata` | object | `total_data_points`, `calculations_completed`, `all_successful` |

Each `results[]` item:

| Field | Type | Present | Meaning |
|---|---|---|---|
| `period` | string | always | Window label |
| `growth` | number | on success | Percent change |
| `direction` | string | on success | `increase` or `decrease` |
| `status` | string | always | e.g. `success` |
| `recent_date` | string | on success | End of window |
| `baseline_date` | string | on success | Start of window |
| `recent_value` | number | on success | Index at `recent_date` |
| `baseline_value` | number | on success | Index at `baseline_date` |
| `growth_unit` | string | often | e.g. `percent` |
| `calculation_method` | string | often | How the % was computed |
| `volume_available` | boolean | when volume exists | |
| `recent_volume` | number | when volume exists | |
| `baseline_volume` | number | when volume exists | |
| `volume_growth` | number | when volume exists | |

## get_top_trends

Live ranked feed. No keyword.

```json
{"mode": "get_top_trends", "type": "Google Trends", "limit": 10}
```

Parsed `body` object:

| Field | Type | Meaning |
|---|---|---|
| `as_of_ts` | string | Snapshot time (ISO 8601) |
| `type` | string | Feed name |
| `limit` | integer | Requested cap |
| `offset` | integer | Pagination offset |
| `count` | integer | Rows in `data` |
| `data` | array | `[rank, label]` pairs |

Labels are feed-specific (search term, video title, hostname, app name). They are not IDs.

Omitting `type` on REST returns every feed and is billed per feed. Send one `type` per call.

## get_context

What people are posting, reading and betting about a keyword right now, with engagement. REST takes one source per call (1 request).

```json
{"mode": "get_context", "source": "Reddit", "keyword": "nintendo switch 2", "days": 7, "limit": 10}
```

Sources: `News`, `YouTube`, `TikTok`, `Instagram`, `X`, `Reddit`, `Bluesky`, `Hacker News`, `Polymarket`, `GitHub`.

Parsed `body` object:

| Field | Type | Meaning |
|---|---|---|
| `keyword` | string | The keyword you asked for |
| `window_days` | number | How far back it looked |
| `sources[].source` | string | The source |
| `sources[].items[]` | array | Each item: `kind`, `url`, `title`, `text`, `author`, `published`, `engagement` (views, likes, comments, shares, score), `top_comments` |
| `sources[].error` | string or null | Why a source returned nothing, when it failed |

## get_top_posts

Live top posts for one hashtag, fetched on every call. **Business plan.** 1 request per call.

```json
{"mode": "get_top_posts", "source": "TikTok", "keyword": "booktok", "limit": 20}
```

Sources: `TikTok` and `Instagram`. Each `posts[]` item has `rank`, `caption`, `author`, `plays` / `likes` / `comments`, `posted` and `url`.

## Errors

Use envelope `statusCode`, not only HTTP status. Errors carry an `error` code and a `message`. Failed calls are free.

| Code | When | Retry? |
|---|---|---|
| 400 | `missing_parameter`, `invalid_source`, `invalid_mode`, `invalid_request`, `growth_calculation_failed` | No. Fix the body or the window |
| 401 (HTTP) | `missing_api_key`: no key sent | No. Send the key |
| 403 (HTTP) | `invalid_api_key`: key mistyped or regenerated | No. Copy the key from your account |
| 403 | `plan_required`: tool needs a higher plan (Top Posts: Business) | No. Upgrade |
| 404 | `no_data`: nothing for that keyword + source | No. Check spelling or keyword format |
| HTTP deny | `monthly_limit_reached`: monthly requests used and no credits left (the message links to credits and plans) | Buy credits or upgrade |
| 502 | `source_unavailable`: the upstream source did not answer | Yes, later |
| 500 | `internal_error` (body has a `request_id` for support) | Yes, with backoff |

```json
{
  "statusCode": 404,
  "body": "{\"error\":\"no_data\",\"message\":\"No data available for this keyword and source combination.\",\"keyword\":\"chatgpt\",\"source\":\"app downloads\"}"
}
```

## Quota

Only `statusCode` 200 is billed. Every plan reads every data set and the full history.

| Plan | Requests / month | Top trends rows | Price / month |
|---|---|---|---|
| Free | 100 | Top 10, 24h delay | $0 |
| Starter | 1,000 | Full board | $19 |
| Pro | 5,000 | Full board | $49 |
| Business | 25,000 | Full board | $199 |

Yearly billing: Starter $16/mo, Pro $39/mo, Business $159/mo. Top Posts is on Business.

**Pay as you go:** one-time credit packs, no subscription ($15 for 600, $49 for 2,500, $199 for 12,000 credits). 1 credit = 1 request. Credits never expire and are used after a plan's monthly requests run out. [Pricing](https://trendsapi.ai/pricing).

One billed request =

- `get_time_series`: 1 source + 1 keyword
- `get_growth`: 1 keyword (all windows included)
- `get_top_trends`: 1 `type`
- `get_context`: 1 source
- `get_top_posts`: 1 hashtag

## SDKs

| Language | Install | Repo |
|---|---|---|
| Python | `pip install trendsapi` | [TrendsAPI-py](https://github.com/trendsapi-ai/TrendsAPI-py) |
| JavaScript / TypeScript | `npm install trendsapi` | [trendsapi-js](https://github.com/trendsapi-ai/trendsapi-js) |

MCP transport (same data): [trends-mcp](https://github.com/trendsapi-ai/trends-mcp).

## Raw HTTP

Use this only if you are not installing a client.

```python
import json, os, requests

res = requests.post(
    "https://api.trendsapi.ai/api",
    headers={"Authorization": f"Bearer {os.environ['TRENDSAPI_KEY']}"},
    json={"mode": "get_time_series", "source": "google search", "keyword": "heat pump"},
    timeout=60,
)
res.raise_for_status()
env = res.json()
if env["statusCode"] != 200:
    raise RuntimeError(env)
series = json.loads(env["body"])
```

```js
const res = await fetch("https://api.trendsapi.ai/api", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${process.env.TRENDSAPI_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    mode: "get_time_series",
    source: "google search",
    keyword: "heat pump",
  }),
});
if (!res.ok) throw new Error(`HTTP ${res.status}`);
const env = await res.json();
if (env.statusCode !== 200) throw new Error(String(env.body));
const series = JSON.parse(env.body);
```

## Per-source guides

Job-specific. Not copies of this file.

| Job | Repository |
|---|---|
| Google search interest | [google-trends-api](https://github.com/trendsapi-ai/google-trends-api) |
| Replace pytrends | [pytrends-alternative](https://github.com/trendsapi-ai/pytrends-alternative) |
| TikTok hashtag volume | [tiktok-trends-api](https://github.com/trendsapi-ai/tiktok-trends-api) |
| YouTube search interest | [youtube-trends-api](https://github.com/trendsapi-ai/youtube-trends-api) |
| Amazon search demand | [amazon-trends-api](https://github.com/trendsapi-ai/amazon-trends-api) |
| Wikipedia page views | [wikipedia-trends-api](https://github.com/trendsapi-ai/wikipedia-trends-api) |
| npm downloads | [npm-trends-api](https://github.com/trendsapi-ai/npm-trends-api) |
| Steam concurrent players | [steam-trends-api](https://github.com/trendsapi-ai/steam-trends-api) |
| App Store / Play charts | [app-store-trends-api](https://github.com/trendsapi-ai/app-store-trends-api) |
| Site traffic rank | [web-traffic-api](https://github.com/trendsapi-ai/web-traffic-api) |

Every data set: [trendsapi.ai/data-catalog](https://trendsapi.ai/data-catalog).

## License

MIT. See [LICENSE](LICENSE). Hosted use follows the plan on the key.
