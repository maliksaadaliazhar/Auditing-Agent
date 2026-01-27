from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class LineItem:
    """Represents a single row on the receipt."""
    description: str
    amount: float
    category: str = "Unknown"  # e.g., "Food", "Alcohol", "Tax"

@dataclass
class Receipt:
    """
    The Master Object. 
    This holds the 'Golden Data' after we clean up the OCR mess.
    """
    merchant_name: str
    date: str          # Format: YYYY-MM-DD
    time: str          # Format: HH:MM (Crucial for 'Structuring' fraud)
    total_amount: float
    currency: str = "USD"
    items: List[LineItem] = field(default_factory=list)
    
    # Metadata for the Auditor
    filename: str = ""
    flagged: bool = False
    flag_reason: List[str] = field(default_factory=list)

    @property
    def datetime_object(self) -> Optional[datetime]:
        """Helper to convert string strings to real Python Time objects for math."""
        try:
            return datetime.strptime(f"{self.date} {self.time}", "%Y-%m-%d %H:%M")
        except ValueError:
            return None