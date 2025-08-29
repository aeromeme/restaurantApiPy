

from typing import List, Optional
from repositories.repository_products import get_product_by_id_uow, get_products, get_product_by_id, save_product, update_product, delete_product
from models.models import Products
from dto.product_dto import CreateProductDTO, ProductDTO, UpdateProductDTO
from mappers.product_model_to_dto import product_model_to_dto
from mappers.product_mapper import create_dto_to_domain, dto_to_domain, domain_to_orm
from domain.services.product_domain_service import ProductDomainService
from unit_of_work import UnitOfWork

def get_products_service(uow: UnitOfWork) -> List[ProductDTO]:
    products = get_products(uow.session)
    return [product_model_to_dto(p) for p in products]

def get_product_by_id_service(product_id: int, uow: UnitOfWork) -> Optional[ProductDTO]:
    product = get_product_by_id(uow.session, product_id)
    if product:
        return product_model_to_dto(product)
    return None

def save_product_service(product_dto: CreateProductDTO, uow: UnitOfWork):
    domain_product = create_dto_to_domain(product_dto)
    if not ProductDomainService.can_be_sold(domain_product):
        return False, "Product cannot be saved: not sellable (out of stock or price invalid)"
    orm_product = domain_to_orm(domain_product)
    new_id = save_product(uow.session, orm_product)
    return True, new_id

def update_product_service(product_id: int, product_dto: UpdateProductDTO, uow: UnitOfWork):
    product = get_product_by_id_uow(uow.session, product_id)
    if not product:
        return False, "Product not found"
    # Map ORM to domain
    domain_product = dto_to_domain(product_model_to_dto(product))
    # Apply changes from DTO to domain entity
    domain_product.name = product_dto.product_name
    domain_product.price = float(product_dto.price)
    domain_product.stock_quantity = product_dto.stock_quantity
    domain_product.category_id = product_dto.category_id
    # Domain validation
    if not ProductDomainService.can_be_sold(domain_product):
        return False, "Product cannot be updated: not sellable (out of stock or price invalid)"
    # Sync changes to ORM
    product.ProductName = domain_product.name
    product.Price = domain_product.price
    product.StockQuantity = domain_product.stock_quantity
    product.CategoryID = domain_product.category_id
    updated = update_product(uow.session, product_id, product)
    if not updated:
        return False, "Update failed"
    return True, ""

def delete_product_service(product_id: int, uow: UnitOfWork):
    deleted = delete_product(uow.session, product_id)
    if not deleted:
        return False, "Product not found"
    return True, ""
