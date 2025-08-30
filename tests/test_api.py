from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_no_input():
    resp = client.post("/api/process", data={})
    assert resp.status_code == 400

def test_text_input():
    resp = client.post("/api/process", data={'text': 'Gostaria de saber o status do chamado 123.'})
    assert resp.status_code == 200
    data = resp.json()
    assert 'category' in data
    assert 'suggested_response' in data
