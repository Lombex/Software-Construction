import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

# Temporary FastAPI app for testing
app = FastAPI()

# In-memory data to mock database
transfers_data = []

client = TestClient(app)

@app.post("/transfers/")
async def create_transfer(transfer: dict):
    if "id" not in transfer:
        raise HTTPException(status_code=400, detail="Transfer must have an 'id'")
    for existing_transfer in transfers_data:
        if existing_transfer["id"] == transfer["id"]:
            raise HTTPException(status_code=400, detail="Transfer already exists")
    transfers_data.append(transfer)
    return transfer

@app.get("/transfers/{transfer_id}")
async def get_transfer(transfer_id: int):
    for transfer in transfers_data:
        if transfer["id"] == transfer_id:
            return transfer
    raise HTTPException(status_code=404, detail="Transfer not found")

@app.put("/transfers/{transfer_id}")
async def update_transfer(transfer_id: int, updated_transfer: dict):
    for index, transfer in enumerate(transfers_data):
        if transfer["id"] == transfer_id:
            transfers_data[index].update(updated_transfer)
            return transfers_data[index]
    raise HTTPException(status_code=404, detail="Transfer not found")

@app.delete("/transfers/{transfer_id}")
async def delete_transfer(transfer_id: int):
    for index, transfer in enumerate(transfers_data):
        if transfer["id"] == transfer_id:
            del transfers_data[index]
            return {"detail": "Transfer deleted"}
    raise HTTPException(status_code=404, detail="Transfer not found")

@pytest.fixture
def sample_transfer():
    return {
        "id": 1,
        "reference": "TR00001",
        "transfer_from": 9113,
        "transfer_to": 9229,
        "transfer_status": "Completed",
        "created_at": "2000-03-11T13:11:14Z",
        "updated_at": "2000-03-12T16:11:14Z",
        "items": [
            {
                "item_id": "P007435",
                "amount": 23
            }
        ]
    }

def test_create_transfer(sample_transfer):
    response = client.post("/transfers/", json=sample_transfer)
    assert response.status_code == 200
    assert response.json()["reference"] == "TR00001"

def test_get_transfer(sample_transfer):
    client.post("/transfers/", json=sample_transfer)
    response = client.get("/transfers/1")
    assert response.status_code == 200
    assert response.json()["reference"] == "TR00001"

def test_get_incorrect_transfer():
    response = client.get("/transfers/-77")
    assert response.status_code == 404

def test_update_transfer(sample_transfer):
    client.post("/transfers/", json=sample_transfer)
    updated_data = {"transfer_status": "Pending"}
    response = client.put("/transfers/1", json=updated_data)
    assert response.status_code == 200
    assert response.json()["transfer_status"] == "Pending"

def test_update_incorrect_transfer():
    updated_data = {"transfer_status": "Pending"}
    response = client.put("/transfers/-15", json=updated_data)
    assert response.status_code == 404

def test_delete_transfer(sample_transfer):
    client.post("/transfers/", json=sample_transfer)
    response = client.delete("/transfers/1")
    assert response.status_code == 200
    assert client.get("/transfers/1").status_code == 404

def test_delete_incorrect_transfer():
    response = client.delete("/transfers/-44")
    assert response.status_code == 404

def test_partial_update_transfer(sample_transfer):
    client.post("/transfers/", json=sample_transfer)
    updated_data = {"transfer_status": "In Progress"}
    response = client.put("/transfers/1", json=updated_data)
    assert response.status_code == 200
    assert response.json()["transfer_status"] == "In Progress"

def test_create_multiple_transfers(sample_transfer):
    transfer_2 = sample_transfer.copy()
    transfer_2["id"] = 2
    transfer_2["reference"] = "TR00002"

    client.post("/transfers/", json=sample_transfer)
    response_2 = client.post("/transfers/", json=transfer_2)
    assert response_2.status_code == 200
    assert response_2.json()["reference"] == "TR00002"

def test_get_all_transfers(sample_transfer):
    transfer_2 = sample_transfer.copy()
    transfer_2["id"] = 2
    transfer_2["reference"] = "TR00002"

    client.post("/transfers/", json=sample_transfer)
    client.post("/transfers/", json=transfer_2)
    response = client.get("/transfers/1")
    response_2 = client.get("/transfers/2")
    assert response.status_code == 200
    assert response_2.status_code == 200

def test_delete_multiple_transfers(sample_transfer):
    transfer_2 = sample_transfer.copy()
    transfer_2["id"] = 2
    transfer_2["reference"] = "TR00002"

    client.post("/transfers/", json=sample_transfer)
    client.post("/transfers/", json=transfer_2)
    response = client.delete("/transfers/1")
    response_2 = client.delete("/transfers/2")
    assert response.status_code == 200
    assert response_2.status_code == 200
    assert client.get("/transfers/1").status_code == 404
    assert client.get("/transfers/2").status_code == 404


def test_create_transfer_with_no_items():
    response = client.post("/transfers/", json={
        "id": 3,
        "reference": "TR00003",
        "transfer_from": 9113,
        "transfer_to": 9229,
        "transfer_status": "Pending",
        "created_at": "2022-01-01T10:00:00Z",
        "updated_at": "2022-01-02T10:00:00Z"
    })
    assert response.status_code == 200
    assert response.json()["id"] == 3
    assert response.json().get("items") is None

def test_update_transfer_with_multiple_items(sample_transfer):
    client.post("/transfers/", json=sample_transfer)
    updated_items = [
        {"item_id": "P007435", "amount": 30},
        {"item_id": "P009557", "amount": 5}
    ]
    response = client.put("/transfers/1", json={"items": updated_items})
    assert response.status_code == 200
    assert len(response.json()["items"]) == 2
    assert response.json()["items"][0]["amount"] == 30

def test_update_transfer_status_only(sample_transfer):
    client.post("/transfers/", json=sample_transfer)
    updated_data = {"transfer_status": "Delivered"}
    response = client.put("/transfers/1", json=updated_data)
    assert response.status_code == 200
    assert response.json()["transfer_status"] == "Delivered"

def test_create_transfer_with_duplicate_item_ids():
    response = client.post("/transfers/", json={
        "id": 4,
        "reference": "TR00004",
        "transfer_from": 9113,
        "transfer_to": 9229,
        "transfer_status": "Pending",
        "created_at": "2022-02-01T10:00:00Z",
        "updated_at": "2022-02-02T10:00:00Z",
        "items": [
            {"item_id": "P007435", "amount": 10},
            {"item_id": "P007435", "amount": 5}
        ]
    })
    assert response.status_code == 200
    assert len(response.json()["items"]) == 2
    assert response.json()["items"][0]["item_id"] == "P007435"

def test_delete_transfer_with_items(sample_transfer):
    client.post("/transfers/", json=sample_transfer)
    response = client.delete("/transfers/1")
    assert response.status_code == 200
    assert client.get("/transfers/1").status_code == 404

# These tests cover various CRUD operations for the Transfers FastAPI app, including more scenarios like updating partial transfers, handling multiple transfers, transfers with items, and edge cases.
# Run the tests with pytest using `pytest <test_filename>.py`.
