from gestor_de_stock.application.category_use_cases.create_category import (
    CreateCategory,
)
from gestor_de_stock.application.category_use_cases.delete_category import (
    DeleteCategory,
)
from gestor_de_stock.application.category_use_cases.get_categories import GetCategories
from gestor_de_stock.application.category_use_cases.get_category import GetCategory
from gestor_de_stock.application.category_use_cases.update_category import (
    UpdateCategory,
)
from gestor_de_stock.domain.category import Category
from tests.fakes.fake_category_repository import FakeCategoryRepository


def test_create_category():
    category_repository = FakeCategoryRepository()

    use_case = CreateCategory(category_repository)

    category = use_case.execute(name="Test Category")

    assert category.id == 1
    assert category.name == "Test Category"
    assert category_repository.categories[0] == category


def test_get_all_categories():
    category_repository = FakeCategoryRepository()

    category1 = Category(id=1, name="Test Category")
    category_repository.save(category1)
    category2 = Category(id=2, name="Test Category 2")
    category_repository.save(category2)

    use_case = GetCategories(category_repository)

    categories = use_case.execute()

    assert len(categories) == 2
    assert categories[0].name == "Test Category"
    assert categories[1].name == "Test Category 2"


def test_get_category(category):
    category_repository = FakeCategoryRepository()
    category_repository.save(category)

    category_repository.requested_id = category.id

    use_case = GetCategory(category_repository)

    category = use_case.execute(1)

    assert category.id == 1
    assert category.name == "Test Category"
    assert category_repository.requested_id == 1


def test_delete_category(category):
    category_repository = FakeCategoryRepository()

    category_repository.save(category)

    use_case = DeleteCategory(category_repository)

    use_case.execute(1)
    assert category not in category_repository.categories


def test_update_category(category):
    category_repository = FakeCategoryRepository()

    category_repository.save(category)

    use_case = UpdateCategory(category_repository)

    updated_category = Category(id=1, name="Updated Test Category")
    result = use_case.execute(updated_category)

    assert result is not None
    assert result.name == "Updated Test Category"
    assert category_repository.categories[0].name == "Updated Test Category"
