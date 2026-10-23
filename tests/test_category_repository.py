from gestor_de_stock.domain.category import Category


def test_save_category(category_repository, category, connection):
    row = connection.execute(
        "SELECT id, name FROM categories WHERE id = ?", (category.id,)
    ).fetchone()
    assert row is None
    category_repository.save(category)
    assert category.id is not None


def test_find_by_id(category_repository, category, connection):
    row = connection.execute(
        "SELECT id, name FROM categories WHERE id = ?", (category.id,)
    ).fetchone()
    assert row is None
    category_repository.save(category)
    retrieved_category = category_repository.find_by_id(category.id)
    assert retrieved_category is not None
    assert retrieved_category.id == category.id
    assert retrieved_category.name == category.name


def test_find_all(category_repository):
    category1 = Category(id=None, name="Test Category 1")
    category2 = Category(id=None, name="Test Category 2")
    category_repository.save(category1)
    category_repository.save(category2)
    retrieved_categories = category_repository.find_all()
    assert len(retrieved_categories) == 2
    assert retrieved_categories[0].name == "Test Category 1"
    assert retrieved_categories[1].name == "Test Category 2"
