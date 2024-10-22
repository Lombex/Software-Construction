import pytest
from httpx import Client, codes

@pytest.fixture
def client():
    """Fixture to create an HTTP client with necessary headers."""
    return Client(base_url="http://localhost:3000/api/v1/",
                  headers={"Content-Type": "application/json", "API_KEY": "a1b2c3d4e5"})

def test_create_shipment_success(client):
    new_shipment = {
        "destination": "Warehouse A",
        "weight": 20,
        "sender": "Sender A"
    }
    response = client.post("/shipments", json=new_shipment)
    
    assert response.status_code == codes.CREATED
    assert "id" in response.json()  # Ensure the response has an ID

def test_create_shipment_invalid_data(client):
    new_shipment = {
        "destination": "",
        "weight": -10,
        "sender": "Sender A"  # Added sender to match valid input
    }
    response = client.post("/shipments", json=new_shipment)
    assert response.status_code == codes.BAD_REQUEST

def test_retrieve_shipment(client):
    # Ensure you have a shipment with ID 1 created beforehand
    response = client.get("/shipments/1")  # Assuming ID 1 exists
    assert response.status_code == codes.OK
    assert "id" in response.json()

def test_retrieve_non_existent_shipment(client):
    response = client.get("/shipments/-1")  # Test for a non-existent ID
    assert response.status_code == codes.NOT_FOUND

def test_update_shipment_success(client):
    updated_shipment = {
        "destination": "Warehouse B",
        "weight": 25
    }
    # Ensure you have a shipment with ID 1 created beforehand
    response = client.put("/shipments/1", json=updated_shipment)  # Assuming ID 1 exists
    assert response.status_code == codes.OK

def test_update_shipment_invalid_data(client):
    updated_shipment = {
        "weight": -5  # Invalid weight
    }
    # Ensure you have a shipment with ID 1 created beforehand
    response = client.put("/shipments/1", json=updated_shipment)  # Assuming ID 1 exists
    assert response.status_code == codes.BAD_REQUEST

def test_delete_shipment_success(client):
    # Ensure you have a shipment with ID 1 created beforehand
    response = client.delete("/shipments/1")  # Assuming ID 1 exists
    assert response.status_code == codes.OK

def test_delete_non_existent_shipment(client):
    response = client.delete("/shipments/-10")  # Test for a non-existent ID
    assert response.status_code == codes.NOT_FOUND

def test_create_shipment_unauthorized(client):
    client.headers["API_KEY"] = "wrong_key"  # Simulate unauthorized access
    new_shipment = {
        "destination": "Warehouse A",
        "weight": 20,
        "sender": "Sender A"
    }
    response = client.post("/shipments", json=new_shipment)
    assert response.status_code == codes.UNAUTHORIZED

def test_update_shipment_unauthorized(client):
    client.headers["API_KEY"] = "wrong_key"  # Simulate unauthorized access
    updated_shipment = {
        "destination": "Warehouse B",
        "weight": 25
    }
    # Ensure you have a shipment with ID 1 created beforehand
    response = client.put("/shipments/1", json=updated_shipment)  # Assuming ID 1 exists
    assert response.status_code == codes.UNAUTHORIZED

def test_delete_shipment_unauthorized(client):
    client.headers["API_KEY"] = "wrong_key"  # Simulate unauthorized access
    # Ensure you have a shipment with ID 1 created beforehand
    response = client.delete("/shipments/1")  # Assuming ID 1 exists
    assert response.status_code == codes.UNAUTHORIZED
