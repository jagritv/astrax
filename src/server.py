from fastapi import FastAPI
from src.data_loader import fetch_stock_data, fetch_crypto_data
from typing import Optional

app = FastAPI(title = "Stock and Crypto Predictor API")

@app.get("/")

def root():
    return {"message": "Welcome to Stock and Crypto Predictor API"}

@app.get("/stock")
def get_stock(symbol: str, start: str, end: str):
    """
    Fetch stock data from Yahoo Finance.
    Example: /stock?symbol=AAPL&start=2023-01-01&end=2023-06-30
    """
    data = fetch_stock_data(symbol, start, end)
    return data.tail(10).to_dict(orient="records")


@app.get("/crypto")
def get_crypto(symbol: str = "BTC/USDT", timeframe: str = "1d", limit: int = 5):
    """
    Fetch crypto data from Binance via ccxt.
    Example: /crypto?symbol=BTC/USDT&timeframe=1d&limit=5
    """
    data = fetch_crypto_data(symbol, timeframe, limit)
    return data.to_dict(orient="records")


@app.get("/predict")
def predict(symbol: str, type: str = "stock", window: int = 20):
    """
    Predict the next price.
    type: "stock" or "crypto"
    window: number of past days to use
    """
    
    if type == "stock":
        # Use a safer date range - current date minus 1 year to current date
        from datetime import datetime, timedelta
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        
        data = fetch_stock_data(symbol, start=start_date, end=end_date)
        
    else:
        data = fetch_crypto_data(symbol, timeframe="1d", limit=window+1)
        
    # Simple linear regression on 'close' prices
    from sklearn.linear_model import LinearRegression
    import numpy as np
    
    # Handle potential column name differences
    close_col = 'close' if 'close' in data.columns else 'Close'
    
    prices = data[close_col].values[-window:]
    X = np.arange(window).reshape(-1, 1)
    Y = prices
    model = LinearRegression()
    model.fit(X, Y)
    next_price = model.predict(np.array([[window]]))[0]
    
    return {"symbol": symbol, "predicted_next_close": next_price}