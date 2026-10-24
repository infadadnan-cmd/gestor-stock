from gestor_de_stock.domain.product import Product
from gestor_de_stock.repositories.product_repository import ProductRepository


class CreateProduct:
    def __init__(self, productRepository: ProductRepository):
        self.productRepository = productRepository

    def execute(
        self, name: str, price: float, quantity: int, category_id: int
    ) -> Product:
        product = Product(
            id=None, name=name, price=price, quantity=quantity, category_id=category_id
        )
        self.productRepository.save(product)
        return product
