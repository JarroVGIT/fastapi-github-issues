from fastapi.testclient import TestClient
from app import app, get_value
import pytest


def test_dep():
    client = TestClient(app)
    app.dependency_overrides[get_value] = lambda: "test"

    assert client.get("/sub/").text == '"value: test"'