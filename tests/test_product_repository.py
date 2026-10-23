from gestor_de_stock.domain.product import Product


def test_save_product_and_check_database(product_repository, connection, product):
    product_repository.save(product)
    row = connection.execute(
        "SELECT id, name, price, quantity, category_id FROM products WHERE id = ?",
        (product.id,),
    ).fetchone()
    assert product.id is not None
    assert row is not None
    assert row["name"] == product.name
    assert row["price"] == product.price
    assert row["quantity"] == product.quantity
    assert row["category_id"] == product.category_id


def test_get_by_id(product_repository, product):
    product_repository.save(product)
    retrieved_product = product_repository.get_by_id(product.id)
    assert retrieved_product is not None
    assert retrieved_product.id == product.id
    assert retrieved_product.name == product.name
    assert retrieved_product.price == product.price
    assert retrieved_product.quantity == product.quantity
    assert retrieved_product.category_id == product.category_id


def test_get_all(product_repository):
    product1 = Product(
        id=None, name="Test Product 1", price=50, quantity=10, category_id=1
    )
    product2 = Product(
        id=None, name="Test Product 2", price=100, quantity=5, category_id=1
    )
    product_repository.save(product1)
    product_repository.save(product2)
    products = product_repository.get_all()
    assert len(products) == 2
    assert products[0].name == "Test Product 1"
    assert products[1].name == "Test Product 2"


def test_delete_product(product_repository, product):
    product_repository.save(product)
    product_repository.delete(product.id)


def test_update_product(product_repository, product):
    product_repository.save(product)
    product.name = "Updated Product"
    product.price = 100
    product.quantity = 5
    product.category_id = 1
    updated_product = product_repository.update(product)
    assert updated_product is not None
    assert updated_product.name == "Updated Product"
    assert updated_product.price == 100
    assert updated_product.quantity == 5
    assert updated_product.category_id == 1


def test_get_by_id_nonexistent_product(product_repository):
    retrieved_product = product_repository.get_by_id(999)
    assert retrieved_product is None


def test_update_nonexistent_product(product_repository):
    non_existent_product = Product(
        id=999, name="Non-existent Product", price=100, quantity=5, category_id=1
    )
    updated_product = product_repository.update(non_existent_product)
    assert updated_product is None


def test_delete_nonexistent_product(product_repository):
    product_repository.delete(999)


def test_get_all_with_category(product_repository, create_category, create_product):
    category = create_category("Electronics")

    create_product(name="Laptop", price=1000, quantity=5, category_id=category.id)

    products = product_repository.get_all()

    assert len(products) == 1
    assert products[0].name == "Laptop"
    assert products[0].category_id == category.id


def test_get_all_with_category_left_join(
    product_repository, create_category, create_product
):
    category = create_category("Electronics")

    create_product(name="Laptop", price=1000, quantity=5, category_id=category.id)

    create_product(name="Keyboard", price=50, quantity=10, category_id=None)

    products = product_repository.get_all()

    assert len(products) == 2
    assert products[0].category_id == category.id
    assert products[1].category_id is None
