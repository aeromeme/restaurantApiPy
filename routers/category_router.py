from fastapi import APIRouter
from typing import List
from dto.category_dto import CategoryDTO
from repositories.repository_categories import get_categories
from fastapi import HTTPException
from repositories.repository_categories import get_category_by_id

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

@router.get("/", response_model=List[CategoryDTO])
def read_categories():
    return get_categories()

@router.get("/{category_id}", response_model=CategoryDTO)
def read_category_by_id(category_id: int):
    category = get_category_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category
