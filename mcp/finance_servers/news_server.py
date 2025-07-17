import requests
from datetime import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from fastmcp import FastMCP
from typing import Annotated, Dict
from pydantic import Field

load_dotenv()

# ---- API KEYS ----
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")


news_mcp = FastMCP(
    name="news MCP server", instructions="Your task is to provide context news articles using the tools below"
)



@news_mcp.tool(
    name="get_top_financial_news",  # ✅ use underscores instead of spaces
    description="Grab all of the important headlines from newsapi"
)
# ---------- NEWSAPI.ORG ----------
def get_top_financial_news(count: Annotated[int, Field(description="The number of top news articles to get, default is 5")] = 5) -> list[dict[str, str]]:
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "category": "business",
        "language": "en",
        "pageSize": count,
        "apiKey": NEWS_API_KEY
    }
    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        data = res.json()
        return [
            {"title": a["title"], "url": a["url"], "source": a["source"]["name"]}
            for a in data.get("articles", [])
        ]
    except Exception as e:
        return [{"error": str(e)}]


@news_mcp.tool(
    name="search_news_topic",
    description="Search a specified news topic"
) 
def search_news_topic(query: Annotated[str, Field(description="The topic to search for")], count: Annotated[int, Field(description="The number of articles to find, default is 5")] = 5) -> list[dict[str, str]] :
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": count,
        "apiKey": NEWS_API_KEY
    }
    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        data = res.json()
        return [
            {"title": a["title"], "url": a["url"], "published": a["publishedAt"]}
            for a in data.get("articles", [])
        ]
    except Exception as e:
        return [{"error": str(e)}]

@news_mcp.tool(
    name="get_headlines_from_finviz",  # 
    description="Grab all of the important headlines from Finviz news"
)
# ---------- FINVIZ SCRAPER ----------
def get_finviz_headlines() -> list[dict[str, str]]:
    url = "https://finviz.com/news.ashx"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        soup = BeautifulSoup(res.content, "html.parser")

        headlines = []
        for row in soup.select(".news_link"):
            title = row.text.strip()
            href = row.get("href")
            if title and href:
                headlines.append({"title": title, "url": href})
        return headlines[:5]
    except Exception as e:
        return [{"error": str(e)}]


# ---------- ALPHA VANTAGE NEWS ----------

@news_mcp.tool(
    name="alpha_vantage_company_news",
    description="Get company-specific news headlines using Alpha Vantage"
)
def alpha_vantage_company_news(
    symbol: Annotated[str, Field(description="The stock symbol (e.g., AAPL, TSLA, MSFT) to retrieve news for")]
) -> list[dict[str, str]]:
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "NEWS_SENTIMENT",
        "tickers": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        data = res.json()
        return [
            {"title": a["title"], "url": a["url"], "summary": a.get("summary", "")}
            for a in data.get("feed", [])[:5]
        ]
    except Exception as e:
        return [{"error": str(e)}]
