from gestor_de_stock.domain.product import Product
from gestor_de_stock.repositories.product_repository import ProductRepository


class GetProduct:
    def __init__(
        self,
        productRepository: ProductRepository,
    ):
        self.productRepository = productRepository

    def execute(self, product_id: int) -> Product:
        return self.productRepository.get_by_id(product_id)
