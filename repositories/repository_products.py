
from typing import List, Optional
from models.models import Products
from sqlalchemy.orm import joinedload


def get_products(session) -> List[Products]:
    return session.query(Products).options(joinedload(Products.Categories_)).all()

def get_product_by_id(session, product_id: int) -> Optional[Products]:
    return (
        session.query(Products)
        .options(joinedload(Products.Categories_))
        .filter(Products.ProductID == product_id)
        .first()
    )
def get_product_by_id_uow(session, product_id: int) -> Optional[Products]:
    return (
        session.query(Products)
        .filter(Products.ProductID == product_id)
        .first()
    )


def save_product(session, product: Products) -> int:
    session.add(product)
    session.flush()  # To get the new ProductID
    return product.ProductID

def update_product(session, product_id: int, updated_product: Products) -> bool:
    product = session.query(Products).filter(Products.ProductID == product_id).first()
    if not product:
        return False
    product.ProductName = updated_product.ProductName
    product.Price = updated_product.Price
    product.StockQuantity = updated_product.StockQuantity
    product.CategoryID = updated_product.CategoryID
    return True

def delete_product(session, product_id: int) -> bool:
    product = session.query(Products).filter(Products.ProductID == product_id).first()
    if not product:
        return False
    session.delete(product)
    return True
