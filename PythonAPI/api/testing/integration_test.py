import requests

API_URL = "http://localhost:3000"  # Change this to your actual API URL
API_KEY = "a1b2c3d4e5"  # Replace with your API key for testing
APP_NAME = "CargoHUB Dashboard 2"  # The app name used for authorization

def test_shipment_creation_and_retrieval():
    headers = {
        "Authorization": API_KEY,  # Use the API key directly for authorization
        "App": APP_NAME  # Ensure APP_NAME is defined here
    }

    # 1. User tries to create a shipment with incorrect data
    response = requests.post(
        f"{API_URL}/api/v1/shipments",
        headers=headers,
        json={"destination": "", "weight": -10}
    )
    # Print the actual response
    print(f"Response Status Code (Incorrect Data): {response.status_code}")
    print(f"Response Body (Incorrect Data): {response.text}")
    
    # Assert the expected status code
    assert response.status_code == 400, "Expected validation error for incorrect shipment data."

    # 2. User tries to create a shipment with correct data
    shipment_data = {"destination": "Warehouse A", "weight": 20, "sender": "Sender A"}
    response = requests.post(
        f"{API_URL}/api/v1/shipments",
        headers=headers,
        json=shipment_data
    )
    # Print the actual response
    print(f"Response Status Code (Correct Data): {response.status_code}")
    print(f"Response Body (Correct Data): {response.text}")

    # Assert the expected status code for successful creation
    assert response.status_code == 201, "Expected successful creation of shipment."

    created_shipment = response.json()
    shipment_id = created_shipment["id"]
    assert created_shipment["destination"] == shipment_data["destination"], "Created shipment destination does not match."

    # 3. Verify shipment is saved
    response = requests.get(f"{API_URL}/api/v1/shipments/{shipment_id}", headers=headers)
    # Print the actual response for retrieval
    print(f"Response Status Code (Retrieve Shipment): {response.status_code}")
    print(f"Response Body (Retrieve Shipment): {response.text}")

    assert response.status_code == 200, "Expected successful retrieval of shipment."
    retrieved_shipment = response.json()
    assert retrieved_shipment["id"] == shipment_id, "Retrieved shipment ID does not match."

def test_shipment_creation_without_login():
    response = requests.post(f"{API_URL}/api/v1/shipments", json={"destination": "Warehouse A", "weight": 20})
    assert response.status_code == 401, "Expected failure response for unauthorized shipment creation."

def test_invalid_shipment_update():
    headers = {
        "Authorization": API_KEY,  # Use the API key directly for authorization
        "App": APP_NAME
    }

    # 1. User creates a shipment
    shipment_data = {"destination": "Warehouse B", "weight": 15, "sender": "Sender B"}
    response = requests.post(f"{API_URL}/api/v1/shipments", headers=headers, json=shipment_data)
    assert response.status_code == 201
    created_shipment = response.json()
    shipment_id = created_shipment["id"]

    # 2. User tries to update the shipment with incorrect data
    response = requests.put(f"{API_URL}/api/v1/shipments/{shipment_id}", headers=headers, json={"weight": -5})
    assert response.status_code == 400, "Expected validation error for invalid shipment update."

def test_valid_shipment_update():
    headers = {
        "Authorization": API_KEY,  # Use the API key directly for authorization
        "App": APP_NAME
    }

    # Create a shipment
    shipment_data = {"destination": "Warehouse C", "weight": 30, "sender": "Sender C"}
    response = requests.post(f"{API_URL}/api/v1/shipments", headers=headers, json=shipment_data)
    created_shipment = response.json()
    shipment_id = created_shipment["id"]

    # Update the shipment with correct data
    updated_data = {"destination": "Warehouse D"}
    response = requests.put(f"{API_URL}/api/v1/shipments/{shipment_id}", headers=headers, json=updated_data)
    assert response.status_code == 200, "Expected successful shipment update."

    # Verify the updated shipment
    response = requests.get(f"{API_URL}/api/v1/shipments/{shipment_id}", headers=headers)
    updated_shipment = response.json()
    assert updated_shipment["destination"] == "Warehouse D", "Shipment destination not updated correctly."

def test_shipment_deletion_and_retrieval():
    headers = {
        "Authorization": API_KEY,  # Use the API key directly for authorization
        "App": APP_NAME
    }

    # Create a shipment
    shipment_data = {"destination": "Warehouse E", "weight": 40, "sender": "Sender D"}
    response = requests.post(f"{API_URL}/api/v1/shipments", headers=headers, json=shipment_data)
    created_shipment = response.json()
    shipment_id = created_shipment["id"]

    # Delete the shipment
    response = requests.delete(f"{API_URL}/api/v1/shipments/{shipment_id}", headers=headers)
    assert response.status_code == 204, "Expected successful deletion of shipment."

    # Try to retrieve the deleted shipment
    response = requests.get(f"{API_URL}/api/v1/shipments/{shipment_id}", headers=headers)
    assert response.status_code == 404, "Expected failure response for retrieving deleted shipment."

# Example location tests would follow a similar structure

if __name__ == "__main__":
    test_shipment_creation_and_retrieval()
    test_shipment_creation_without_login()
    test_invalid_shipment_update()
    test_valid_shipment_update()
    test_shipment_deletion_and_retrieval()
    print("All integration tests passed.")
