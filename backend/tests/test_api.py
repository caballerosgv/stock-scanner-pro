from fastapi.testclient import TestClient

from backend.api.app import app



def test_health_endpoint() -> None:
    client = TestClient(app)
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'



def test_provider_configs_crud() -> None:
    client = TestClient(app)

    list_response = client.get('/api/provider-configs')
    assert list_response.status_code == 200
    body = list_response.json()
    assert 'providers' in body
    assert any(item['provider'] == 'polygon' for item in body['providers'])

    save_response = client.put('/api/provider-configs/polygon', json={'api_key': 'abc-123'})
    assert save_response.status_code == 200
    assert save_response.json()['configured'] is True
