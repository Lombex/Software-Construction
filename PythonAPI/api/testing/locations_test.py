from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
import json
import pytest

# Define the FastAPI app
app = FastAPI()

# Load data from JSON file (locations.json)
try:
    with open("data/locations.json", "r") as file:
        locations_data = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    locations_data = []

client = TestClient(app)

# Temporary routes for testing
@app.post("/locations/")
async def create_location(location: dict):
    if "id" not in location:
        raise HTTPException(status_code=400, detail="Location must have an 'id'")
    for existing_location in locations_data:
        if existing_location.get("id") == location["id"]:
            raise HTTPException(status_code=400, detail="Location already exists")
    locations_data.append(location)
    return location

@app.get("/locations/{location_id}")
async def get_location(location_id: str):
    for location in locations_data:
        if location.get("id") == location_id:
            return location
    raise HTTPException(status_code=404, detail="Location not found")

@app.put("/locations/{location_id}")
async def update_location(location_id: str, updated_location: dict):
    for index, location in enumerate(locations_data):
        if location.get("id") == location_id:
            locations_data[index].update(updated_location)
            return locations_data[index]
    raise HTTPException(status_code=404, detail="Location not found")

@app.delete("/locations/{location_id}")
async def delete_location(location_id: str):
    for index, location in enumerate(locations_data):
        if location.get("id") == location_id:
            del locations_data[index]
            return {"detail": "Location deleted"}
    raise HTTPException(status_code=404, detail="Location not found")

@pytest.fixture
def sample_location():
    """
    Fixture to provide sample location data.
    """
    return {
        "id": "location1",
        "name": "Sample Location",
        "address": "123 Main St"
    }

# Happy Path Tests
def test_create_location_integration(sample_location):
    response = client.get(f"/locations/{sample_location['id']}")
    assert response.status_code == 404  # Ensure it doesn't exist before creation
    
    response = client.post("/locations/", json=sample_location)
    assert response.status_code == 200  # Successful creation
    assert response.json()["name"] == sample_location["name"]

    response = client.get(f"/locations/{sample_location['id']}")
    assert response.status_code == 200
    assert response.json()["address"] == sample_location["address"]

def test_update_location_integration(sample_location):
    client.post("/locations/", json=sample_location)
    
    updated_data = {
        "name": sample_location["name"] + " Updated",
        "address": sample_location["address"] + " Updated"
    }
    response = client.put(f"/locations/{sample_location['id']}", json=updated_data)
    assert response.status_code == 200
    
    response = client.get(f"/locations/{sample_location['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == updated_data["name"]

def test_delete_location_integration(sample_location):
    client.post("/locations/", json=sample_location)

    response = client.delete(f"/locations/{sample_location['id']}")
    assert response.status_code == 200
    
    response = client.get(f"/locations/{sample_location['id']}")
    assert response.status_code == 404

def test_list_locations_integration():
    location_1 = {"id": "location1", "name": "Location One", "address": "123 Main St"}
    location_2 = {"id": "location2", "name": "Location Two", "address": "456 Elm St"}
    
    client.post("/locations/", json=location_1)
    client.post("/locations/", json=location_2)
    
    response = client.get("/locations/")
    assert response.status_code == 200
    locations = response.json()
    assert len(locations) >= 2
    assert any(location["id"] == "location1" for location in locations)
    assert any(location["id"] == "location2" for location in locations)

# Sad Path Tests
def test_create_location_invalid_data():
    invalid_location = {"name": "Invalid Location"}

    response = client.post("/locations/", json=invalid_location)
    assert response.status_code == 400

def test_get_non_existent_location():
    response = client.get("/locations/nonexistent")
    assert response.status_code == 404

def test_update_non_existent_location():
    response = client.put("/locations/nonexistent", json={"name": "Updated Name"})
    assert response.status_code == 404

def test_delete_non_existent_location():
    response = client.delete("/locations/nonexistent")
    assert response.status_code == 404
