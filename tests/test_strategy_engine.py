from fastapi.testclient import TestClient
from strategy_engine.app.main import app

client = TestClient(app)


def test_list_strategies():
    data = {
        "name": "test",
        "indicators": [{"name": "ma", "weight": 1.0}]
    }
    client.post("/strategy", json=data)
    response = client.get("/strategies")
    assert response.status_code == 200
    assert response.json()["strategies"]
