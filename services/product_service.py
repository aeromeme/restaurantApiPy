
from typing import List, Optional
from repositories.repository_products import get_product_by_id_uow, get_products, get_product_by_id, save_product, update_product, delete_product
from models.models import Products
from dto.product_dto import CreateProductDTO, ProductDTO, UpdateProductDTO
from dto.category_dto import CategoryDTO
from mappers.product_model_to_dto import product_model_to_dto
from mappers.product_mapper import create_dto_to_domain, dto_to_domain, domain_to_orm
from domain.services.product_domain_service import ProductDomainService



def get_products_service() -> List[ProductDTO]:
    return [product_model_to_dto(p) for p in get_products()]

def get_product_by_id_service(product_id: int) -> Optional[ProductDTO]:
    product = get_product_by_id(product_id)
    if product:
        return product_model_to_dto(product)
    return None

def save_product_service(product_dto: CreateProductDTO) -> int:
    # 1. Map DTO to domain entity using mapper
    domain_product = create_dto_to_domain(product_dto)

    # 2. Apply domain logic (example: check if can be sold)
    if not ProductDomainService.can_be_sold(domain_product):
        raise ValueError("Product cannot be saved: not sellable (out of stock or price invalid)")

    # 3. Map domain entity to ORM model for persistence using mapper
    orm_product = domain_to_orm(domain_product)
    return save_product(orm_product)

def update_product_service(product_id: int, product_dto: UpdateProductDTO) -> bool:
    product = get_product_by_id_uow(product_id)
    if not product:
        return False
    product.ProductName = product_dto.product_name
    product.Price = product_dto.price
    product.StockQuantity = product_dto.stock_quantity
    product.CategoryID = product_dto.category_id
    return update_product(product_id, product)

def delete_product_service(product_id: int) -> bool:
    return delete_product(product_id)
