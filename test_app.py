from app import app

def test_home():
    client = app.test_client()
    r = client.get("/")
    assert r.status_code == 200
    assert b"Task Tracker" in r.data

def test_health():
    client = app.test_client()
    r = client.get("/health")
    assert r.get_json()["status"] == "ok"