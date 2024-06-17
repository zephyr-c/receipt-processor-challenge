'''
- 1 point for every alnum character in the retailer name
- 50 pts if total is round dollar with no cents
- 25 pts if total is multiple of 0.25
- 5 pts for every two items on the receipt
- If trimmed length of item description is a multiple of 3, multiply price by 0.2 and round up to nearest integer for points
- 6 pts if day in purchase date is odd
- 10 pts if time of purchase is after 2pm and before 4pm
'''
import math
from datetime import date, time


class Receipt:
    def __init__(self, receipt):
        self.retailer = receipt["retailer"]
        self.purchaseDate = date.fromisoformat(receipt["purchaseDate"])
        self.purchaseTime = time.fromisoformat(receipt["purchaseTime"])
        self.items = receipt["items"]
        self.total = float(receipt["total"])
        self.points = 0

        self.process_all()

    def process_name(self):
        print("processing name")
        for char in self.retailer:
            if char.isalnum():
                self.points += 1

    def process_total(self):
        if self.total % 1 == 0:
            self.points += 50
        if self.total % 0.25 == 0:
            self.points += 25

    def process_items(self):
        self.points += 5 * (len(self.items) // 2)
        for item in self.items:
            description, price = item.values()
            trimmed = description[:].strip()
            if len(trimmed) % 3 == 0:
                self.points += math.ceil(float(price) * 0.2)

    def process_date(self):
        if self.purchaseDate.day % 2 == 1:
            self.points += 6

    def process_time(self):
        earliest_purchase = time(14, 0)
        latest_purchase = time(16, 0)
        if earliest_purchase < self.purchaseTime < latest_purchase:
            self.points += 10

    def process_all(self):
        self.process_name()
        self.process_date()
        self.process_time()
        self.process_items()
        self.process_total()
