from gestor_de_stock.domain.product_with_category import ProductWithCategory
from gestor_de_stock.repositories.product_repository import ProductRepository


class GetProducts:
    def __init__(self, productRepository: ProductRepository):
        self.productRepository = productRepository

    def execute(self) -> list[ProductWithCategory]:
        return self.productRepository.get_all()
