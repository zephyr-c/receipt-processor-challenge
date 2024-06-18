from flask import Flask, request, jsonify
from ReceiptProcessor import ReceiptProcessor
import uuid
import json

app = Flask(__name__)

receipts = {}

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/receipts/process", methods=['GET', 'POST'])
def process_receipt():
    new_receipt_data = request.get_json()
    new_receipt = ReceiptProcessor(new_receipt_data)
    receipt_id = str(uuid.uuid4())
    receipts[receipt_id] = new_receipt.points
    return receipt_id

@app.route("/receipts/<id>/points", methods=['GET'])
def get_receipt_points(id):
    print(receipts)
    # receipt = receipts[id]
    # return jsonify(points=receipt.points)
    return jsonify(points=receipts[id])

@app.route("/receipts/all", methods=['GET'])
def get_all_receipts():
    return receipts


