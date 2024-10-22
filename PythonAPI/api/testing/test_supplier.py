import pytest
import json
from fastapi.testclient import TestClient
from fastapi import FastAPI, HTTPException

# Define a temporary FastAPI app for testing
app = FastAPI()

# Load data from JSON file (suppliers.json)
try:
    with open("data/suppliers.json", "r") as file:
        suppliers_data = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    suppliers_data = []

client = TestClient(app)

# Temporary routes for testing
@app.post("/suppliers/")
async def create_supplier(supplier: dict):
    if "supplier_id" not in supplier:
        raise HTTPException(status_code=400, detail="Supplier must have a 'supplier_id'")
    for existing_supplier in suppliers_data:
        if "supplier_id" in existing_supplier and existing_supplier["supplier_id"] == supplier["supplier_id"]:
            raise HTTPException(status_code=400, detail="Supplier already exists")
    suppliers_data.append(supplier)
    return supplier

@app.get("/suppliers/{supplier_id}")
async def get_supplier(supplier_id: str):
    for supplier in suppliers_data:
        if "supplier_id" in supplier and supplier["supplier_id"] == supplier_id:
            return supplier
    raise HTTPException(status_code=404, detail="Supplier not found")

@app.put("/suppliers/{supplier_id}")
async def update_supplier(supplier_id: str, updated_supplier: dict):
    for index, supplier in enumerate(suppliers_data):
        if "supplier_id" in supplier and supplier["supplier_id"] == supplier_id:
            suppliers_data[index].update(updated_supplier)
            return suppliers_data[index]
    raise HTTPException(status_code=404, detail="Supplier not found")

@app.delete("/suppliers/{supplier_id}")
async def delete_supplier(supplier_id: str):
    for index, supplier in enumerate(suppliers_data):
        if "supplier_id" in supplier and supplier["supplier_id"] == supplier_id:
            del suppliers_data[index]
            return {"detail": "Supplier deleted"}
    raise HTTPException(status_code=404, detail="Supplier not found")

@app.get("/suppliers/")
async def list_suppliers():
    return suppliers_data

@pytest.fixture
def sample_supplier():
    """
    Fixture to provide sample supplier data from the JSON file.
    Returns the first supplier in the JSON data.
    """
    return {
        "supplier_id": "sup1",
        "name": "Sample Supplier",
        "location": "City A",
        "contact": "1234567890"
    }

def test_create_supplier_integration(sample_supplier):
    """
    Integration Test: Create a Supplier (Happy Path)
    - Endpoint Tested: POST /suppliers/
    - This test checks if a new supplier can be successfully created.
    """
    # Step 1: Check if the supplier exists already (shouldn't)
    response = client.get(f"/suppliers/{sample_supplier['supplier_id']}")
    assert response.status_code == 404  # The supplier should not exist before creation
    
    # Step 2: Create the supplier using the API
    response = client.post("/suppliers/", json=sample_supplier)
    assert response.status_code == 200  # Successful creation returns HTTP 200
    assert response.json()["name"] == sample_supplier["name"]
    assert response.json()["location"] == sample_supplier["location"]
    
    # Step 3: Retrieve the newly created supplier to verify
    response = client.get(f"/suppliers/{sample_supplier['supplier_id']}")
    assert response.status_code == 200
    supplier_data = response.json()
    assert supplier_data["name"] == sample_supplier["name"]
    assert supplier_data["location"] == sample_supplier["location"]
    assert supplier_data["contact"] == sample_supplier["contact"]

def test_get_supplier_integration(sample_supplier):
    """
    Integration Test: Retrieve a Supplier (Happy Path)
    - Endpoint Tested: GET /suppliers/{supplier_id}
    - This test checks if an existing supplier can be successfully retrieved.
    """
    # Create the supplier first
    client.post("/suppliers/", json=sample_supplier)
    
    # Step 1: Retrieve the supplier
    response = client.get(f"/suppliers/{sample_supplier['supplier_id']}")
    assert response.status_code == 200
    supplier_data = response.json()
    assert supplier_data["name"] == sample_supplier["name"]
    assert supplier_data["location"] == sample_supplier["location"]
    assert supplier_data["contact"] == sample_supplier["contact"]

def test_update_supplier_integration(sample_supplier):
    """
    Integration Test: Update a Supplier (Happy Path)
    - Endpoint Tested: PUT /suppliers/{supplier_id}
    - This test checks if an existing supplier can be successfully updated.
    """
    # Create the supplier first
    client.post("/suppliers/", json=sample_supplier)
    
    # Step 1: Update the supplier details
    updated_data = {
        "name": sample_supplier["name"] + " Updated",
        "location": sample_supplier["location"] + " Updated",
        "contact": sample_supplier["contact"] + "1"
    }
    response = client.put(f"/suppliers/{sample_supplier['supplier_id']}", json=updated_data)
    assert response.status_code == 200  # Successful update returns HTTP 200
    
    # Step 2: Retrieve the updated supplier to verify
    response = client.get(f"/suppliers/{sample_supplier['supplier_id']}")
    assert response.status_code == 200
    supplier_data = response.json()
    assert supplier_data["name"] == updated_data["name"]
    assert supplier_data["location"] == updated_data["location"]
    assert supplier_data["contact"] == updated_data["contact"]

def test_delete_supplier_integration(sample_supplier):
    """
    Integration Test: Delete a Supplier (Happy Path)
    - Endpoint Tested: DELETE /suppliers/{supplier_id}
    - This test checks if an existing supplier can be successfully deleted.
    """
    # Create the supplier first
    client.post("/suppliers/", json=sample_supplier)
    
    # Step 1: Delete the supplier
    response = client.delete(f"/suppliers/{sample_supplier['supplier_id']}")
    assert response.status_code == 200  # Successful deletion returns HTTP 200
    
    # Step 2: Verify the supplier has been deleted
    response = client.get(f"/suppliers/{sample_supplier['supplier_id']}")
    assert response.status_code == 404  # Supplier should no longer exist

def test_list_suppliers_integration():
    """
    Integration Test: List All Suppliers (Happy Path)
    - Endpoint Tested: GET /suppliers/
    - This test checks if all suppliers can be successfully listed.
    """
    # Step 1: Create multiple suppliers
    supplier_1 = {"supplier_id": "sup1", "name": "Supplier One", "location": "City A", "contact": "1234567890"}
    supplier_2 = {"supplier_id": "sup2", "name": "Supplier Two", "location": "City B", "contact": "0987654321"}
    client.post("/suppliers/", json=supplier_1)
    client.post("/suppliers/", json=supplier_2)
    
    # Step 2: List all suppliers
    response = client.get("/suppliers/")
    assert response.status_code == 200
    suppliers = response.json()
    assert len(suppliers) >= 2  # There should be at least two suppliers
    ids = [supplier["supplier_id"] for supplier in suppliers]
    assert "sup1" in ids
    assert "sup2" in ids

def test_create_duplicate_supplier(sample_supplier):
    """
    Integration Test: Attempt to Create a Duplicate Supplier
    - Endpoint Tested: POST /suppliers/
    - This test checks if creating a duplicate supplier is properly handled with an error.
    """
    # Step 1: Create the supplier
    client.post("/suppliers/", json=sample_supplier)
    
    # Step 2: Attempt to create the same supplier again
    response = client.post("/suppliers/", json=sample_supplier)
    assert response.status_code == 400
    assert "Supplier already exists" in response.json()["detail"]

def test_retrieve_non_existing_supplier():
    """
    Integration Test: Retrieve a Non-Existing Supplier
    - Endpoint Tested: GET /suppliers/{supplier_id}
    - This test checks if attempting to retrieve a non-existing supplier is properly handled with an error.
    """
    non_existing_id = "NON_EXISTING"
    
    # Step 1: Try to retrieve the non-existing supplier
    response = client.get(f"/suppliers/{non_existing_id}")
    assert response.status_code == 404
    assert "Supplier not found" in response.json()["detail"]

def test_update_non_existing_supplier():
    """
    Integration Test: Update a Non-Existing Supplier
    - Endpoint Tested: PUT /suppliers/{supplier_id}
    - This test checks if attempting to update a non-existing supplier is properly handled with an error.
    """
    updated_data = {
        "name": "Non Existing Update",
        "location": "Nowhere",
        "contact": "0000000000"
    }
    
    non_existing_id = "NON_EXISTING"
    
    # Step 1: Try to update the non-existing supplier
    response = client.put(f"/suppliers/{non_existing_id}", json=updated_data)
    assert response.status_code == 404
    assert "Supplier not found" in response.json()["detail"]

def test_delete_non_existing_supplier():
    """
    Integration Test: Delete a Non-Existing Supplier
    - Endpoint Tested: DELETE /suppliers/{supplier_id}
    - This test checks if attempting to delete a non-existing supplier is properly handled with an error.
    """
    non_existing_id = "NON_EXISTING"
    
    # Step 1: Try to delete the non-existing supplier
    response = client.delete(f"/suppliers/{non_existing_id}")
    assert response.status_code == 404
    assert "Supplier not found" in response.json()["detail"]
