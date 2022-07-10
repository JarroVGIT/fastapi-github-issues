from fastapi import HTTPException
import app
from fastapi.testclient import TestClient
import requests
from pytest_mock import MockerFixture

client = TestClient(app.app)

def test_read_main():
    response = client.get("/hello")
    assert response.json() == {"msg":"Hello World"}
    assert response.status_code == 200

def get_value_raise():
    raise requests.exceptions.HTTPError()

def test_errors(mocker: MockerFixture):
    mocker.patch("app.get_value", get_value_raise)
    response = client.get("/hello")
    assert response.status_code == 400
    assert response.json() == {"detail": "error occured"}
