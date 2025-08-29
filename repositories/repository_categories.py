from typing import List
from dto.category_dto import CategoryDTO
from unit_of_work import UnitOfWork
from models.models import Categories

def get_categories() -> List[CategoryDTO]:
    with UnitOfWork() as uow:
        categories = uow.session.query(Categories).all()
        return [CategoryDTO(
            category_id=c.CategoryID,
            category_name=c.CategoryName,
            description=c.Description   
        ) for c in categories]


def get_category_by_id(category_id: int) -> CategoryDTO | None:
    with UnitOfWork() as uow:
        c = uow.session.query(Categories).filter(Categories.CategoryID == category_id).first()
        if c:
            return CategoryDTO(
                category_id=c.CategoryID,
                category_name=c.CategoryName,
                description=c.Description
            )
        return None
