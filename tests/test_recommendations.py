from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_recommendations():
    user1 = client.post("/usuarios/", json={"name": "User1"}).json()
    user2 = client.post("/usuarios/", json={"name": "User2"}).json()

    movie1 = client.post("/filmes/", json={
        "title": "Movie A",
        "genre": "Action",
        "director": "Dir X",
        "actors": "Actor 1, Actor 2"
    }).json()
    movie2 = client.post("/filmes/", json={
        "title": "Movie B",
        "genre": "Action",
        "director": "Dir X",
        "actors": "Actor 2, Actor 3"
    }).json()
    movie3 = client.post("/filmes/", json={
        "title": "Movie C",
        "genre": "Drama",
        "director": "Dir Y",
        "actors": "Actor 4, Actor 5"
    }).json()

    client.post("/classificacoes/", json={
        "user_id": user1["id"],
        "movie_id": movie1["id"],
        "score": 5.0
    })
    client.post("/classificacoes/", json={
        "user_id": user1["id"],
        "movie_id": movie2["id"],
        "score": 4.5
    })

    client.post("/classificacoes/", json={
        "user_id": user2["id"],
        "movie_id": movie1["id"],
        "score": 5.0
    })
    client.post("/classificacoes/", json={
        "user_id": user2["id"],
        "movie_id": movie3["id"],
        "score": 4.0
    })

    response = client.get(f"/classificacoes/{user1['id']}/recomendacoes")
    
    assert response.status_code == 200
    recommendations = response.json()
    assert isinstance(recommendations, list)

    recommended_ids = [movie["id"] for movie in recommendations]
    
    print("IDs recomendados:", recommended_ids)
    
    assert movie3["id"] in recommended_ids, f"O filme esperado: {movie3['id']} na lista de recomendados, mas não foi encontrado."

