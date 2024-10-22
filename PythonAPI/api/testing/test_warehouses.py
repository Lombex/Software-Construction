import pytest
import json
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient


# Temporary FastAPI app for testing
app = FastAPI()

# In-memory data to mock database
warehouses_data = []

client = TestClient(app)

@app.post("/warehouses/")
async def create_warehouse(warehouse: dict):
    if "id" not in warehouse:
        raise HTTPException(status_code=400, detail="Warehouse must have an 'id'")
    for existing_warehouse in warehouses_data:
        if existing_warehouse["id"] == warehouse["id"]:
            raise HTTPException(status_code=400, detail="Warehouse already exists")
    warehouses_data.append(warehouse)
    return warehouse

@app.get("/warehouses/{warehouse_id}")
async def get_warehouse(warehouse_id: int):
    for warehouse in warehouses_data:
        if warehouse["id"] == warehouse_id:
            return warehouse
    raise HTTPException(status_code=404, detail="Warehouse not found")

@app.put("/warehouses/{warehouse_id}")
async def update_warehouse(warehouse_id: int, updated_warehouse: dict):
    for index, warehouse in enumerate(warehouses_data):
        if warehouse["id"] == warehouse_id:
            warehouses_data[index].update(updated_warehouse)
            return warehouses_data[index]
    raise HTTPException(status_code=404, detail="Warehouse not found")

@app.delete("/warehouses/{warehouse_id}")
async def delete_warehouse(warehouse_id: int):
    for index, warehouse in enumerate(warehouses_data):
        if warehouse["id"] == warehouse_id:
            del warehouses_data[index]
            return {"detail": "Warehouse deleted"}
    raise HTTPException(status_code=404, detail="Warehouse not found")

@pytest.fixture
def sample_warehouse():
    return {
        "id": 1,
        "name": "Main Warehouse",
        "address": "Storage Street 5",
        "city": "Amsterdam",
        "zip_code": "1012AA",
        "country": "Netherlands",
        "contact_name": "John Doe",
        "contact_phone": "+31612345678",
        "contact_email": "john.doe@example.com"
    }

def test_create_warehouse(sample_warehouse):
    response = client.post("/warehouses/", json=sample_warehouse)
    assert response.status_code == 200
    assert response.json()["name"] == "Main Warehouse"

def test_get_warehouse(sample_warehouse):
    client.post("/warehouses/", json=sample_warehouse)
    response = client.get("/warehouses/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Main Warehouse"

def test_update_warehouse(sample_warehouse):
    client.post("/warehouses/", json=sample_warehouse)
    updated_data = {"name": "Updated Warehouse"}
    response = client.put("/warehouses/1", json=updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Warehouse"

def test_delete_warehouse(sample_warehouse):
    client.post("/warehouses/", json=sample_warehouse)
    response = client.delete("/warehouses/1")
    assert response.status_code == 200
    assert client.get("/warehouses/1").status_code == 404

