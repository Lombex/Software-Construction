import pytest
import json
from fastapi.testclient import TestClient
from fastapi import FastAPI, HTTPException

# Define a temporary FastAPI app for testing
app = FastAPI()

# Load data from JSON file (inventories.json)
try:
    with open("data/inventories.json", "r") as file:
        inventories_data = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    inventories_data = []

client = TestClient(app)

# Temporary routes for testing
@app.post("/inventories/")
async def create_inventory(inventory: dict):
    if "inventory_id" not in inventory:
        raise HTTPException(status_code=400, detail="Inventory must have an 'inventory_id'")
    for existing_inventory in inventories_data:
        if "inventory_id" in existing_inventory and existing_inventory["inventory_id"] == inventory["inventory_id"]:
            raise HTTPException(status_code=400, detail="Inventory already exists")
    inventories_data.append(inventory)
    return inventory

@app.get("/inventories/{inventory_id}")
async def get_inventory(inventory_id: str):
    for inventory in inventories_data:
        if "inventory_id" in inventory and inventory["inventory_id"] == inventory_id:
            return inventory
    raise HTTPException(status_code=404, detail="Inventory not found")

@app.put("/inventories/{inventory_id}")
async def update_inventory(inventory_id: str, updated_inventory: dict):
    for index, inventory in enumerate(inventories_data):
        if "inventory_id" in inventory and inventory["inventory_id"] == inventory_id:
            inventories_data[index].update(updated_inventory)
            return inventories_data[index]
    raise HTTPException(status_code=404, detail="Inventory not found")

@app.delete("/inventories/{inventory_id}")
async def delete_inventory(inventory_id: str):
    for index, inventory in enumerate(inventories_data):
        if "inventory_id" in inventory and inventory["inventory_id"] == inventory_id:
            del inventories_data[index]
            return {"detail": "Inventory deleted"}
    raise HTTPException(status_code=404, detail="Inventory not found")

@app.get("/inventories/")
async def list_inventories():
    return inventories_data

@pytest.fixture
def sample_inventory():
    """
    Fixture to provide sample inventory data from the JSON file.
    Returns the first inventory in the JSON data.
    """
    return {
        "inventory_id": "inv1",
        "item_name": "Sample Inventory",
        "quantity": 50,
        "location": "Warehouse A"
    }

def test_create_inventory_integration(sample_inventory):
    """
    Integration Test: Create an Inventory (Happy Path)
    """
    # Step 1: Check if the inventory exists already (shouldn't)
    response = client.get(f"/inventories/{sample_inventory['inventory_id']}")
    assert response.status_code == 404  # The inventory should not exist before creation
    
    # Step 2: Create the inventory using the API
    response = client.post("/inventories/", json=sample_inventory)
    assert response.status_code == 200  # Successful creation returns HTTP 200
    assert response.json()["item_name"] == sample_inventory["item_name"]
    assert response.json()["quantity"] == sample_inventory["quantity"]
    
    # Step 3: Retrieve the newly created inventory to verify
    response = client.get(f"/inventories/{sample_inventory['inventory_id']}")
    assert response.status_code == 200
    inventory_data = response.json()
    assert inventory_data["item_name"] == sample_inventory["item_name"]
    assert inventory_data["quantity"] == sample_inventory["quantity"]
    assert inventory_data["location"] == sample_inventory["location"]

def test_get_inventory_integration(sample_inventory):
    """
    Integration Test: Retrieve an Inventory (Happy Path)
    """
    # Create the inventory first
    client.post("/inventories/", json=sample_inventory)
    
    # Step 1: Retrieve the inventory
    response = client.get(f"/inventories/{sample_inventory['inventory_id']}")
    assert response.status_code == 200
    inventory_data = response.json()
    assert inventory_data["item_name"] == sample_inventory["item_name"]
    assert inventory_data["quantity"] == sample_inventory["quantity"]
    assert inventory_data["location"] == sample_inventory["location"]

def test_update_inventory_integration(sample_inventory):
    """
    Integration Test: Update an Inventory (Happy Path)
    """
    # Create the inventory first
    client.post("/inventories/", json=sample_inventory)
    
    # Step 1: Update the inventory details
    updated_data = {
        "item_name": sample_inventory["item_name"] + " Updated",
        "quantity": sample_inventory["quantity"] + 10,
        "location": sample_inventory["location"] + " Updated"
    }
    response = client.put(f"/inventories/{sample_inventory['inventory_id']}", json=updated_data)
    assert response.status_code == 200  # Successful update returns HTTP 200
    
    # Step 2: Retrieve the updated inventory to verify
    response = client.get(f"/inventories/{sample_inventory['inventory_id']}")
    assert response.status_code == 200
    inventory_data = response.json()
    assert inventory_data["item_name"] == updated_data["item_name"]
    assert inventory_data["quantity"] == updated_data["quantity"]
    assert inventory_data["location"] == updated_data["location"]

def test_delete_inventory_integration(sample_inventory):
    """
    Integration Test: Delete an Inventory (Happy Path)
    """
    # Create the inventory first
    client.post("/inventories/", json=sample_inventory)
    
    # Step 1: Delete the inventory
    response = client.delete(f"/inventories/{sample_inventory['inventory_id']}")
    assert response.status_code == 200  # Successful deletion returns HTTP 200
    
    # Step 2: Verify the inventory has been deleted
    response = client.get(f"/inventories/{sample_inventory['inventory_id']}")
    assert response.status_code == 404  # Inventory should no longer exist

def test_list_inventories_integration():
    """
    Integration Test: List All Inventories (Happy Path)
    """
    # Step 1: Create multiple inventories
    inventory_1 = {"inventory_id": "inv1", "item_name": "Item One", "quantity": 10, "location": "Warehouse A"}
    inventory_2 = {"inventory_id": "inv2", "item_name": "Item Two", "quantity": 20, "location": "Warehouse B"}
    client.post("/inventories/", json=inventory_1)
    client.post("/inventories/", json=inventory_2)
    
    # Step 2: List all inventories
    response = client.get("/inventories/")
    assert response.status_code == 200
    inventories = response.json()
    assert len(inventories) >= 2  # There should be at least two inventories
    ids = [inventory["inventory_id"] for inventory in inventories]
    assert "inv1" in ids
    assert "inv2" in ids

def test_create_duplicate_inventory(sample_inventory):
    """
    Integration Test: Attempt to Create a Duplicate Inventory
    """
    # Step 1: Create the inventory
    client.post("/inventories/", json=sample_inventory)
    
    # Step 2: Attempt to create the same inventory again
    response = client.post("/inventories/", json=sample_inventory)
    assert response.status_code == 400
    assert "Inventory already exists" in response.json()["detail"]

def test_retrieve_non_existing_inventory():
    """
    Integration Test: Retrieve a Non-Existing Inventory
    """
    non_existing_id = "NON_EXISTING"
    
    # Step 1: Try to retrieve the non-existing inventory
    response = client.get(f"/inventories/{non_existing_id}")
    assert response.status_code == 404
    assert "Inventory not found" in response.json()["detail"]

def test_update_non_existing_inventory():
    """
    Integration Test: Update a Non-Existing Inventory
    """
    updated_data = {
        "item_name": "Non Existing Update",
        "quantity": 0,
        "location": "Nowhere"
    }
    
    non_existing_id = "NON_EXISTING"
    
    # Step 1: Try to update the non-existing inventory
    response = client.put(f"/inventories/{non_existing_id}", json=updated_data)
    assert response.status_code == 404
    assert "Inventory not found" in response.json()["detail"]
