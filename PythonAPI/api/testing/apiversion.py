import pytest
import os
import sys
import requests

# Ensure the providers module is in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

BASE_URL = "http://localhost:5000"  

@pytest.fixture
def setup_orders():
    # This could reset the order dataset for testing, if necessary
    return

@pytest.fixture
def setup_shipments():
    # This could reset the shipment dataset for testing, if necessary
    return

def test_fetch_all_orders(setup_orders):
    response = requests.get(f"{BASE_URL}/orders")
    assert response.status_code == 200, "Should return status code 200"
    data = response.json()
    assert isinstance(data['data'], list), "Orders should be returned as a list"
    assert len(data['data']) > 0, "Order list should not be empty"

def test_fetch_order_by_id(setup_orders):
    order_id = 1  # Adjust based on your test data
    response = requests.get(f"{BASE_URL}/orders/{order_id}")
    assert response.status_code == 200, "Should return status code 200"
    data = response.json()
    assert data['data'] is not None, f"Order with ID {order_id} should exist"
    assert data['data']['id'] == order_id, f"Order ID should match {order_id}"

def test_create_order(setup_orders):
    new_order = {
        "id": 5,  # Ensure this ID doesn't conflict with existing IDs
        "source_id": 40,
        "order_date": "2024-01-01T12:00:00Z",
        "request_date": "2024-01-05T12:00:00Z",
        "total_amount": 1000.0,
        "total_discount": 0.0,
        "total_tax": 100.0,
        "total_surcharge": 50.0,
        "items": [{"item_id": "P001111", "amount": 10}]
    }
    response = requests.post(f"{BASE_URL}/orders", json=new_order)
    assert response.status_code == 201, "Should return status code 201 for created resource"

    # Verify that the order was created successfully
    fetch_response = requests.get(f"{BASE_URL}/orders/5")
    fetch_data = fetch_response.json()
    assert fetch_data['data'] is not None, "Newly created order should exist"

def test_update_order_status(setup_orders):
    order_id = 1  # Adjust based on your test data
    updated_order = {
        "order_status": "Canceled"  # Modify the order status
    }
    response = requests.put(f"{BASE_URL}/orders/{order_id}", json=updated_order)
    assert response.status_code == 200, "Should return status code 200 for updated resource"

    # Fetch updated order
    fetch_response = requests.get(f"{BASE_URL}/orders/{order_id}")
    fetch_data = fetch_response.json()
    assert fetch_data['data']['order_status'] == "Canceled", "Order status should be updated"

def test_delete_order(setup_orders):
    order_id = 2  # Adjust based on your test data
    response = requests.delete(f"{BASE_URL}/orders/{order_id}")
    assert response.status_code == 204, "Should return status code 204 for deleted resource"

    # Verify that the order was deleted
    fetch_response = requests.get(f"{BASE_URL}/orders/{order_id}")
    fetch_data = fetch_response.json()
    assert fetch_data['data'] is None, f"Order with ID {order_id} should no longer exist"

def test_fetch_all_shipments(setup_shipments):
    response = requests.get(f"{BASE_URL}/shipments")
    assert response.status_code == 200, "Should return status code 200"
    data = response.json()
    assert isinstance(data['data'], list), "Shipments should be returned as a list"
    assert len(data['data']) > 0, "Shipment list should not be empty"

def test_fetch_shipment_by_id(setup_shipments):
    shipment_id = 1  # Adjust based on your test data
    response = requests.get(f"{BASE_URL}/shipments/{shipment_id}")
    assert response.status_code == 200, "Should return status code 200"
    data = response.json()
    assert data['data'] is not None, f"Shipment with ID {shipment_id} should exist"
    assert data['data']['id'] == shipment_id, f"Shipment ID should match {shipment_id}"

def test_create_shipment(setup_shipments):
    new_shipment = {
        "id": 5,  # Ensure this ID doesn't conflict with existing IDs
        "items": [{"item_id": "P001111", "amount": 10}],
        "created_at": "2024-01-01T12:00:00Z",
        "updated_at": "2024-01-01T12:00:00Z"
    }
    response = requests.post(f"{BASE_URL}/shipments", json=new_shipment)
    assert response.status_code == 201, "Should return status code 201 for created resource"

    # Verify that the shipment was created successfully
    fetch_response = requests.get(f"{BASE_URL}/shipments/5")
    fetch_data = fetch_response.json()
    assert fetch_data['data'] is not None, "Newly created shipment should exist"

def test_update_shipment_status(setup_shipments):
    shipment_id = 1  # Adjust based on your test data
    updated_shipment = {
        "status": "Delivered"  # Modify the shipment status
    }
    response = requests.put(f"{BASE_URL}/shipments/{shipment_id}", json=updated_shipment)
    assert response.status_code == 200, "Should return status code 200 for updated resource"

    # Fetch updated shipment
    fetch_response = requests.get(f"{BASE_URL}/shipments/{shipment_id}")
    fetch_data = fetch_response.json()
    assert fetch_data['data']['status'] == "Delivered", "Shipment status should be updated"

def test_delete_shipment(setup_shipments):
    shipment_id = 2  # Adjust based on your test data
    response = requests.delete(f"{BASE_URL}/shipments/{shipment_id}")
    assert response.status_code == 204, "Should return status code 204 for deleted resource"

    # Verify that the shipment was deleted
    fetch_response = requests.get(f"{BASE_URL}/shipments/{shipment_id}")
    fetch_data = fetch_response.json()
    assert fetch_data['data'] is None, f"Shipment with ID {shipment_id} should no longer exist"
