from dataclasses import dataclass, field
from typing import List, Optional
import datetime

@dataclass
class OrderDetail:
    order_detail_id: int
    product_id: int
    quantity: int
    price: float

@dataclass
class Order:
    id: int
    customer_name: str
    order_date: datetime.date
    order_details: List[OrderDetail] = field(default_factory=list)

    def total_amount(self) -> float:
        return sum(od.quantity * od.price for od in self.order_details)

    def is_empty(self) -> bool:
        return len(self.order_details) == 0
