from gestor_de_stock.domain.category import Category
from gestor_de_stock.repositories.category_repository import CategoryRepository


class GetCategory:
    def __init__(self, categoryRepository: CategoryRepository):
        self.categoryRepository = categoryRepository

    def execute(self, category_id: int) -> Category | None:
        return self.categoryRepository.find_by_id(category_id)
