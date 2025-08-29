from domain.entities.order import Order

class OrderDomainService:
    @staticmethod
    def can_be_processed(order: Order) -> bool:
        # Example business rule: order must have at least one detail
        return not order.is_empty()

    @staticmethod
    def total_amount(order: Order) -> float:
        return order.total_amount()
