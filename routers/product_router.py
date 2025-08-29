from fastapi import APIRouter, HTTPException
from typing import List
from dto.product_dto import ProductDTO
from services.product_service import get_products_service, get_product_by_id_service, save_product_service,update_product_service,delete_product_service
from unit_of_work import UnitOfWork

router = APIRouter(
    prefix="/products",
    tags=["products"]
)


@router.get("/", response_model=List[ProductDTO])
def read_products():
    with UnitOfWork() as uow:
        return get_products_service(uow)



@router.get("/{product_id}", response_model=ProductDTO)
def read_product_by_id(product_id: int):
    with UnitOfWork() as uow:
        product = get_product_by_id_service(product_id, uow)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product



from dto.product_dto import CreateProductDTO, UpdateProductDTO

@router.post("/", response_model=ProductDTO, status_code=201)
def create_product(product_dto: CreateProductDTO):
    with UnitOfWork() as uow:
        success, result = save_product_service(product_dto, uow)
        if not success:
            raise HTTPException(status_code=400, detail=result)
        new_product = get_product_by_id_service(result, uow)
        if not new_product:
            raise HTTPException(status_code=500, detail="Product creation failed")
        return new_product


@router.put("/{product_id}", response_model=ProductDTO)
def update_product(product_id: int, product_dto: UpdateProductDTO):
    with UnitOfWork() as uow:
        success, message = update_product_service(product_id, product_dto, uow)
        if not success:
            raise HTTPException(status_code=404, detail=message)
        fresh_product = get_product_by_id_service(product_id, uow)
        if not fresh_product:
            raise HTTPException(status_code=500, detail="Product update failed")
        return fresh_product


@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int):
    with UnitOfWork() as uow:
        success, message = delete_product_service(product_id, uow)
        if not success:
            raise HTTPException(status_code=404, detail=message)
        return None
