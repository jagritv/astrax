from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from src.data_loader import fetch_stock_data

# Create router
router = APIRouter(
    prefix="/stock",
    tags=["stocks"],
)

@router.get("/")
@cache(expire=300)  # Cache for 5 minutes
def get_stock(symbol: str, start: str, end: str):
    """
    Fetch stock data from Yahoo Finance.
    Example: /stock?symbol=AAPL&start=2023-01-01&end=2023-06-30
    """
    data = fetch_stock_data(symbol, start, end)
    return data.tail(10).to_dict(orient="records")