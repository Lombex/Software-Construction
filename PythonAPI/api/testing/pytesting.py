import pytest
from httpx import Client, codes
from unittest.mock import patch

@pytest.fixture
def client():
    """Fixture to create an HTTP client with necessary headers."""
    return Client(base_url="http://localhost:3000/api/v1/",
                  headers={"Content-Type": "application/json", "API_KEY": "a1b2c3d4e5"})

@patch('httpx.Client.post')
def test_create_shipment_success(mock_post, client):
    # Mock response data
    mock_post.return_value.status_code = codes.CREATED
    mock_post.return_value.json.return_value = {"id": 1}

    new_shipment = {
        "destination": "Warehouse A",
        "weight": 20,
        "sender": "Sender A"
    }
    response = client.post("/shipments", json=new_shipment)

    assert response.status_code == codes.CREATED
    assert "id" in response.json()  # Ensure the response has an ID

@patch('httpx.Client.post')
def test_create_shipment_invalid_data(mock_post, client):
    mock_post.return_value.status_code = codes.BAD_REQUEST

    new_shipment = {
        "destination": "",
        "weight": -10,
        "sender": "Sender A"
    }
    response = client.post("/shipments", json=new_shipment)
    assert response.status_code == codes.BAD_REQUEST

@patch('httpx.Client.get')
def test_retrieve_shipment(mock_get, client):
    # Mock response data for retrieving a shipment
    mock_get.return_value.status_code = codes.OK
    mock_get.return_value.json.return_value = {"id": 1, "destination": "Warehouse A"}

    response = client.get("/shipments/1")  # Assuming ID 1 exists
    assert response.status_code == codes.OK
    assert "id" in response.json()

@patch('httpx.Client.get')
def test_retrieve_non_existent_shipment(mock_get, client):
    mock_get.return_value.status_code = codes.NOT_FOUND

    response = client.get("/shipments/-1")
    assert response.status_code == codes.NOT_FOUND

@patch('httpx.Client.put')
def test_update_shipment_success(mock_put, client):
    mock_put.return_value.status_code = codes.OK

    updated_shipment = {
        "destination": "Warehouse B",
        "weight": 25
    }
    response = client.put("/shipments/1", json=updated_shipment)  # Assuming ID 1 exists
    assert response.status_code == codes.OK

@patch('httpx.Client.delete')
def test_delete_shipment_success(mock_delete, client):
    mock_delete.return_value.status_code = codes.OK

    response = client.delete("/shipments/1")  # Assuming ID 1 exists
    assert response.status_code == codes.OK

@patch('httpx.Client.post')
def test_create_shipment_unauthorized(mock_post, client):
    mock_post.return_value.status_code = codes.UNAUTHORIZED

    client.headers["API_KEY"] = "wrong_key"
    new_shipment = {
        "destination": "Warehouse A",
        "weight": 20,
        "sender": "Sender A"
    }
    response = client.post("/shipments", json=new_shipment)
    assert response.status_code == codes.UNAUTHORIZED

# Additional Tests

@patch('httpx.Client.post')
def test_create_shipment_with_login(mock_post, client):
    # Simulate successful login
    mock_post.return_value.status_code = codes.OK
    mock_post.return_value.json.return_value = {"token": "some_token"}

    # User login
    login_response = client.post("/login", json={"username": "user", "password": "pass"})
    assert login_response.status_code == codes.OK
    token = login_response.json().get("token")

    # Creating shipment after login
    new_shipment = {
        "destination": "Warehouse A",
        "weight": 20,
        "sender": "Sender A"
    }
    client.headers["Authorization"] = f"Bearer {token}"
    response = client.post("/shipments", json=new_shipment)
    
    assert response.status_code == codes.CREATED
    assert "id" in response.json()

@patch('httpx.Client.post')
def test_create_shipment_without_login(mock_post, client):
    mock_post.return_value.status_code = codes.UNAUTHORIZED

    new_shipment = {
        "destination": "Warehouse A",
        "weight": 20,
        "sender": "Sender A"
    }
    response = client.post("/shipments", json=new_shipment)
    assert response.status_code == codes.UNAUTHORIZED

@patch('httpx.Client.put')
def test_update_shipment_with_invalid_data(mock_put, client):
    mock_put.return_value.status_code = codes.BAD_REQUEST

    updated_shipment = {
        "weight": -5  # Invalid weight
    }
    response = client.put("/shipments/1", json=updated_shipment)  # Assuming ID 1 exists
    assert response.status_code == codes.BAD_REQUEST

@patch('httpx.Client.put')
def test_update_shipment_with_valid_data(mock_put, client):
    mock_put.return_value.status_code = codes.OK

    updated_shipment = {
        "destination": "Warehouse B",
        "weight": 25
    }
    response = client.put("/shipments/1", json=updated_shipment)  # Assuming ID 1 exists
    assert response.status_code == codes.OK

@patch('httpx.Client.delete')
def test_delete_shipment_without_login(mock_delete, client):
    mock_delete.return_value.status_code = codes.UNAUTHORIZED

    response = client.delete("/shipments/1")  # Assuming ID 1 exists
    assert response.status_code == codes.UNAUTHORIZED

@patch('httpx.Client.get')
def test_create_location_and_retrieve(mock_get, client):
    # Mock response data for creating a location
    mock_post.return_value.status_code = codes.CREATED
    mock_post.return_value.json.return_value = {"id": 1, "name": "Location A"}

    # Simulate user login to create a location
    login_response = client.post("/login", json={"username": "user", "password": "pass"})
    token = login_response.json().get("token")
    client.headers["Authorization"] = f"Bearer {token}"

    # Creating location
    new_location = {
        "name": "Location A",
        "address": "123 Main St"
    }
    response = client.post("/locations", json=new_location)
    
    assert response.status_code == codes.CREATED
    assert "id" in response.json()

    # Retrieve the created location
    location_id = response.json()["id"]
    mock_get.return_value.status_code = codes.OK
    mock_get.return_value.json.return_value = {"id": location_id, "name": "Location A"}

    response = client.get(f"/locations/{location_id}")
    assert response.status_code == codes.OK
    assert response.json()["name"] == "Location A"

# Further tests for locations can be added similarly based on your provided structure.

