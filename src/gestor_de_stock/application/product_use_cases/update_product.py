from gestor_de_stock.domain.product import Product
from gestor_de_stock.repositories.product_repository import ProductRepository


class UpdateProduct:
    def __init__(self, productRepository: ProductRepository):
        self.productRepository = productRepository

    def execute(self, product: Product) -> Product | None:
        return self.productRepository.update(product)
