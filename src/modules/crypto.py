from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from src.data_loader import fetch_crypto_data

router = APIRouter(
    prefix="/crypto",
    tags=["crypto"],
)

@router.get("/")
@cache(expire=300)  # Cache for 5 minutes
def get_crypto(symbol: str = "BTC/USDT", timeframe: str = "1d", limit: int = 5):
    """
    Fetch crypto data from Binance via ccxt.
    Example: /crypto?symbol=BTC/USDT&timeframe=1d&limit=5
    """
    data = fetch_crypto_data(symbol, timeframe, limit)
    return data.to_dict(orient="records")