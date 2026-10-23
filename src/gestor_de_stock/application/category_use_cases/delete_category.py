from gestor_de_stock.repositories.category_repository import CategoryRepository


class DeleteCategory:
    def __init__(self, categoryRepository: CategoryRepository):
        self.categoryRepository = categoryRepository

    def execute(self, category_id: int) -> None:
        category = self.categoryRepository.find_by_id(category_id)
        if category is not None:
            self.categoryRepository.delete(category_id)
