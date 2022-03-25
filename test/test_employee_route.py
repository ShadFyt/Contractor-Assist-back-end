from fastapi.testclient import TestClient


from ..main import app


client = TestClient(app)


def test_read_employees():
    response = client.get("/employees")
    assert response.status_code == 200
