import os
from fastmcp import FastMCP
from typing import Annotated, Dict
from pydantic import Field
import yfinance as yf


stock_mcp = FastMCP(
    name="Stock MCP server", instructions="Your taks is to provide in depth updates on current stock prices"
)





# 2) Define your tool as before
@stock_mcp.tool(
    name="get_current_price",
    description="Fetches the latest current price for a given stock ticker symbol.",
    
)
def get_current_price(ticker: Annotated[str, Field(description="Stock ticker symbol.")]) -> Dict[str, float]:


    print(f"[DEBUG] Entered get_current_price with ticker={ticker!r}")  # function‐entry log
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d")
    if data.empty:
        print("[DEBUG] No data returned for ticker")  # empty case
        return {"ticker": ticker, "price": None}
    price = float(data["Close"].iloc[-1])
    print(f"[DEBUG] Retrieved price={price}")        # success case
    return {"price": price}



@stock_mcp.tool(
    name="get_historical_prices",
    description="Fetches daily historical price data for a given stock between two dates."
)
def get_historical_prices(
    ticker: Annotated[str, Field(description="Stock ticker symbol.")],
    start_date: Annotated[str, Field(description="Start date in YYYY-MM-DD format.")],
    end_date: Annotated[str, Field(description="End date in YYYY-MM-DD format.")]
) -> Dict[str, Dict[str, float]]:
    """
    Returns a dict mapping dates to OHLC prices for the specified ticker.
    """
    hist = yf.Ticker(ticker).history(start=start_date, end=end_date)
    results: Dict[str, Dict[str, float]] = {}
    for idx, row in hist.iterrows():
        date_str = idx.strftime("%Y-%m-%d")
        results[date_str] = {
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"]),
            "volume": int(row["Volume"])
        }
    return results


@stock_mcp.tool(
    name="get_company_profile",
    description="Fetches basic company profile information for the given stock ticker."
)
def get_company_profile(
    ticker: Annotated[str, Field(description="Stock ticker symbol.")]
) -> Dict[str, str]:
    """
    Returns company info such as name, sector, industry, and website.
    """
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        "ticker": ticker,
        "longName": info.get("longName", ""),
        "sector": info.get("sector", ""),
        "industry": info.get("industry", ""),
        "website": info.get("website", "")
    }


@stock_mcp.tool(
    name="get_market_news",
    description="Fetches the latest news headlines and URLs related to the given stock ticker."
)
def get_market_news(
    ticker: Annotated[str, Field(description="Stock ticker symbol to fetch news for.")]
) -> Dict[str, str]:
    """
    Returns a mapping from headline to URL for recent news articles about the ticker.
    """
    stock = yf.Ticker(ticker)
    news_items = stock.news
    results: Dict[str, str] = {}
    for item in news_items:
        title = item.get("title", "No title")
        link = item.get("link", "")
        results[title] = link
    return results