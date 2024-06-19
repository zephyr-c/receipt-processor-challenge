from models.receipt import ReceiptSchema


class TestNamePoints:
    def test_name_points(self, simple_receipt):
        simple_receipt._process_name()
        assert simple_receipt.points == 6

    def test_name_with_space(self, simple_receipt):
        simple_receipt.retailer = "Pottery Barn"
        simple_receipt._process_name()
        assert simple_receipt.points == 11

    def test_name_with_numbers(self, simple_receipt):
        simple_receipt.retailer = "Rue21"
        simple_receipt._process_name()
        assert simple_receipt.points == 5


class TestPurchaseTotal:
    def test_multiple_of_25(self, simple_receipt):
        simple_receipt._process_total()
        assert simple_receipt.points == 25

    def test_whole_number(self, simple_receipt):
        simple_receipt.total = 2.00
        simple_receipt._process_total()
        assert simple_receipt.points == 75

    def test_odd_number(self, morning_receipt):
        morning_receipt._process_total()
        assert morning_receipt.points == 0


class TestItemsPurchased:
    def test_single_item(self, simple_receipt):
        simple_receipt._process_items()
        assert simple_receipt.points == 0

    def test_two_items(self, morning_receipt):
        morning_receipt._process_items()
        assert morning_receipt.points == 6


class TestPurchaseTimestamp:
    def test_odd_date(self, morning_receipt):
        morning_receipt._process_date()
        assert morning_receipt.points == 6

    def test_even_date(self, simple_receipt):
        simple_receipt._process_date()
        assert simple_receipt.points == 0

    def test_time_in_range(self, simple_receipt):
        simple_receipt._process_time()
        assert simple_receipt.points == 10

    def test_time_too_early(self, morning_receipt):
        morning_receipt._process_time()
        assert morning_receipt.points == 0


class TestTotalPoints:
    def test_simple_receipt(self, simple_receipt_data):
        processed_receipt = ReceiptSchema().load(data=simple_receipt_data)
        assert processed_receipt.points == 41

