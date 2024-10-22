import json
import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

# In-memory storage for simplicity
app = FastAPI()

# Load data from JSON file (shipments.json)
try:
    with open("data/shipments.json", "r") as file:
        shipments_data = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    shipments_data = []

@app.post("/shipments")
def create_shipment(shipment: dict):
    shipments_data.append(shipment)
    return {"message": "Shipment created", "shipment": shipment}

@app.get("/shipments/")
def get_all_shipments():
    return shipments_data

@app.get("/shipments/{shipment_id}")
def get_shipment(shipment_id: int):
    if shipment_id < 0 or shipment_id >= len(shipments_data):
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipments_data[shipment_id]

@app.put("/shipments/{shipment_id}")
def update_shipment(shipment_id: int, updated_shipment: dict):
    if shipment_id < 0 or shipment_id >= len(shipments_data):
        raise HTTPException(status_code=404, detail="Shipment not found")
    shipments_data[shipment_id].update(updated_shipment)
    return {"message": "Shipment updated", "shipment": shipments_data[shipment_id]}

@app.delete("/shipments/{shipment_id}")
def delete_shipment(shipment_id: int):
    if shipment_id < 0 or shipment_id >= len(shipments_data):
        raise HTTPException(status_code=404, detail="Shipment not found")
    deleted_shipment = shipments_data.pop(shipment_id)
    return {"message": "Shipment deleted", "shipment": deleted_shipment}

@app.post("/login")
def login(username: str, password: str):
    # Simple authentication example
    if username == "user" and password == "pass":
        return {"token": "some_fake_token"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Initialize the TestClient
@pytest.fixture
def client():
    return TestClient(app)

# Happy Path Tests
def test_create_shipment_success(client):
    new_shipment = {"destination": "Warehouse A", "weight": 20, "sender": "Sender A"}
    response = client.post("/shipments", json=new_shipment)
    
    assert response.status_code == 200
    assert response.json()["shipment"]["destination"] == "Warehouse A"
    assert response.json()["shipment"]["weight"] == 20

def test_create_multiple_shipments(client):
    shipment_1 = {"destination": "Warehouse A", "weight": 20, "sender": "Sender A"}
    shipment_2 = {"destination": "Warehouse B", "weight": 25, "sender": "Sender B"}
    
    response_1 = client.post("/shipments", json=shipment_1)
    response_2 = client.post("/shipments", json=shipment_2)
    
    assert response_1.status_code == 200
    assert response_2.status_code == 200
    
    response = client.get("/shipments/")
    assert response.status_code == 200
    shipments = response.json()
    assert len(shipments) >= 2

def test_retrieve_all_shipments_success(client):
    response = client.get("/shipments/")
    assert response.status_code == 200
    assert len(response.json()) >= 1  # Check that at least one shipment exists

def test_retrieve_shipment_by_id(client):
    new_shipment = {"destination": "Warehouse C", "weight": 30, "sender": "Sender C"}
    
    create_response = client.post("/shipments", json=new_shipment)
    shipment_id = len(shipments_data) - 1  # Assuming the ID is the index
    response = client.get(f"/shipments/{shipment_id}")
    
    assert response.status_code == 200
    assert response.json()["destination"] == new_shipment["destination"]

def test_update_shipment_success(client):
    new_shipment = {"destination": "Warehouse D", "weight": 40, "sender": "Sender D"}
    client.post("/shipments", json=new_shipment)
    
    updated_shipment = {"destination": "Warehouse B", "weight": 25}
    shipment_id = len(shipments_data) - 1  # Assuming the ID is the index
    response = client.put(f"/shipments/{shipment_id}", json=updated_shipment)
    
    assert response.status_code == 200
    assert response.json()["shipment"]["destination"] == "Warehouse B"

def test_delete_shipment_success(client):
    new_shipment = {"destination": "Warehouse E", "weight": 50, "sender": "Sender E"}
    client.post("/shipments", json=new_shipment)
    
    shipment_id = len(shipments_data) - 1  # Assuming the ID is the index
    response = client.delete(f"/shipments/{shipment_id}")
    
    assert response.status_code == 200

def test_create_shipment_with_login(client):
    login_response = client.post("/login/", json={"username": "user", "password": "pass"})
    assert login_response.status_code == 200
    token = login_response.json()["token"]
    
    client.headers.update({"Authorization": f"Bearer {token}"})
    
    new_shipment = {"destination": "Warehouse A", "weight": 20, "sender": "Sender A"}
    response = client.post("/shipments", json=new_shipment)
    
    assert response.status_code == 200

def test_update_shipment_sender(client):
    new_shipment = {"destination": "Warehouse D", "weight": 40, "sender": "Sender D"}
    client.post("/shipments", json=new_shipment)
    
    shipment_id = len(shipments_data) - 1  # Assuming the ID is the index
    update_data = {"sender": "Updated Sender"}
    response = client.put(f"/shipments/{shipment_id}", json=update_data)
    
    assert response.status_code == 200
    updated_shipment = response.json()
    assert updated_shipment["shipment"]["sender"] == "Updated Sender"

# Sad Path Tests
def test_create_shipment_invalid_data(client):
    invalid_shipment = {"destination": "", "weight": -10}
    response = client.post("/shipments/", json=invalid_shipment)
    assert response.status_code == 422  # FastAPI validation error

def test_retrieve_non_existent_shipment(client):
    response = client.get("/shipments/999")
    assert response.status_code == 404

def test_update_shipment_with_invalid_data(client):
    invalid_shipment = {"weight": -5}
    shipment_id = 0  # Assuming this shipment exists
    response = client.put(f"/shipments/{shipment_id}", json=invalid_shipment)
    assert response.status_code == 422  # FastAPI validation error

def test_delete_non_existent_shipment(client):
    response = client.delete("/shipments/999")
    assert response.status_code == 404
