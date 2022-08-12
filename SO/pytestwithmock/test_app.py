import pytest
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def replace_do_something():
    raise Exception()
    return


def test_read_main(monkeypatch: pytest.MonkeyPatch):
    response = client.get("/myroute")
    assert response.status_code == 200
    assert response.json() == {"hello": "world"}


def test_read_main_with_error(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr("app.do_something", replace_do_something)
    response = client.get("/myroute")
    assert response.status_code == 400
    assert response.json() == {"detail": "something went wrong"}
