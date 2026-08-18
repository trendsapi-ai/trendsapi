# Trends API

`POST https://api.trendsapi.ai/api` returns a 0-100 demand index for Google, TikTok, Amazon, Reddit, YouTube, Steam, npm, and related feeds.

Three operations (`mode`): history, growth, live ranks. One Bearer key covers all of them.

[Get a free key](https://trendsapi.ai/#get-key) · [Pricing](https://trendsapi.ai/#pricing) · [llms.txt](https://trendsapi.ai/llms.txt)

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![REST](https://img.shields.io/badge/REST-POST%20%2Fapi-blue.svg)](https://trendsapi.ai/#quickstart)
[![Free tier](https://img.shields.io/badge/free-100%20req%2Fmo-orange.svg)](https://trendsapi.ai/#pricing)

## Table of contents

* [Authentication](#authentication)
* [Quickstart](#quickstart)
* [HTTP response](#http-response)
* [Methods](#methods)
* [Request fields](#request-fields)
* [Keyword sources](#keyword-sources)
* [Live feeds](#live-feeds)
* [get_time_series](#get_time_series)
* [get_growth](#get_growth)
* [get_top_trends](#get_top_trends)
* [Errors](#errors)
* [Quota](#quota)
* [SDKs](#sdks)
* [Raw HTTP](#raw-http)
* [Per-source guides](#per-source-guides)

## Authentication

| Item | Value |
|---|---|
| Header | `Authorization: Bearer <key>` |
| Key | Issued at [trendsapi.ai/#get-key](https://trendsapi.ai/#get-key) |
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

If the **HTTP** status is not 200, the gateway may return HTML (504). Check HTTP status before `.json()`. Only envelope `statusCode == 200` counts against quota.

## Methods

One URL. The JSON field `mode` selects the operation.

| `mode` | Returns | Required |
|---|---|---|
| `get_time_series` | Weekly history for one keyword on one source | `source`, `keyword` |
| `get_growth` | Percent change over one or more windows | `source`, `keyword` |
| `get_top_trends` | Live ranked list for one feed | `type` |

`get_trends` is an alias of `get_time_series`. Use `get_time_series` in new code.

Not available: geo / region breakdown, related queries, related topics, hourly series, category filters on keyword sources.

## Request fields

| Field | Type | Used by | Required | Notes |
|---|---|---|---|---|
| `mode` | string | all | yes | One of the three values above |
| `source` | string | time series, growth | yes | Lowercase. See [keyword sources](#keyword-sources) |
| `keyword` | string | time series, growth | yes | Format depends on `source` |
| `percent_growth` | array | growth | no | Default `["12M"]`. Strings and/or `{recent, baseline}` objects |
| `type` | string | top trends | yes (prefer) | Exact feed name. See [live feeds](#live-feeds) |
| `limit` | integer | top trends | no | Default 25, max 200 |
| `offset` | integer | top trends | no | Default 0 |
| `category` | string | top trends | no | Only `Amazon Best Sellers by Category` and `Top Websites` |

`source` and `type` are different catalogs. `source: "Google Trends"` is 400. `type: "google search"` is 400.

## Keyword sources

`source` on `get_time_series` and `get_growth`. One source per time-series call. Growth may take a comma-separated list (`"amazon, tiktok, youtube"`).

| `source` | Signal | `keyword` must be |
|---|---|---|
| `google search` | Google search volume | Any phrase |
| `google images` | Image search volume | Any phrase |
| `google news` | News-tab search volume | Any phrase |
| `google shopping` | Shopping-tab search volume | Any phrase |
| `youtube` | YouTube search volume | Any phrase |
| `tiktok` | TikTok hashtag volume | Hashtag or topic (`#` optional) |
| `reddit` | Community / topic attention | Subreddit name, no `r/` |
| `amazon` | Amazon product search volume | Product name or category |
| `wikipedia` | Wikipedia page views | Article title or topic |
| `news volume` | Article mention volume | Any phrase |
| `news sentiment` | News tone | Any phrase |
| `app downloads` | Android download interest | Bundle ID, e.g. `com.openai.chatgpt` |
| `app rankings` | Android chart position | Bundle ID, e.g. `com.himshers.hims` |
| `npm` | npm weekly downloads | Exact package name (`react`, `@babel/core`) |
| `steam` | Monthly concurrent players | Game display name (`Elden Ring`) |

`chatgpt` on `app downloads` is 404. Use the Play Store id after `?id=`.

iOS charts, GitHub repos, Spotify, IMDb, Open Library, and global site rank are [live feeds](#live-feeds), not `source` values. There is no `source: "web traffic"`.

## Live feeds

`type` on `get_top_trends`. No `keyword`. Match spelling and capitalization exactly.

| `type` | Ranks |
|---|---|
| `Google Trends` | Google searches right now |
| `Google News Top News` | Google News stories |
| `TikTok Trending Hashtags` | TikTok hashtags |
| `TikTok Trending Searches` | TikTok in-app searches |
| `TikTok Shop Hot Products` | TikTok Shop products |
| `YouTube Trending` | YouTube videos |
| `X (Twitter) Trending` | Topics on X |
| `Reddit Hot Posts` | Reddit front page |
| `Reddit World News` | r/worldnews |
| `Wikipedia Trending` | Most-viewed articles today |
| `Amazon Best Sellers Top Rated` | Top-rated Amazon sellers |
| `Amazon Best Sellers by Category` | Category sellers (`category` filter) |
| `App Store Top Free` | iOS free chart |
| `App Store Top Paid` | iOS paid chart |
| `Google Play` | Play chart |
| `Top Websites` | Global traffic rank |
| `Spotify Top Podcasts` | Spotify podcasts |
| `Steam Most Played` | Live concurrent players |
| `GitHub Trending Repos` | Daily repos |
| `IMDb MOVIEmeter` | Movie activity |
| `Open Library Trending Books` | Books |

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

Free keys: 90 days, 24h delay. Paid: up to about five years weekly.

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

## Errors

Use envelope `statusCode`, not only HTTP status.

| Code | When | Retry? |
|---|---|---|
| 400 | Bad `mode` / `source` / `type`, or missing field | No. Fix the body |
| 401 | Missing or invalid key | No. Fix the key |
| 404 | No series for that keyword + source | No. Wrong spelling or wrong keyword format |
| 429 | Monthly quota used | No until the next cycle, or upgrade |
| 500 | Upstream error | Yes, with backoff |
| HTTP 504 HTML | Gateway timeout (seen on `news volume`) | Yes. Not billed |

```json
{
  "statusCode": 404,
  "body": "{\"error\":\"no_data\",\"message\":\"No data available for this keyword and source combination.\",\"keyword\":\"chatgpt\",\"source\":\"app downloads\"}"
}
```

## Quota

Only `statusCode` 200 is billed.

| Plan | Requests / month | Freshness | History |
|---|---|---|---|
| Free | 100 | 24h delay | 90 days |
| Starter | 5,000 | real-time | 1 year |
| Pro | 25,000 | real-time | 5 years |
| Business | 100,000 | real-time | full archive |

One billed request =

- `get_time_series`: 1 source + 1 keyword
- `get_growth`: 1 source + 1 keyword (all windows included)
- `get_top_trends`: 1 `type`

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
| Reddit attention | [reddit-trends-api](https://github.com/trendsapi-ai/reddit-trends-api) |
| Amazon search demand | [amazon-trends-api](https://github.com/trendsapi-ai/amazon-trends-api) |
| Wikipedia page views | [wikipedia-trends-api](https://github.com/trendsapi-ai/wikipedia-trends-api) |
| npm downloads | [npm-trends-api](https://github.com/trendsapi-ai/npm-trends-api) |
| Steam concurrent players | [steam-trends-api](https://github.com/trendsapi-ai/steam-trends-api) |
| App Store / Play charts | [app-store-trends-api](https://github.com/trendsapi-ai/app-store-trends-api) |
| News mention volume | [news-trends-api](https://github.com/trendsapi-ai/news-trends-api) |
| News tone | [news-sentiment-api](https://github.com/trendsapi-ai/news-sentiment-api) |
| Site traffic rank | [web-traffic-api](https://github.com/trendsapi-ai/web-traffic-api) |

Site: [trendsapi.ai/trends](https://trendsapi.ai/trends).

## License

MIT. See [LICENSE](LICENSE). Hosted use follows the plan on the key.
