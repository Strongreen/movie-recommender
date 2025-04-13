from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_rate_movie():
    user_response = client.post("/usuarios/", json={"name": "Rater"})
    assert user_response.status_code == 200
    user = user_response.json()
    assert user["name"] == "Rater"
    assert "id" in user

    movie_response = client.post("/filmes/", json={
        "title": "Rated Movie",
        "genre": "Action",
        "director": "Dir A",
        "actors": "Act A, Act B",
    })
    assert movie_response.status_code == 200
    movie = movie_response.json()
    assert movie["title"] == "Rated Movie"
    assert "id" in movie

    payload = {
        "user_id": user["id"],
        "movie_id": movie["id"],
        "score": 4.5
    }
    rating_response = client.post("/classificacoes/", json=payload)
    assert rating_response.status_code == 200
    rating = rating_response.json()
    assert rating["score"] == 4.5
    assert rating["user_id"] == user["id"]
    assert rating["movie_id"] == movie["id"]

    user_ratings_response = client.get(f"/classificacoes/usuarios/{user['id']}")
    assert user_ratings_response.status_code == 200
    user_ratings = user_ratings_response.json()
    assert isinstance(user_ratings, list)
    assert any(r["score"] == 4.5 and r["movie_id"] == movie["id"] for r in user_ratings)

    movie_ratings_response = client.get(f"/classificacoes/filmes/{movie['id']}")
    assert movie_ratings_response.status_code == 200
    movie_ratings = movie_ratings_response.json()
    assert isinstance(movie_ratings, list)
    assert any(r["score"] == 4.5 and r["user_id"] == user["id"] for r in movie_ratings)
