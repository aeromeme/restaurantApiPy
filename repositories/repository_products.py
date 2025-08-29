from typing import List, Optional
from database import SessionLocal
from unit_of_work import UnitOfWork
from models.models import Products
from sqlalchemy.orm import joinedload,sessionmaker


def get_products() -> List[Products]:
    with SessionLocal() as session:
        products = session.query(Products).options(joinedload(Products.Categories_)).all()
        return products

def get_product_by_id(product_id: int) -> Optional[Products]:
  with SessionLocal() as session:
        return (
            session.query(Products)
            .options(joinedload(Products.Categories_))
            .filter(Products.ProductID == product_id)
            .first()
        )
def get_product_by_id_uow(product_id: int) -> Optional[Products]:
    with UnitOfWork() as uow:
        return (
            uow.session.query(Products)
            .filter(Products.ProductID == product_id)
            .first()
        )


def save_product(product: Products) -> int:
    with UnitOfWork() as uow:
        uow.session.add(product)
        uow.session.flush()  # To get the new ProductID
        return product.ProductID

def update_product(product_id: int, updated_product: Products) -> bool:
    with UnitOfWork() as uow:
        product = uow.session.query(Products).filter(Products.ProductID == product_id).first()
        if not product:
            return False
        product.ProductName = updated_product.ProductName
        product.Price = updated_product.Price
        product.StockQuantity = updated_product.StockQuantity
        product.CategoryID = updated_product.CategoryID
        return True

def delete_product(product_id: int) -> bool:
    with UnitOfWork() as uow:
        product = uow.session.query(Products).filter(Products.ProductID == product_id).first()
        if not product:
            return False
        uow.session.delete(product)
        return True
