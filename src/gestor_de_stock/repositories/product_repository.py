from abc import ABC, abstractmethod

from gestor_de_stock.domain.product import Product
from gestor_de_stock.domain.product_with_category import ProductWithCategory


class ProductRepository(ABC):
    @abstractmethod
    def save(self, product: Product) -> None:
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Product | None:
        pass

    @abstractmethod
    def get_all(self) -> list[ProductWithCategory]:
        pass

    @abstractmethod
    def delete(self, product_id: int) -> None:
        pass

    @abstractmethod
    def update(self, product: Product) -> Product | None:
        pass
