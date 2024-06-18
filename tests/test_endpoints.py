import json

def test_hello_world(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert "Hello, World!" in response.text

def test_process_receipt(test_client):
    with open('examples/simple-receipt.json') as jsonfile:
        data = jsonfile.read()
    receipt_data = json.loads(data)
    response = test_client.post('/receipts/process', json=receipt_data)
    assert response.status_code == 200
    assert len(response.text) == 36
