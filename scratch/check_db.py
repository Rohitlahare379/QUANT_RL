from database import SessionLocal
from market_data.storage.models import MarketCandle

db = SessionLocal()
count = db.query(MarketCandle).count()
print(f"Total candles in database: {count}")

distinct_tfs = db.query(MarketCandle.timeframe).distinct().all()
print(f"Timeframes in database: {distinct_tfs}")

distinct_syms = db.query(MarketCandle.symbol).distinct().all()
print(f"Symbols in database: {distinct_syms}")

sample = db.query(MarketCandle).first()
if sample:
    print(f"Sample candle: {sample.symbol} {sample.timeframe} {sample.timestamp}")
else:
    print("No candles found.")
db.close()
