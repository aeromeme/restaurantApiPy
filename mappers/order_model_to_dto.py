from dto.order_dto import OrderDTO, OrderDetailDTO

def order_model_to_dto(order) -> OrderDTO:
    details = [OrderDetailDTO(
        order_detail_id=od.OrderDetailID,
        product_id=od.ProductID,
        quantity=od.Quantity,
        price=float(getattr(od, 'Price', getattr(od, 'UnitPrice', 0)))
    ) for od in getattr(order, 'OrderDetails', [])]
    return OrderDTO(
        order_id=order.OrderID,
        customer_name=order.CustomerName,
        order_date=order.OrderDate,
        order_details=details,
        total_amount=sum(d.quantity * d.price for d in details)
    )
