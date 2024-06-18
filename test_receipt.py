import pytest
from ReceiptProcessor import ReceiptProcessor

@pytest.fixture
def simple_receipt_data():
    return {
        "retailer": "Target",  # 6pts for characters in name
        "purchaseDate": "2022-01-02",
        "purchaseTime": "14:13",  # 10pts for purchase time after 2pm and before 4pm
        "total": "1.25",  # 25 points for multiple of 0.25
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


class TestNamePoints:
    def test_name_points(self, simple_receipt):
        simple_receipt.process_name()
        assert simple_receipt.points == 6

    def test_name_with_space(self, simple_receipt):
        simple_receipt.retailer = "Pottery Barn"
        simple_receipt.process_name()
        assert simple_receipt.points == 11

    def test_name_with_numbers(self, simple_receipt):
        simple_receipt.retailer = "Rue21"
        simple_receipt.process_name()
        assert simple_receipt.points == 5

class TestPurchaseTotal:
    def test_multiple_of_25(self, simple_receipt):
        simple_receipt.process_total()
        assert simple_receipt.points == 25

    def test_whole_number(self, simple_receipt):
        simple_receipt.total = 2.00
        simple_receipt.process_total()
        assert simple_receipt.points == 75

    def test_odd_number(self, morning_receipt):
        morning_receipt.process_total()
        assert morning_receipt.points == 0

class TestItemsPurchased:
    def test_single_item(self, simple_receipt):
        simple_receipt.process_items()
        assert simple_receipt.points == 0

    def test_two_items(self, morning_receipt):
        morning_receipt.process_items()
        assert morning_receipt.points == 6

class TestPurchaseTimestamp:
    def test_odd_date(self, morning_receipt):
        morning_receipt.process_date()
        assert morning_receipt.points == 6

    def test_even_date(self, simple_receipt):
        simple_receipt.process_date()
        assert simple_receipt.points == 0

    def test_time_in_range(self, simple_receipt):
        simple_receipt.process_time()
        assert simple_receipt.points == 10

    def test_time_too_early(self, morning_receipt):
        morning_receipt.process_time()
        assert morning_receipt.points == 0


class TestTotalPoints:
    def test_simple_receipt(self, simple_receipt_data):
        processed_receipt = ReceiptProcessor(simple_receipt_data)
        assert processed_receipt.points == 41

