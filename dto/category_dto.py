from pydantic import BaseModel
from typing import Optional

class CategoryDTO(BaseModel):
    category_id: int
    category_name: str
    description: Optional[str] = None
