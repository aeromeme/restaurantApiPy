from fastapi import APIRouter, HTTPException
from typing import List
from dto.order_dto import OrderDTO
from services.order_service import (
    get_orders_service,
    get_order_by_id_service,
    save_order_service,
    update_order_service,
    delete_order_service
)
from unit_of_work import UnitOfWork

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("/", response_model=List[OrderDTO])
def get_orders():
    with UnitOfWork() as uow:
        return get_orders_service(uow)

@router.get("/{order_id}", response_model=OrderDTO)
def get_order_by_id(order_id: int):
    with UnitOfWork() as uow:
        order = get_order_by_id_service(order_id, uow)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order

@router.post("/", response_model=int)
def create_order(order_dto: OrderDTO):
    with UnitOfWork() as uow:
        result, value = save_order_service(order_dto, uow)
        if not result:
            raise HTTPException(status_code=400, detail=value or "Order creation failed")
        return value

@router.put("/{order_id}", response_model=bool)
def update_order(order_id: int, order_dto: OrderDTO):
    with UnitOfWork() as uow:
        result, message = update_order_service(order_id, order_dto, uow)
        if not result:
            raise HTTPException(status_code=404, detail=message or "Order not found or update failed")
        return result

@router.delete("/{order_id}", response_model=bool)
def delete_order(order_id: int):
    with UnitOfWork() as uow:
        result, message = delete_order_service(order_id, uow)
        if not result:
            raise HTTPException(status_code=404, detail=message or "Order not found or delete failed")
        return result
