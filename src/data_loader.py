import yfinance as yf
import ccxt
import pandas as pd


def fetch_stock_data(symbol: str, start: str, end: str) -> pd.DataFrame:
    """
    Fetch stock data from Yahoo Finance with Date as a column.
    Example: fetch_stock_data("AAPL", "2023-01-01", "2023-12-31")
    """
    df = yf.download(symbol, start=start, end=end)
    
    # Fix MultiIndex columns by keeping only the first level (attribute names)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]
    
    # Reset index to move Date from index to a column
    df = df.reset_index()
    
    return df



def fetch_crypto_data(symbol: str = "BTC/USDT", timeframe: str = "1D", limit: int = 100) -> pd.DataFrame:
    
    # Fetch OHLCV crypto data from binance using ccxt.
    # Example: fetch_crypto_data("ETH/USDT", "4h", 200)
    
    binance = ccxt.binance()
    ohlcv = binance.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df
