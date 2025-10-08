from fastapi import FastAPI
from typing import Optional

from src.modules.stocks import router as stocks_router
from src.modules.crypto import router as crypto_router
from src.modules.predictor import router as predictor_router
from src.modules.cache_handler import setup_cache

app = FastAPI(title="Stock and Crypto Predictor API")

setup_cache(app)

app.include_router(stocks_router)
app.include_router(crypto_router)
app.include_router(predictor_router)

@app.get("/")
def root():
    return {"message": "Welcome to Stock and Crypto Predictor API"}