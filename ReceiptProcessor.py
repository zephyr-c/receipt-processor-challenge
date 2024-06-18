import math
from datetime import date, time


class ReceiptProcessor:
    def __init__(self, receipt):
        self.retailer = receipt["retailer"]
        self.purchaseDate = date.fromisoformat(receipt["purchaseDate"])
        self.purchaseTime = time.fromisoformat(receipt["purchaseTime"])
        self.items = receipt["items"]
        self.total = float(receipt["total"])
        self.points = 0

        self.process_all()

    def process_name(self):
        """
        Adds 1 point for every alphanumeric character in retailer name.
        """
        for char in self.retailer:
            if char.isalnum():
                self.points += 1

    def process_total(self):
        """
        Adds 50 points if purchase total is a round dollar amount
        Adds 25 points if purchase total is a multiple of 0.25
        """
        if self.total % 1 == 0:
            self.points += 50
        if self.total % 0.25 == 0:
            self.points += 25

    def process_items(self):
        """
        Adds 5 points for every two items purchased
        Adds points for every item with a trimmed description length divisible by 3
        These points are equal to 20% of the item's price rounded up to the nearest integer
        """
        self.points += 5 * (len(self.items) // 2)
        for item in self.items:
            description, price = item.values()
            trimmed = description[:].strip()
            if len(trimmed) % 3 == 0:
                self.points += math.ceil(float(price) * 0.2)

    def process_date(self):
        """
        Adds 6 points if purchase date is odd
        """
        if self.purchaseDate.day % 2 == 1:
            self.points += 6

    def process_time(self):
        """
        Adds 10 points if purchase time is after 2pm and before 4pm
        """
        earliest_purchase = time(14, 0)
        latest_purchase = time(16, 0)
        if earliest_purchase < self.purchaseTime < latest_purchase:
            self.points += 10

    def process_all(self):
        """
        Calculates and adds all eligible points on receipt
        """
        self.process_name()
        self.process_date()
        self.process_time()
        self.process_items()
        self.process_total()
