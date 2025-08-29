# domain/entities/product.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    id: int
    name: str
    price: float
    stock_quantity: int
    category_id: Optional[int] = None

    def is_in_stock(self) -> bool:
        return self.stock_quantity > 0

    def apply_discount(self, percent: float):
        self.price = self.price * (1 - percent / 100)
