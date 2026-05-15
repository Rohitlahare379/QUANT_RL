from datetime import datetime, timezone
from typing import Optional, Dict

class RegimeManager:
    """
    Manages historical date ranges representing different market conditions.
    """
    REGIMES = {
        "full_history": {
            "name": "Full Market Cycle",
            "start": datetime(2017, 1, 1, tzinfo=timezone.utc), 
            "end": datetime(2025, 1, 1, tzinfo=timezone.utc)
        },
        "covid_2020": {
            "name": "COVID Crash",
            "start": datetime(2020, 2, 1, tzinfo=timezone.utc), 
            "end": datetime(2020, 5, 1, tzinfo=timezone.utc)
        },
        "ftx_collapse": {
            "name": "FTX Collapse",
            "start": datetime(2022, 11, 1, tzinfo=timezone.utc), 
            "end": datetime(2022, 12, 1, tzinfo=timezone.utc)
        },
        "2018_bear": {
            "name": "2018 Bear Market",
            "start": datetime(2018, 1, 1, tzinfo=timezone.utc), 
            "end": datetime(2018, 12, 31, tzinfo=timezone.utc)
        },
        "bull_market": {
            "name": "2020-2021 Bull Market",
            "start": datetime(2020, 10, 1, tzinfo=timezone.utc), 
            "end": datetime(2021, 11, 1, tzinfo=timezone.utc)
        },
        "sideways": {
            "name": "Sideways Market",
            "start": datetime(2023, 1, 1, tzinfo=timezone.utc), 
            "end": datetime(2023, 9, 1, tzinfo=timezone.utc)
        }
    }
    
    @classmethod
    def get_regime(cls, regime_id: str) -> Optional[Dict[str, datetime]]:
        return cls.REGIMES.get(regime_id)
