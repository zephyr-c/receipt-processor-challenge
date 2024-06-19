from marshmallow import Schema, fields, post_load
import uuid
import math

from models.item import ItemSchema


class Receipt(object):
    def __init__(self, retailer, purchaseDate, purchaseTime, items, total, points):
        self._id = uuid.uuid4()
        self.retailer = retailer
        self.purchaseDate = purchaseDate
        self.purchaseTime = purchaseTime
        self.items = items
        self.total = total
        self.points = 0


class ReceiptSchema(Schema):
    _id = fields.Str()
    retailer = fields.Str()
    purchaseDate = fields.Date()
    purchaseTime = fields.Time()
    items = fields.List(fields.Nested(ItemSchema))
    total = fields.Float()
    points = fields.Int()
