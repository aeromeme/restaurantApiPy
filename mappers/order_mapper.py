from domain.entities.order import Order as DomainOrder, OrderDetail as DomainOrderDetail
from dto.order_dto import OrderDTO, OrderDetailDTO
from models.models import Orders, OrderDetails

def dto_to_domain(order_dto: OrderDTO) -> DomainOrder:
    return DomainOrder(
        id=order_dto.order_id,
        customer_name=order_dto.customer_name,
        order_date=order_dto.order_date,
        order_details=[
            DomainOrderDetail(
                order_detail_id=detail.order_detail_id,
                product_id=detail.product_id,
                quantity=detail.quantity,
                price=detail.price
            ) for detail in order_dto.order_details
        ]
    )

def domain_to_orm(domain_order: DomainOrder) -> Orders:
    order = Orders(
        CustomerName=domain_order.customer_name,
        OrderDate=domain_order.order_date
    )
    for detail in domain_order.order_details:
        order_detail = OrderDetails(
            ProductID=detail.product_id,
            Quantity=detail.quantity,
            Price=detail.price
        )
        order.OrderDetails.append(order_detail)
    return order

def orm_to_domain(order: Orders) -> DomainOrder:
    return DomainOrder(
        id=order.OrderID,
        customer_name=order.CustomerName,
        order_date=order.OrderDate,
        order_details=[
            DomainOrderDetail(
                order_detail_id=od.OrderDetailID,
                product_id=od.ProductID,
                quantity=od.Quantity,
                price=float(getattr(od, 'Price', getattr(od, 'UnitPrice', 0)))
            ) for od in getattr(order, 'OrderDetails', [])
        ]
    )

def domain_to_dto(domain_order: DomainOrder) -> OrderDTO:
    details = [OrderDetailDTO(
        order_detail_id=od.order_detail_id,
        product_id=od.product_id,
        quantity=od.quantity,
        price=od.price
    ) for od in domain_order.order_details]
    return OrderDTO(
        order_id=domain_order.id,
        customer_name=domain_order.customer_name,
        order_date=domain_order.order_date,
        order_details=details,
        total_amount=domain_order.total_amount()
    )
def order_detail_dto_to_domain(dto: OrderDetailDTO) -> DomainOrderDetail:
    return DomainOrderDetail(
        order_detail_id=dto.order_detail_id,
        product_id=dto.product_id,
        quantity=dto.quantity,
        price=dto.price
    )
