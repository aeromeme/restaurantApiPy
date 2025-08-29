from pydantic import BaseModel, Field
from typing import List, Optional
import datetime

class OrderDetailDTO(BaseModel):
    order_detail_id: int
    product_id: int
    quantity: int = Field(..., ge=1)
    price: float = Field(..., ge=0)

class OrderDTO(BaseModel):
    order_id: int
    customer_name: str = Field(..., min_length=1, max_length=100)
    order_date: datetime.date
    order_details: List[OrderDetailDTO] = []
    total_amount: Optional[float] = None
