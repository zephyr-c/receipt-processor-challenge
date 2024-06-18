import pytest
from ReceiptProcessor import ReceiptProcessor
from main import app

@pytest.fixture
def test_client():
    app.config.update({"TESTING": True})
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client

@pytest.fixture
def simple_receipt_data():
    return {
        "retailer": "Target",
        "purchaseDate": "2022-01-02",
        "purchaseTime": "14:13",
        "total": "1.25",
        "items": [
            {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
        ]
    }


@pytest.fixture
def morning_receipt_data():
    return {
        "retailer": "Walgreens",
        "purchaseDate": "2022-01-03",
        "purchaseTime": "08:13",
        "total": "2.65",
        "items": [
            {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
            {"shortDescription": "Dasani", "price": "1.40"}
        ]
    }


@pytest.fixture
def simple_receipt(simple_receipt_data):
    receipt = ReceiptProcessor(simple_receipt_data)
    receipt.points = 0
    return receipt


@pytest.fixture
def morning_receipt(morning_receipt_data):
    receipt = ReceiptProcessor(morning_receipt_data)
    receipt.points = 0
    return receipt
