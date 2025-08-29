from fastapi import APIRouter, HTTPException
from typing import List
from dto.product_dto import ProductDTO
from services.product_service import get_products_service, get_product_by_id_service, save_product_service,update_product_service,delete_product_service

router = APIRouter(
    prefix="/products",
    tags=["products"]
)


@router.get("/", response_model=List[ProductDTO])
def read_products():
    return get_products_service()


@router.get("/{product_id}", response_model=ProductDTO)
def read_product_by_id(product_id: int):
    product = get_product_by_id_service(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=ProductDTO, status_code=201)
def create_product(product_dto: ProductDTO):
    new_id = save_product_service(product_dto)
    # Fetch the new product from DB and return as DTO
    new_product = get_product_by_id_service(new_id)
    if not new_product:
        raise HTTPException(status_code=500, detail="Product creation failed")
    return new_product

@router.put("/{product_id}", response_model=ProductDTO)
def update_product(product_id: int, product_dto: ProductDTO):
    updated = update_product_service(product_id, product_dto)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    # Fetch the updated product from DB and return as DTO
    fresh_product = get_product_by_id_service(product_id)
    if not fresh_product:
        raise HTTPException(status_code=500, detail="Product update failed")
    return fresh_product

@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int):
    deleted = delete_product_service(product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return None
