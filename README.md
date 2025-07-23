# StockDash — A Streamlit Stock Market Dashboard

**StockDash** is a clean and interactive stock market dashboard built using **Python**, **Streamlit**, and **yfinance**. It allows users to analyze stock prices, visualize historical data, and track key technical indicators like **RSI**, **MACD**, and **Moving Averages**.
This version of StockDash currently supports **Indian stock tickers** (e.g., `RELIANCE.NS`, `TCS.NS`, `HDFCBANK.NS`) using the Yahoo Finance API.

**Live Demo:** [Try StockDash on Streamlit](https://stockdash-uonjnyuvlaya9u43vbks7z.streamlit.app/)

---

### Features

- Interactive stock price chart
- Technical indicators:
  - Relative Strength Index (RSI)
  - Moving Average Convergence Divergence (MACD)
  - Simple Moving Average (SMA)
- Multiple timeframes (5 days to max historical)
- Data fetched live using yfinance
- Clean UI powered by Streamlit and Plotly

---

### Getting Started

#### Prerequisites

Install dependencies:

```bash
pip install -r requirements.txt
```

#### Run the app

```bash
streamlit run stockDash.py
```

---

### Dependencies

- `streamlit`
- `yfinance`
- `plotly`
- `ta`

All required libraries are listed in `requirements.txt`.
