import pytest
from fastapi.testclient import TestClient

# Assuming `app` is our FastAPI application object
client = TestClient(app)

@pytest.fixture
def sample_supplier():
    return {
        "supplier_id": "sup_test",
        "name": "Test Supplier",
        "location": "Test City",
        "contact": "123456789"
    }

# Happy Path: Create a New Supplier
def test_create_supplier(sample_supplier):
    response = client.post("/suppliers/", json=sample_supplier)
    assert response.status_code == 200
    assert response.json()["supplier_id"] == sample_supplier["supplier_id"]

# Unhappy Path: Create Supplier with Missing supplier_id
def test_create_supplier_missing_id():
    supplier = {"name": "Test Supplier", "location": "Test City", "contact": "123456789"}
    response = client.post("/suppliers/", json=supplier)
    assert response.status_code == 400

# Happy Path: Retrieve Existing Supplier
def test_get_supplier(sample_supplier):
    client.post("/suppliers/", json=sample_supplier)
    response = client.get(f"/suppliers/{sample_supplier['supplier_id']}")
    assert response.status_code == 200
    assert response.json()["name"] == sample_supplier["name"]

# Unhappy Path: Retrieve Non-Existing Supplier
def test_get_non_existing_supplier():
    response = client.get("/suppliers/non_existing")
    assert response.status_code == 404

# Happy Path: Update Existing Supplier
def test_update_supplier(sample_supplier):
    client.post("/suppliers/", json=sample_supplier)
    updated_data = {"name": "Updated Supplier", "location": "Updated City", "contact": "987654321"}
    response = client.put(f"/suppliers/{sample_supplier['supplier_id']}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == updated_data["name"]

# Unhappy Path: Update Non-Existing Supplier
def test_update_non_existing_supplier():
    updated_data = {"name": "Non-Existent", "location": "Nowhere", "contact": "000000000"}
    response = client.put("/suppliers/non_existing", json=updated_data)
    assert response.status_code == 404

# Happy Path: Delete Existing Supplier
def test_delete_supplier(sample_supplier):
    client.post("/suppliers/", json=sample_supplier)
    response = client.delete(f"/suppliers/{sample_supplier['supplier_id']}")
    assert response.status_code == 200
    response = client.get(f"/suppliers/{sample_supplier['supplier_id']}")
    assert response.status_code == 404

# Unhappy Path: Delete Non-Existing Supplier
def test_delete_non_existing_supplier():
    response = client.delete("/suppliers/non_existing")
    assert response.status_code == 404
