from marshmallow import Schema, fields


class Item(object):
    def __init__(self, shortDescription, price):
        self.shortDescription = shortDescription
        self.price = price


class ItemSchema(Schema):
    shortDescription = fields.Str()
    price = fields.Float()
