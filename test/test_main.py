from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_read_employees_bad_token():
    response = client.get(
        "/employees",
        headers={
            "WWW-Authenticate": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTY0ODE3NTAyNX0.AjUh6_Uc9TcWtk9XiULj1_LjVP6sc0_l4jNlD493nuY"
        },
    )
    assert response.status_code == 401
