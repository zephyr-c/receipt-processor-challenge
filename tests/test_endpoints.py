import json


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
    response = test_client.get(f'/receipts/{receipt_id}/points')
    assert response.status_code == 200
    assert response.json['points'] == 15


def test_receipt_not_found(test_client):
    receipt_id = '111-2222-3333'
    response = test_client.get(f'/receipts/{receipt_id}/points')
    assert response.status_code == 404


def test_incomplete_receipt(test_client, invalid_receipt_data):
    response = test_client.post('/receipts/process', json=invalid_receipt_data)
    assert response.status_code == 400


def test_process_and_retrieve(test_client, simple_receipt_data):
    process_response = test_client.post('/receipts/process', json=simple_receipt_data)
    result_id = process_response.json['id']
    assert process_response.status_code == 200
    retrieve_response = test_client.get(f'/receipts/{result_id}/points')
    assert retrieve_response.status_code == 200
    assert 'points' in retrieve_response.json
    assert retrieve_response.json['points'] == 41
