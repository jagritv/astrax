from src.data_loader import fetch_crypto_data, fetch_stock_data

# Fetch stock
stocks = fetch_stock_data("AAPL", "2023-01-01", "2023-06-30")
print("Stock Data:\n", stocks.head())

# Fetch crypto
crypto = fetch_crypto_data("BTC/USDT", "1d", 5)
print("Crypto Data:\n", crypto.head())