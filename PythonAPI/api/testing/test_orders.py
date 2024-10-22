import pytest
import json
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

# Temporary FastAPI app for testing
app = FastAPI()

# In-memory data to mock database
orders_data = []

client = TestClient(app)

@app.post("/orders/")
async def create_order(order: dict):
    if "id" not in order:
        raise HTTPException(status_code=400, detail="Order must have an 'id'")
    for existing_order in orders_data:
        if existing_order["id"] == order["id"]:
            raise HTTPException(status_code=400, detail="Order already exists")
    orders_data.append(order)
    return order

@app.get("/orders/{order_id}")
async def get_order(order_id: int):
    for order in orders_data:
        if order["id"] == order_id:
            return order
    raise HTTPException(status_code=404, detail="Order not found")

@app.put("/orders/{order_id}")
async def update_order(order_id: int, updated_order: dict):
    for index, order in enumerate(orders_data):
        if order["id"] == order_id:
            orders_data[index].update(updated_order)
            return orders_data[index]
    raise HTTPException(status_code=404, detail="Order not found")

@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    for index, order in enumerate(orders_data):
        if order["id"] == order_id:
            del orders_data[index]
            return {"detail": "Order deleted"}
    raise HTTPException(status_code=404, detail="Order not found")

@pytest.fixture
def sample_order():
    return {
        "id": 1,
        "source_id": 33,
        "order_date": "2019-04-03T11:33:15Z",
        "request_date": "2019-04-07T11:33:15Z",
        "reference": "ORD00001",
        "reference_extra": "Bedreven arm straffen bureau.",
        "order_status": "Delivered",
        "notes": "Voedsel vijf vork heel.",
        "shipping_notes": "Buurman betalen plaats bewolkt.",
        "picking_notes": "Ademen fijn volgorde scherp aardappel op leren.",
        "warehouse_id": 18,
        "ship_to": None,
        "bill_to": None,
        "shipment_id": 1,
        "total_amount": 9905.13,
        "total_discount": 150.77,
        "total_tax": 372.72,
        "total_surcharge": 77.6,
        "created_at": "2019-04-03T11:33:15Z",
        "updated_at": "2019-04-05T07:33:15Z",
        "items": [
            {"item_id": "P007435", "amount": 23},
            {"item_id": "P009557", "amount": 1},
            {"item_id": "P009553", "amount": 50}
        ]
    }

def test_create_order(sample_order):
    response = client.post("/orders/", json=sample_order)
    assert response.status_code == 200
    assert response.json()["reference"] == "ORD00001"

def test_get_orders(sample_order):
    client.post("/orders/", json=sample_order)
    response = client.get("/orders/1")
    assert response.status_code == 200
    assert response.json()["reference"] == "ORD00001"

def test_get_incorrect_order():
    response = client.get("/orders/-77")
    assert response.status_code == 404

def test_post_order_same_id(sample_order):
    client.post("/orders/", json=sample_order)
    response = client.post("/orders/", json=sample_order)
    assert response.status_code == 400



def test_update_order(sample_order):
    client.post("/orders/", json=sample_order)
    updated_data = {
        "order_status": "Updated",
        "total_amount": 1234.56
    }
    response = client.put("/orders/1", json=updated_data)
    assert response.status_code == 200
    assert response.json()["order_status"] == "Updated"

def test_update_incorrect_order():
    response = client.put("/orders/-1", json={
        "order_status": "Updated"
    })
    assert response.status_code == 404

def test_delete_order(sample_order):
    client.post("/orders/", json=sample_order)
    response = client.delete("/orders/1")
    assert response.status_code == 200
    assert client.get("/orders/1").status_code == 404

def test_delete_incorrect_order():
    response = client.delete("/orders/-44")
    assert response.status_code == 404

def test_update_partial_order(sample_order):
    client.post("/orders/", json=sample_order)
    updated_data = {
        "total_discount": 200.50
    }
    response = client.put("/orders/1", json=updated_data)
    assert response.status_code == 200
    assert response.json()["total_discount"] == 200.50

def test_create_multiple_orders(sample_order):
    order_2 = sample_order.copy()
    order_2["id"] = 2
    order_2["reference"] = "ORD00002"

    client.post("/orders/", json=sample_order)
    response_2 = client.post("/orders/", json=order_2)
    assert response_2.status_code == 200
    assert response_2.json()["reference"] == "ORD00002"

def test_get_all_orders(sample_order):
    order_2 = sample_order.copy()
    order_2["id"] = 2
    order_2["reference"] = "ORD00002"

    client.post("/orders/", json=sample_order)
    client.post("/orders/", json=order_2)
    response = client.get("/orders/1")
    response_2 = client.get("/orders/2")
    assert response.status_code == 200
    assert response_2.status_code == 200

def test_delete_multiple_orders(sample_order):
    order_2 = sample_order.copy()
    order_2["id"] = 2
    order_2["reference"] = "ORD00002"

    client.post("/orders/", json=sample_order)
    client.post("/orders/", json=order_2)
    response = client.delete("/orders/1")
    response_2 = client.delete("/orders/2")
    assert response.status_code == 200
    assert response_2.status_code == 200
    assert client.get("/orders/1").status_code == 404
    assert client.get("/orders/2").status_code == 404

def test_create_order_with_no_items():
    response = client.post("/orders/", json={
        "id": 3,
        "source_id": 33,
        "order_date": "2022-01-01T10:00:00Z",
        "request_date": "2022-01-02T10:00:00Z",
        "reference": "ORD00003",
        "order_status": "Pending",
        "total_amount": 5000.00
    })
    assert response.status_code == 200
    assert response.json()["id"] == 3
    assert response.json().get("items") is None

# These tests cover various CRUD operations for the Orders FastAPI app, including more scenarios like updating partial orders, handling multiple orders, and testing edge cases.
# Run the tests with pytest using `pytest <test_filename>.py`.
