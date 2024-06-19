import json


def test_hello_world(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert "Hello, World!" in response.text


def test_process_new_receipt(test_client):
    with open('examples/simple-receipt.json') as jsonfile:
        data = jsonfile.read()
    receipt_data = json.loads(data)
    response = test_client.post('/receipts/process', json=receipt_data)
    assert response.status_code == 200
    assert 'id' in response.json
    assert len(response.json['id']) == 36


def test_get_existing_points(test_client):
    receipt_id = '13b989e1-66f5-41cd-b71f-dffe26049cf4'
    response = test_client.get(f'receipts/{receipt_id}/points')
    assert response.json['points'] == 15

