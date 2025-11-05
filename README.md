# 📈 Notion Stock Prices Sync

Automatically fetch **US stock prices** from Yahoo Finance and update a Notion database using GitHub Actions.

---

## 🚀 Features
- Fetches **latest US stock prices** using [Yahoo Finance](https://pypi.org/project/yfinance/).
- Syncs tickers into a Notion database with:
  - ✅ Ticker symbol
  - ✅ Current Price
  - ✅ Last Updated timestamp
- Runs automatically every day at **5:00 AM IST** using GitHub Actions.
- Can also be triggered manually from the GitHub Actions tab.

---

## 🛠️ Setup

### 1. Clone this repo
```bash
git clone https://github.com/your-username/notion-stock-prices-sync.git
cd notion-stock-prices-sync
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Locally
```bash
python main.py
```

# Changelog:

2025-10-05: Updated script to use REST calls instead of SDK due to breaking changes in notion outlined in - https://developers.notion.com/docs/upgrade-guide-2025-09-03