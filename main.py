from flask import Flask, request, jsonify
from ReceiptProcessor import ReceiptProcessor
import uuid

from models.receipt import ReceiptSchema

app = Flask(__name__)

receipts = {
    '13b989e1-66f5-41cd-b71f-dffe26049cf4': {'points': 35}
}


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/receipts/process", methods=['GET', 'POST'])
def process_receipt():
    schema = ReceiptSchema()
    new_receipt_data = request.get_json()
    processed_receipt = ReceiptProcessor(new_receipt_data)
    new_receipt = schema.dump(processed_receipt)
    receipt_id = str(uuid.uuid4())
    receipts[receipt_id] = new_receipt

    return jsonify(id=receipt_id)


@app.route("/receipts/<id>/points", methods=['GET'])
def get_receipt_points(id):
    receipt = receipts[id]
    return jsonify(points=receipt['points'])
    # return jsonify(points=receipts[id])


@app.route("/receipts/all", methods=['GET'])
def get_all_receipts():
    return receipts


