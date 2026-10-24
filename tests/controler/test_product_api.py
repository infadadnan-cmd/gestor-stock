def test_home(client_product):
    response = client_product.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "API running"}


def test_create_product(client_product):
    response = client_product.post(
        "/products",
        json={"name": "Test Product", "price": 50, "quantity": 10, "category_id": 1},
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test Product"
    assert data["price"] == 50
    assert data["quantity"] == 10
    assert data["category_id"] == 1
    assert "id" in data


def test_get_products(client_product):
    client_product.post(
        "/products",
        json={"name": "mouse", "price": 20, "quantity": 5, "category_id": 1},
    )
    client_product.post(
        "/products",
        json={"name": "keyboard", "price": 30, "quantity": 6, "category_id": 1},
    )
    response = client_product.get("/products")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["name"] == "mouse"
    assert data[1]["name"] == "keyboard"


def test_get_product(client_product, create_product, api_product_repository):
    product = create_product("Mouse", 20, 10, 1)
    api_product_repository.save(product)

    response = client_product.get(f"/products/{product.id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == product.id
    assert data["name"] == "Mouse"
    assert data["price"] == 20
    assert data["quantity"] == 10
    assert data["category_id"] == 1


def test_get_product_not_found(client_product):
    response = client_product.get("/products/9999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


def test_update_product(client_product, product, api_product_repository):
    api_product_repository.save(product)

    response = client_product.put(
        f"/products/{product.id}",
        json={"name": "Gaming Mouse", "price": 35, "quantity": 15, "category_id": 1},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == product.id
    assert data["name"] != product.name
    assert data["price"] != product.price
    assert data["quantity"] != product.quantity
    assert data["category_id"] == product.category_id


def test_update_product_not_found(client_product):
    response = client_product.put(
        "/products/9999",
        json={"name": "Gaming Mouse", "price": 35, "quantity": 15, "category_id": 1},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


def test_delete_product(client_product, create_product):
    product = create_product("Mouse", 20, 10, 1)

    response = client_product.delete(f"/products/{product.id}")

    assert response.status_code == 204

    # Comprobar que realmente se eliminó
    check_response = client_product.get(f"/products/{product.id}")

    assert check_response.status_code == 404


def test_delete_product_not_found(client_product):
    response = client_product.delete("/products/9999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


def test_create_product_invalid_price(client_product):
    response = client_product.post(
        "/products", json={"name": "Mouse", "price": -10, "quantity": 10}
    )

    assert response.status_code == 422


def test_create_product_empty_name(client_product):
    response = client_product.post(
        "/products", json={"name": "", "price": 20, "quantity": 10}
    )

    assert response.status_code == 422


def test_create_product_invalid_price_type(client_product):
    response = client_product.post(
        "/products", json={"name": "Mouse", "price": "hola", "quantity": 10}
    )
    assert response.status_code == 422


def test_get_products_with_category(client_product, create_category):
    category = create_category("Electronics")

    client_product.post(
        "/products",
        json={
            "name": "Laptop",
            "price": 1000,
            "quantity": 5,
            "category_id": category.id,
        },
    )

    response = client_product.get("/products")

    assert response.status_code == 200

    data = response.json()

    assert data[0]["name"] == "Laptop"
    assert data[0]["category_id"] == category.id
    assert data[0]["category_name"] == "Electronics"
