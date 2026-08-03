# Trends API - Google, TikTok, Amazon & 30+ trend sources as JSON

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE) [![API v1](https://img.shields.io/badge/API-v1-blue.svg)](https://trendsapi.ai) [![MCP compatible](https://img.shields.io/badge/MCP-compatible-blueviolet.svg)](https://modelcontextprotocol.io) [![Free tier](https://img.shields.io/badge/free%20tier-100%20req%2Fmo-orange.svg)](https://trendsapi.ai/#pricing)

> **One score. Every platform.** Trends API normalizes Google, TikTok, Amazon, Reddit, YouTube, Steam, npm and more into a single 0-100 trend score, served from one REST endpoint as clean JSON. Built for developers and AI agents.

**100 requests/month free** · No credit card · 60 seconds to your first call

**Docs:** [https://trendsapi.ai/#quickstart](https://trendsapi.ai/#quickstart) · **llms.txt:** [https://trendsapi.ai/llms.txt](https://trendsapi.ai/llms.txt) · **Pricing:** [https://trendsapi.ai/#pricing](https://trendsapi.ai/#pricing)

---

## The whole point

Messy platform metrics in. One 0-100 score out.

Search volume, hashtag counts, concurrent players, package downloads: different units, different scales, different APIs. Trends API normalizes all of it, so a TikTok hashtag and an npm package become directly comparable.

```
Google search interest ─┐
TikTok hashtag views ───┤
Amazon search volume ───┼──> NORMALIZE ──> 74/100  ("creatine gummies", all sources)
Steam players ──────────┤
npm weekly downloads ───┘
```

## Quickstart

```bash
curl -X POST https://api.trendsapi.ai/api \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"mode": "get_growth", "source": "tiktok", "keyword": "ai agents", "percent_growth": ["12M"]}'
```

```json
{ "keyword": "ai agents", "source": "tiktok", "growth": { "12M": 340.2 } }
```

Get your free key at [https://trendsapi.ai/#get-key](https://trendsapi.ai/#get-key).

## Three modes, one endpoint, one schema

| Mode | What it returns | Example |
|---|---|---|
| `get_time_series` | Historical trend series for a keyword on one source | `{"mode":"get_time_series","source":"google search","keyword":"bitcoin"}` |
| `get_growth` | Growth % over 3M / 6M / 12M / 5Y | `{"mode":"get_growth","source":"tiktok","keyword":"bitcoin","percent_growth":["12M"]}` |
| `get_top_trends` | Live trending feeds, no keyword needed | `{"mode":"get_top_trends","type":"Google Trends","limit":10}` |

## Coverage

### 15 keyword sources

| Source | `source` value | What it measures |
|---|---|---|
| Google Search | `google search` | Search volume |
| Google Images | `google images` | Image search volume |
| Google News | `google news` | News search volume |
| Google Shopping | `google shopping` | Shopping search volume |
| YouTube | `youtube` | Search volume |
| TikTok | `tiktok` | Hashtag volume |
| Reddit | `reddit` | Subreddit subscribers |
| Amazon | `amazon` | Product search volume |
| Wikipedia | `wikipedia` | Page views |
| News volume | `news volume` | Article mention volume |
| News sentiment | `news sentiment` | Positive / negative score |
| App downloads | `app downloads` | Android downloads (AppBrain) |
| App rankings | `app rankings` | Android chart position |
| npm | `npm` | Weekly package downloads |
| Steam | `steam` | Concurrent players (monthly) |

### 21 live feeds

| Feed | `type` value |
|---|---|
| Google Trends | `Google Trends` |
| Google News Top News | `Google News Top News` |
| TikTok Trending Hashtags | `TikTok Trending Hashtags` |
| TikTok Trending Searches | `TikTok Trending Searches` |
| TikTok Shop Hot Products | `TikTok Shop Hot Products` |
| YouTube Trending | `YouTube Trending` |
| X (Twitter) Trending | `X (Twitter) Trending` |
| Reddit Hot Posts | `Reddit Hot Posts` |
| Reddit World News | `Reddit World News` |
| Wikipedia Trending | `Wikipedia Trending` |
| Amazon Best Sellers Top Rated | `Amazon Best Sellers Top Rated` |
| Amazon Best Sellers by Category | `Amazon Best Sellers by Category` |
| App Store Top Free | `App Store Top Free` |
| App Store Top Paid | `App Store Top Paid` |
| Google Play | `Google Play` |
| Top Websites | `Top Websites` |
| Spotify Top Podcasts | `Spotify Top Podcasts` |
| Steam Most Played | `Steam Most Played` |
| GitHub Trending Repos | `GitHub Trending Repos` |
| IMDb MOVIEmeter | `IMDb MOVIEmeter` |
| Open Library Trending Books | `Open Library Trending Books` |

## Official clients

| Client | Repo | Install |
|---|---|---|
| Python | [trendsapi-py](https://github.com/trendsapi/trendsapi-py) | `pip install trendsapi` |
| JavaScript / TypeScript | [trendsapi-js](https://github.com/trendsapi/trendsapi-js) | `npm install trendsapi` |

## Per-source guides

| Source | Repo |
|---|---|
| Google Trends (pytrends alternative) | [google-trends-api](https://github.com/trendsapi/google-trends-api) · [pytrends-alternative](https://github.com/trendsapi/pytrends-alternative) |
| TikTok | [tiktok-trends-api](https://github.com/trendsapi/tiktok-trends-api) |
| YouTube | [youtube-trends-api](https://github.com/trendsapi/youtube-trends-api) |
| Reddit | [reddit-trends-api](https://github.com/trendsapi/reddit-trends-api) |
| Amazon | [amazon-trends-api](https://github.com/trendsapi/amazon-trends-api) |
| Wikipedia | [wikipedia-trends-api](https://github.com/trendsapi/wikipedia-trends-api) |
| npm | [npm-trends-api](https://github.com/trendsapi/npm-trends-api) |
| Steam | [steam-trends-api](https://github.com/trendsapi/steam-trends-api) |
| App Store / Google Play | [app-store-trends-api](https://github.com/trendsapi/app-store-trends-api) |
| News volume | [news-trends-api](https://github.com/trendsapi/news-trends-api) |
| News sentiment | [news-sentiment-api](https://github.com/trendsapi/news-sentiment-api) |
| Web traffic | [web-traffic-api](https://github.com/trendsapi/web-traffic-api) |
| MCP server | [trends-mcp](https://github.com/trendsapi/trends-mcp) |

---

## Use it from your AI assistant (MCP)

The same API key powers the Trends API MCP server, so Claude, Cursor, VS Code, ChatGPT and any MCP-compatible client can query this data in natural language.

[**+ Add to Cursor (one click)**](cursor://anysphere.cursor-deeplink/mcp/install?name=trendsapi&config=eyJ1cmwiOiAiaHR0cHM6Ly9hcGkudHJlbmRzYXBpLmFpL21jcCIsICJoZWFkZXJzIjogeyJBdXRob3JpemF0aW9uIjogIkJlYXJlciBZT1VSX0FQSV9LRVkifX0=)

**Cursor / Windsurf / Cline** (`~/.cursor/mcp.json` or equivalent):

```json
{
  "mcpServers": {
    "trendsapi": {
      "url": "https://api.trendsapi.ai/mcp",
      "transport": "http",
      "headers": { "Authorization": "Bearer YOUR_API_KEY" }
    }
  }
}
```

**VS Code / GitHub Copilot** (`.vscode/mcp.json`):

```json
{
  "servers": {
    "trendsapi": {
      "type": "http",
      "url": "https://api.trendsapi.ai/mcp",
      "headers": { "Authorization": "Bearer YOUR_API_KEY" }
    }
  }
}
```

**Claude Desktop** (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "trendsapi": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://api.trendsapi.ai/mcp", "--header", "Authorization:${AUTH_HEADER}"],
      "env": { "AUTH_HEADER": "Bearer YOUR_API_KEY" }
    }
  }
}
```

**Claude.ai (browser):** Settings -> Connectors -> Add custom connector -> `https://api.trendsapi.ai/mcp`

Then ask things like:

```
How did "creatine gummies" grow on TikTok vs Google over the last 12 months?
What is trending on YouTube right now?
```

---

## Agent-native by design

A growing share of first contact with an API is an AI agent reading the docs on a developer's behalf. Trends API is ready for them:

- **`/llms.txt` at the root** - the whole API, modes, sources and examples in one machine-readable file
- **MCP server included** - Claude, ChatGPT and Cursor query the same data with natural language; your API key works there too
- **One response shape** - parse it once and every source, feed and keyword just works

## Pricing

| Plan | Lookups/mo | Data | History |
|---|---|---|---|
| Free | 100 | 24h delayed | 90 days |
| Starter ($29) | 5,000 | real-time | 1 year |
| Pro ($99) | 25,000 | real-time | 5 years |
| Business ($299) | 100,000 | real-time | full archive |

Every plan includes all 15 keyword sources and all 21 live feeds. Failed and cached requests are never charged.

---

## Links

- **Docs & quickstart:** [https://trendsapi.ai/#quickstart](https://trendsapi.ai/#quickstart)
- **llms.txt (machine-readable API reference):** [https://trendsapi.ai/llms.txt](https://trendsapi.ai/llms.txt)
- **Pricing (free tier: 100 requests/month):** [https://trendsapi.ai/#pricing](https://trendsapi.ai/#pricing)
- **Get an API key:** [https://trendsapi.ai/#get-key](https://trendsapi.ai/#get-key)

## License

MIT - see [LICENSE](LICENSE). Data is served by [Trends API](https://trendsapi.ai); usage of the API itself is subject to the plan limits on your key.
