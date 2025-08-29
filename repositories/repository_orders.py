from unit_of_work import UnitOfWork
from typing import List, Optional
from models.models import Orders
from sqlalchemy.orm import joinedload

def get_orders(session) -> List[Orders]:
    return session.query(Orders).options(joinedload(Orders.OrderDetails)).all()

def get_order_by_id(session, order_id: int) -> Optional[Orders]:
    return (
        session.query(Orders)
        .options(joinedload(Orders.OrderDetails))
        .filter(Orders.OrderID == order_id)
        .first()
    )

def get_order_by_id_uow(session, order_id: int) -> Optional[Orders]:
    return (
        session.query(Orders)
        .options(joinedload(Orders.OrderDetails))
        .filter(Orders.OrderID == order_id)
        .first()
    )

def save_order(session, order: Orders) -> int:
    session.add(order)
    session.flush()
    return order.OrderID


def delete_order(session, order: Orders) -> bool:
    if not order:
        return False
    session.delete(order)
    return True
