from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user_success():
    response = client.post("/usuarios/", json={"name": "TestUser"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "TestUser"
    assert "id" in data


def test_get_all_users():
    client.post("/usuarios/", json={"name": "User1"})

    response = client.get("/usuarios/")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert any(user["name"] == "User1" for user in users)


def test_get_single_user():
    create_response = client.post("/usuarios/", json={"name": "UniqueUser"})
    user_id = create_response.json()["id"]

    get_response = client.get(f"/usuarios/{user_id}")
    assert get_response.status_code == 200
    user = get_response.json()
    assert user["id"] == user_id
    assert user["name"] == "UniqueUser"


def test_delete_user():
    create_response = client.post("/usuarios/", json={"name": "ToDelete"})
    user_id = create_response.json()["id"]

    delete_response = client.delete(f"/usuarios/{user_id}")
    assert delete_response.status_code == 200

    get_response = client.get(f"/usuarios/{user_id}")
    assert get_response.status_code == 404
