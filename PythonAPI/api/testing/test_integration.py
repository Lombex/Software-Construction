import pytest
import os
import sys

# Ensure the providers module is in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from providers import data_provider
@pytest.fixture
def setup_orders():
    # Initialize orders for testing
    orders_pool = data_provider.fetch_order_pool()
    # You may want to reset or load a specific test dataset here.
    return orders_pool

@pytest.fixture
def setup_shipments():
    # Initialize shipments for testing
    shipments_pool = data_provider.fetch_shipment_pool()
    # You may want to reset or load a specific test dataset here.
    return shipments_pool

def test_fetch_all_orders(setup_orders):
    orders = setup_orders.get_orders()
    assert isinstance(orders, list), "Orders should be returned as a list"
    assert len(orders) > 0, "Order list should not be empty"

def test_fetch_order_by_id(setup_orders):
    order_id = 1  # Adjust based on your test data
    order = setup_orders.get_order(order_id)
    assert order is not None, f"Order with ID {order_id} should exist"
    assert order['id'] == order_id, f"Order ID should match {order_id}"

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
    setup_orders.add_order(new_order)
    assert setup_orders.get_order(5) is not None, "Newly created order should exist"

def test_update_order_status(setup_orders):
    order_id = 1  # Adjust based on your test data
    order = setup_orders.get_order(order_id)
    assert order is not None, f"Order with ID {order_id} should exist"

    updated_order = order
    updated_order["order_status"] = "Canceled"  # Modify the order status
    setup_orders.update_order(order_id, updated_order)
    updated_order = setup_orders.get_order(order_id)  # Fetch updated order
    assert updated_order['order_status'] == "Canceled", "Order status should be updated"

def test_delete_order(setup_orders):
    order_id = 2  # Adjust based on your test data
    setup_orders.remove_order(order_id)
    order = setup_orders.get_order(order_id)
    assert order is None, f"Order with ID {order_id} should no longer exist"

def test_fetch_all_shipments(setup_shipments):
    shipments = setup_shipments.get_shipments()
    assert isinstance(shipments, list), "Shipments should be returned as a list"
    assert len(shipments) > 0, "Shipment list should not be empty"

def test_fetch_shipment_by_id(setup_shipments):
    shipment_id = 1  # Adjust based on your test data
    shipment = setup_shipments.get_shipment(shipment_id)
    assert shipment is not None, f"Shipment with ID {shipment_id} should exist"
    assert shipment['id'] == shipment_id, f"Shipment ID should match {shipment_id}"

def test_create_shipment(setup_shipments):
    new_shipment = {
        "id": 5,  # Ensure this ID doesn't conflict with existing IDs
        "items": [{"item_id": "P001111", "amount": 10}],
        "created_at": "2024-01-01T12:00:00Z",
        "updated_at": "2024-01-01T12:00:00Z"
    }
    setup_shipments.add_shipment(new_shipment)
    assert setup_shipments.get_shipment(5) is not None, "Newly created shipment should exist"

def test_update_shipment_status(setup_shipments):
    shipment_id = 1  # Adjust based on your test data
    shipment = setup_shipments.get_shipment(shipment_id)
    assert shipment is not None, f"Shipment with ID {shipment_id} should exist"

    updated_shipment = shipment
    updated_shipment["status"] = "Delivered"  # Modify the shipment status
    setup_shipments.update_shipment(shipment_id, updated_shipment)
    updated_shipment = setup_shipments.get_shipment(shipment_id)  # Fetch updated shipment
    assert updated_shipment['status'] == "Delivered", "Shipment status should be updated"

def test_delete_shipment(setup_shipments):
    shipment_id = 2  # Adjust based on your test data
    setup_shipments.remove_shipment(shipment_id)
    shipment = setup_shipments.get_shipment(shipment_id)
    assert shipment is None, f"Shipment with ID {shipment_id} should no longer exist"
