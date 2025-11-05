import os
import requests
import yfinance as yf
from datetime import datetime
from notion_client import Client

# --- CONFIG ---
NOTION_TOKEN = os.environ["NOTION_TOKEN"]  # your Notion integration token
DATASOURCE_ID = os.environ["DATASOURCE_ID"]  # your Notion database ID
NOTION_MIGRATION_VERSION = "2025-09-03"

# --- INIT ---
notion = Client(auth=NOTION_TOKEN)

url = f"https://api.notion.com/v1/data_sources/{DATASOURCE_ID}/query"
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2025-09-03",
    "Content-Type": "application/json",
}

query_resp = requests.post(url, headers=headers, json={})
query_resp_json = query.json()

tickers = {}
for page in query_resp_json["results"]:
    props = page["properties"]

    ticker_text = None
    if props["Ticker"]["rich_text"]:
        ticker_text = props["Ticker"]["rich_text"][0]["plain_text"]

    if ticker_text:
        tickers[ticker_text] = page["id"]

print("🔎 Found tickers:", tickers.keys())


# --- Step 2. Fetch all prices & store in a map ---
prices = {}
symbols = list(tickers.keys())

# Download last day's data
data = yf.download(symbols, period="1d", interval="1m")

# Take the latest close price for each symbol
last_prices = data["Close"].iloc[-1].to_dict()

for symbol, price in last_prices.items():
    if price and not str(price) == "nan":
        prices[symbol] = float(price)

print("💰 Prices fetched:", prices)


# --- Step 3. Use prices map to update Notion ---
for ticker, page_id in tickers.items():
    if ticker in prices:
        notion.pages.update(
            page_id=page_id,
            properties={
                "Current Price": {"number": prices[ticker]},
                "Price Last Updated": {"date": {"start": datetime.utcnow().isoformat()}}
            }
        )
        print(f"✅ Updated {ticker} → {prices[ticker]}")
    else:
        print(f"⚠️ No price available for {ticker}")
