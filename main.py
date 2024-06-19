from flask import Flask, request, jsonify

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
    new_receipt = ReceiptSchema().load(request.get_json())
    receipt_id = new_receipt.id
    receipts[receipt_id] = new_receipt

    return jsonify(id=receipt_id)


@app.route("/receipts/<id>/points", methods=['GET'])
def get_receipt_points(id):
    receipt = receipts[id]
    return jsonify(points=receipt.points)


@app.route("/receipts/all", methods=['GET'])
def get_all_receipts():
    return receipts


if __name__ == "__main__":
    app.run()
