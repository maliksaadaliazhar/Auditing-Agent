from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class LineItem:

    description: str
    amount: float
    category: str = "Unknown"  # e.g., "Food", "Alcohol", "Tax"
    flagged: bool = False
    bbox: Optional[List[int]] = None

@dataclass
class Receipt:
    
    merchant_name: str
    date: str          # Format: YYYY-MM-DD
    time: str          # Format: HH:MM
    total_amount: float
    currency: str = "USD"
    items: List[LineItem] = field(default_factory=list)
    

    filename: str = ""
    flagged: bool = False
    flag_reason: List[str] = field(default_factory=list)

    @property
    def datetime_object(self) -> Optional[datetime]:

        try:
            return datetime.strptime(f"{self.date} {self.time}", "%Y-%m-%d %H:%M")
        except ValueError:
            return None
        
    @property
    def flagged_boxes(self) -> list[list[int]]:
        return [item.bbox for item in self.items if item.flagged and item.bbox]
    
    