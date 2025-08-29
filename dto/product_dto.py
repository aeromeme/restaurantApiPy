from pydantic import BaseModel
from typing import Optional, List
import decimal
from dto.category_dto import CategoryDTO


class ProductBaseDTO(BaseModel):
    product_name: str
    price: decimal.Decimal
    stock_quantity: int
    category_id: Optional[int] = None

class CreateProductDTO(ProductBaseDTO):
    pass

class UpdateProductDTO(ProductBaseDTO):
    product_id: int
    
class ProductDTO(ProductBaseDTO):
    product_id: int
    category: Optional[CategoryDTO] = None
