def test_home_category(client_category):
    response = client_category.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "API running"}


def test_create_category(client_category):
    response = client_category.post("/categories", json={"name": "Test Category"})

    assert response.status_code == 201
    assert response.json() == {"id": 1, "name": "Test Category"}


def test_get_categories(client_category):
    client_category.post("/categories", json={"name": "Test Category 1"})
    client_category.post("/categories", json={"name": "Test Category 2"})

    response = client_category.get("/categories")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["name"] == "Test Category 1"
    assert data[1]["name"] == "Test Category 2"


def test_get_category(client_category):
    client_category.post("/categories", json={"name": "Test Category"})

    response = client_category.get("/categories/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Test Category"


def test_get_category_not_found(client_category):
    response = client_category.get("/categories/9999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Category not found"}


def test_update_category(client_category):
    client_category.post("/categories", json={"name": "Test Category"})

    response = client_category.put("/categories/1", json={"name": "Updated Category"})

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Updated Category"


def test_update_category_not_found(client_category):
    response = client_category.put(
        "/categories/9999", json={"name": "Updated Category"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Category not found"}


def test_delete_category(client_category, create_category):
    category = create_category("Test category")

    response = client_category.delete(f"/categories/{category.id}")
    assert response.status_code == 204

    check_response = client_category.get(f"/categories/{category.id}")
    assert check_response.status_code == 404
