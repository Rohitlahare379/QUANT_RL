import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost/aegis_db")
    
    # Ingestion Config
    INGEST_START_DATE: str = os.getenv("INGEST_START_DATE", "2017-01-01T00:00:00Z")
    INGEST_SYMBOLS: str = os.getenv("INGEST_SYMBOLS", "BTCUSDT,ETHUSDT")
    INGEST_TIMEFRAMES: str = os.getenv("INGEST_TIMEFRAMES", "1h")
    INGEST_BATCH_SIZE: int = int(os.getenv("INGEST_BATCH_SIZE", "1000"))
    
settings = Settings()
