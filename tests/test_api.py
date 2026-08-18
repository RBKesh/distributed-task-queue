from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_submit_task():
    res = client.post("/tasks", json={"task_type": "fibonacci", "payload": {"n": 10}})
    assert res.status_code == 200
    assert "task_id" in res.json()

def test_invalid_task_type():
    res = client.post("/tasks", json={"task_type": "hax0r", "payload": {}})
    assert res.status_code == 400

def test_get_task_status():
    res = client.post("/tasks", json={"task_type": "fibonacci", "payload": {"n": 5}})
    task_id = res.json()["task_id"]
    
    res2 = client.get(f"/tasks/{task_id}")
    assert res2.status_code == 200
    assert "status" in res2.json()
