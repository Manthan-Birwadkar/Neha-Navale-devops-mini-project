import pytest
from app.main import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home_endpoint(client):
    assert client.get("/").status_code == 200

def test_health_check(client):
    assert client.get("/health").status_code == 200

def test_calculate_addition(client):
    assert client.post("/api/calculate", json={"a": 15, "b": 25, "operation": "add"}).get_json()["result"] == 40

def test_calculate_division_by_zero(client):
    assert client.post("/api/calculate", json={"a": 10, "b": 0, "operation": "divide"}).status_code == 400
