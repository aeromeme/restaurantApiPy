from dto.product_dto import ProductDTO
from dto.category_dto import CategoryDTO


def product_model_to_dto(product) -> ProductDTO:
    category = None
    if hasattr(product, 'Categories_') and product.Categories_:
        category = CategoryDTO(
            category_id=product.Categories_.CategoryID,
            category_name=product.Categories_.CategoryName,
            description=product.Categories_.Description
        )
    return ProductDTO(
        product_id=product.ProductID,
        product_name=product.ProductName,
        price=product.Price,
        stock_quantity=product.StockQuantity,
        category_id=product.CategoryID,
        category=category
    )
