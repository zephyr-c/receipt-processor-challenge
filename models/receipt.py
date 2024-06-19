from marshmallow import Schema, fields, post_load
from datetime import time
import uuid
import math

from models.item import ItemSchema


class Receipt(object):
    def __init__(self, retailer, purchaseDate, purchaseTime, items, total):
        self.id = str(uuid.uuid4())
        self.retailer = retailer
        self.purchaseDate = purchaseDate
        self.purchaseTime = purchaseTime
        self.items = items
        self.total = total
        self.points = 0

        self.process_all()

    def _process_name(self):
        """
        Adds 1 point for every alphanumeric character in retailer name.
        """
        for char in self.retailer:
            if char.isalnum():
                self.points += 1

    def _process_total(self):
        """
        Adds 50 points if purchase total is a round dollar amount
        Adds 25 points if purchase total is a multiple of 0.25
        """
        if self.total % 1 == 0:
            self.points += 50
        if self.total % 0.25 == 0:
            self.points += 25

    def _process_items(self):
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

    def _process_date(self):
        """
        Adds 6 points if purchase date is odd
        """
        if self.purchaseDate.day % 2 == 1:
            self.points += 6

    def _process_time(self):
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
        self._process_name()
        self._process_date()
        self._process_time()
        self._process_items()
        self._process_total()


class ReceiptSchema(Schema):
    id = fields.Str()
    retailer = fields.Str()
    purchaseDate = fields.Date()
    purchaseTime = fields.Time()
    items = fields.List(fields.Nested(ItemSchema))
    total = fields.Float()
    points = fields.Int()

    @post_load
    def make_receipt(self, data, **kwargs):
        return Receipt(**data)
