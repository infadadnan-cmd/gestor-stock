from gestor_de_stock.application.product_use_cases.create_product import CreateProduct
from gestor_de_stock.application.product_use_cases.delete_product import DeleteProduct
from gestor_de_stock.application.product_use_cases.get_product import GetProduct
from gestor_de_stock.application.product_use_cases.get_products import GetProducts
from gestor_de_stock.application.product_use_cases.update_product import UpdateProduct
from gestor_de_stock.domain.product import Product
from tests.fakes.fake_product_repository import FakeProductRepository


def test_create_product():
    product_repository = FakeProductRepository()

    use_case = CreateProduct(product_repository)

    product = use_case.execute(
        name="Test Product", price=50, quantity=10, category_id=1
    )

    assert product.name == "Test Product"
    assert product.price == 50
    assert product_repository.products[0] == product
    assert product.quantity == 10
    assert product.category_id == 1


def test_get_all_products():
    product_repository = FakeProductRepository()

    product1 = Product(id=1, name="Test Product", price=50, quantity=10, category_id=1)
    product_repository.save(product1)

    use_case = GetProducts(product_repository)

    products = use_case.execute()

    assert len(products) == 1
    assert products[0].id == 1
    assert products[0].name == "Test Product"
    assert products[0].price == 50
    assert products[0].quantity == 10
    assert products[0].category_id == 1


def test_get_product(product):
    product_repository = FakeProductRepository()
    product_repository.save(product)
    product_repository.requested_id = product.id

    use_case = GetProduct(product_repository)

    product = use_case.execute(1)

    assert product.id == 1
    assert product_repository.requested_id == 1


def test_delete_product(product):
    product_repository = FakeProductRepository()

    product_repository.save(product)

    use_case = DeleteProduct(product_repository)

    use_case.execute(1)
    assert product not in product_repository.products


def test_update_product(existing_product):
    product_repository = FakeProductRepository()
    product_repository.save(existing_product)
    print(product_repository.products)
    print(existing_product.id)
    use_case = UpdateProduct(product_repository)

    updated_product = Product(
        id=1,
        name="Updated product",
        price=20,
        quantity=100,
        category_id=1,
    )
    result = use_case.execute(updated_product)

    assert result.name == "Updated product"
    assert result.price == 20
    assert result.quantity == 100
    assert result.category_id == 1
