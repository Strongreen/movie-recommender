from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_movie_success():
    response = client.post("/filmes/", json={
        "title": "Test Movie",
        "genre": "Drama",
        "director": "Director X",
        "actors": "Actor A, Actor B"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Movie"
    assert data["genre"] == "Drama"
    assert "id" in data


def test_get_all_movies():
    client.post("/filmes/", json={
        "title": "Movie 1",
        "genre": "Action",
        "director": "Director A",
        "actors": "Actor 1, Actor 2"
    })

    response = client.get("/filmes/")
    assert response.status_code == 200
    movies = response.json()
    assert isinstance(movies, list)
    assert any(movie["title"] == "Movie 1" for movie in movies)


def test_get_single_movie():
    create_response = client.post("/filmes/", json={
        "title": "Unique Movie",
        "genre": "Sci Fi",
        "director": "Director B",
        "actors": "Actor X, Actor Y"
    })
    movie_id = create_response.json()["id"]

    get_response = client.get(f"/filmes/{movie_id}")
    assert get_response.status_code == 200
    movie = get_response.json()
    assert movie["title"] == "Unique Movie"
    assert movie["id"] == movie_id


def test_delete_movie():
    create_response = client.post("/filmes/", json={
        "title": "Movie to Delete",
        "genre": "Horror",
        "director": "Director Z",
        "actors": "Actor Q, Actor W"
    })
    movie_id = create_response.json()["id"]

    delete_response = client.delete(f"/filmes/{movie_id}")
    assert delete_response.status_code == 200

    get_response = client.get(f"/filmes/{movie_id}")
    assert get_response.status_code == 404
