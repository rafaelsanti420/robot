from fastapi.testclient import TestClient
from indicator_engine.app.main import app

client = TestClient(app)


def test_ma():
    data = {"prices": [1,2,3,4,5], "period": 3}
    response = client.post("/ma", json=data)
    assert response.status_code == 200
    assert response.json() == {"ma": 4.0}


def test_rsi():
    data = {"prices": [1,2,3,2,1,2,3], "period": 3}
    response = client.post("/rsi", json=data)
    assert response.status_code == 200
    assert "rsi" in response.json()


def test_ema():
    data = {"prices": [1,2,3,4,5,6], "period": 3}
    response = client.post("/ema", json=data)
    assert response.status_code == 200
    assert "ema" in response.json()
