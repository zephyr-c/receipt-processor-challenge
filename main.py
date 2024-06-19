from flask import Flask, request, jsonify, abort
import json

from models.receipt import ReceiptSchema

app = Flask(__name__)

receipts = {}

with open("examples/morning-receipt.json") as jsonfile:
    data = jsonfile.read()
    test_receipt = ReceiptSchema().load(json.loads(data))
    test_receipt.id = '13b989e1-66f5-41cd-b71f-dffe26049cf4'
    receipts[test_receipt.id] = test_receipt


@app.route("/receipts/process", methods=['POST'])
def process_receipt():
    try:
        new_receipt = ReceiptSchema().load(request.get_json())
        receipt_id = new_receipt.id
        receipts[receipt_id] = new_receipt

        return {"id": new_receipt.id}

    except TypeError:
        abort(400)


@app.route("/receipts/<receipt_id>/points", methods=['GET'])
def get_receipt_points(receipt_id):
    receipt = receipts.get(receipt_id)
    if not receipt:
        abort(404, "Invalid receipt ID")
    return {"points": receipt.points}


@app.route("/receipts/all", methods=['GET'])
def get_all_receipts():
    schema = ReceiptSchema()
    all_receipts = [schema.dump(receipt) for receipt in receipts.values()]
    return jsonify(all_receipts)


if __name__ == "__main__":
    app.run()
