# domain/services/product_domain_service.py
from domain.entities.product import Product

class ProductDomainService:
    @staticmethod
    def can_be_sold(product: Product) -> bool:
        # Example business rule: product must be in stock and price > 0
        return product.is_in_stock() and product.price > 0

    @staticmethod
    def discount_if_old(product: Product, is_old: bool):
        if is_old:
            product.apply_discount(10)
