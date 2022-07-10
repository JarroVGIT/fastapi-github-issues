from app import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_empty_list_invalid():
    response = client.post("/query", json=[])
    assert response.status_code == 422

def test_empty_list():
    response = client.post("/query", json=[])
    assert response.json() == []

def test_empty_list_does_not_mutate_to_dict():
    response = client.post("/query", json=[])
    assert response.json() != {}

def test_non_empty_list():
    response = client.post("/query", json=[1,2,3])
    assert response.json() == {[1,2,3]}
