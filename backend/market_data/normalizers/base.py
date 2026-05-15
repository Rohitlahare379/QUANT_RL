from abc import ABC, abstractmethod
from typing import List, Any
from .schemas import NormalizedCandle

class BaseNormalizer(ABC):
    """
    Abstract base class for all market data normalizers.
    Forces child classes to implement a unified output format.
    """
    
    @abstractmethod
    def normalize(self, raw_data: Any, symbol: str, timeframe: str) -> List[NormalizedCandle]:
        """
        Convert raw exchange data into a list of NormalizedCandle objects.
        """
        pass
