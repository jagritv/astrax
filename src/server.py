from fastapi import FastAPI
from src.data_loader import fetch_stock_data, fetch_crypto_data
from typing import Optional

app = FastAPI(title = "Stock and Crypto Predictor API")

@app.get("/")

def root():
    return {"message": "Welcome to Stock and Crypto Predictor API"}

@app.get("/stock")
def get_stock(ticker: str, start: str, end: str):
    
    """
    Fetch stock data from Yahoo Finance.
    Example: /stock?ticker=AAPL&start=2023-01-01&end=2023-06-30
    """
    
    data = fetch_stock_data(ticker, start, end)
    return data.tail(5).to_dict()  

@app.get("/crypto")
def get_crypto(symbol: str="BTC/USDT", timeframe: str = "1d", limit: int=5):
    
    """
    Fetch crypto data from Binance via ccxt.
    Example: /crypto?symbol=BTC/USDT&timeframe=1d&limit=5
    """
    
    data = fetch_crypto_data(symbol, timeframe, limit)
    return data.to_dict()