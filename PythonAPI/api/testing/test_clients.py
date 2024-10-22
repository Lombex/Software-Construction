import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, HTTPException

# Temporary FastAPI app for testing
app = FastAPI()

# In-memory data to mock database
clients_data = []

client = TestClient(app)

@app.post("/clients/")
async def create_client(client: dict):
    if "id" not in client:
        raise HTTPException(status_code=400, detail="Client must have an 'id'")
    for existing_client in clients_data:
        if existing_client["id"] == client["id"]:
            raise HTTPException(status_code=400, detail="Client already exists")
    clients_data.append(client)
    return client

@app.get("/clients/{client_id}")
async def get_client(client_id: int):
    for client in clients_data:
        if client["id"] == client_id:
            return client
    raise HTTPException(status_code=404, detail="Client not found")

@app.put("/clients/{client_id}")
async def update_client(client_id: int, updated_client: dict):
    for index, client in enumerate(clients_data):
        if client["id"] == client_id:
            clients_data[index].update(updated_client)
            return clients_data[index]
    raise HTTPException(status_code=404, detail="Client not found")

@app.delete("/clients/{client_id}")
async def delete_client(client_id: int):
    for index, client in enumerate(clients_data):
        if client["id"] == client_id:
            del clients_data[index]
            return {"detail": "Client deleted"}
    raise HTTPException(status_code=404, detail="Client not found")

@pytest.fixture
def sample_client():
    return {
        "id": 1,
        "name": "Jane Doe",
        "address": "Second Street 2",
        "city": "Utrecht",
        "zip_code": "3511AA",
        "country": "Netherlands",
        "contact_name": "Jane Doe",
        "contact_phone": "+31687654321",
        "contact_email": "jane.doe@example.com"
    }

def test_create_client(sample_client):
    response = client.post("/clients/", json=sample_client)
    assert response.status_code == 200
    assert response.json()["name"] == "Jane Doe"

def test_get_client(sample_client):
    client.post("/clients/", json=sample_client)
    response = client.get("/clients/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Jane Doe"

def test_update_client(sample_client):
    client.post("/clients/", json=sample_client)
    updated_data = {"name": "Jane Updated"}
    response = client.put("/clients/1", json=updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Jane Updated"

def test_delete_client(sample_client):
    client.post("/clients/", json=sample_client)
    response = client.delete("/clients/1")
    assert response.status_code == 200
    assert client.get("/clients/1").status_code == 404