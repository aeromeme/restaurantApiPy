from repositories.repository_orders import save_order, delete_order
from models.models import Orders, OrderDetails
from typing import List, Optional
from repositories.repository_orders import get_orders, get_order_by_id,get_order_by_id_uow
from dto.order_dto import OrderDTO, OrderDetailDTO
from models.models import Orders
from mappers.product_model_to_dto import product_model_to_dto  # If you need product mapping for details
from sqlalchemy.orm import Session
from database import SessionLocal
from unit_of_work import UnitOfWork
from mappers.order_model_to_dto import order_model_to_dto
from mappers.order_mapper import dto_to_domain, domain_to_orm,orm_to_domain,order_detail_dto_to_domain

def get_orders_service(uow: UnitOfWork) -> List[OrderDTO]:
    orders = get_orders(uow.session)
    return [order_model_to_dto(o) for o in orders]

def get_order_by_id_service(order_id: int, uow: UnitOfWork) -> Optional[OrderDTO]:
    order = get_order_by_id(uow.session, order_id)
    if order:
        return order_model_to_dto(order)
    return None



def save_order_service(order_dto: OrderDTO, uow: UnitOfWork) -> int:
    domain_order = dto_to_domain(order_dto)
    # --- Apply domain rules/validation here ---
    # Example: if domain_order.is_empty(): return False, "Order must have at least one detail"
    # You can add more business logic as needed
    if hasattr(domain_order, 'is_empty') and domain_order.is_empty():
        return False, "Order must have at least one detail"
    order = domain_to_orm(domain_order)
    order_id = save_order(uow.session, order)
    return True, order_id

def update_order_service(order_id: int, order_dto: OrderDTO, uow: UnitOfWork) -> bool:
    from services.order_sync import sync_order_domain_to_orm
    orm_order = get_order_by_id_uow(uow.session, order_id)
    if not orm_order:
        return False, "Order not found"

    # Map ORM to domain
    domain_order = orm_to_domain(orm_order)

    # --- Apply domain rules/validation here ---
    # Example: if updated_domain_order.is_empty(): return False, "Order has no details"
    # You can add more business logic as needed

    updated_domain_order = orm_to_domain(orm_order)  # start from current state
    # Apply changes from DTO to domain entity (simulate update)
    updated_domain_order.customer_name = order_dto.customer_name
    updated_domain_order.order_date = order_dto.order_date
    from domain.entities.order import OrderDetail
    updated_domain_order.order_details = [
        order_detail_dto_to_domain(detail) for detail in order_dto.order_details
    ] if order_dto.order_details else []

    # --- Apply domain rules/validation here ---
    # Example: if updated_domain_order.is_empty(): return False, "Order has no details"
    # You can add more business logic as needed

    # Sync changes from updated_domain_order to orm_order using helper
    sync_order_domain_to_orm(updated_domain_order, orm_order, uow.session)
    return True, ""

def delete_order_service(order_id: int, uow: UnitOfWork) -> bool:
    orm_order = get_order_by_id_uow(uow.session, order_id)
    if not orm_order:
        return False, "Order not found"
    domain_order = orm_to_domain(orm_order)
    # --- Apply domain rules/validation here ---
    # Example: if domain_order.is_empty(): return False, "Cannot delete empty order"
    # You can add more business logic as needed
    deleted = delete_order(uow.session, orm_order)
    if not deleted:
        return False, "Delete failed"
    return True, ""

