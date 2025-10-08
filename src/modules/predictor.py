from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from src.data_loader import fetch_stock_data, fetch_crypto_data
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import numpy as np

router = APIRouter(
    prefix="/predict",
    tags=["predictions"],
)

@router.get("/")
@cache(expire=300)  # Cache for 5 minutes
def predict(symbol: str, type: str = "stock", window: int = 20):
    """
    Predict the next price.
    type: "stock" or "crypto"
    window: number of past days to use
    """
    
    if type == "stock":
        # Use a safer date range - current date minus 1 year to current date
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        
        data = fetch_stock_data(symbol, start=start_date, end=end_date)
        
    else:
        data = fetch_crypto_data(symbol, timeframe="1d", limit=window+1)
        
    close_col = 'close' if 'close' in data.columns else 'Close'
    
    prices = data[close_col].values[-window:]
    X = np.arange(window).reshape(-1, 1)
    Y = prices
    model = LinearRegression()
    model.fit(X, Y)
    next_price = model.predict(np.array([[window]]))[0]
    
    return {"symbol": symbol, "predicted_next_close": next_price}