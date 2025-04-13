import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sqlmodel import Session, select
from app.models import Rating, Movie

def get_recommendations(user_id: int, session: Session):
    ratings = session.exec(select(Rating)).all()
    if not ratings:
        return []

    df = pd.DataFrame([{
        "user_id": r.user_id,
        "movie_id": r.movie_id,
        "score": r.score
    } for r in ratings])

    rating_matrix = df.pivot_table(index='user_id', columns='movie_id', values='score').fillna(0)

    if user_id not in rating_matrix.index:
        return []

    cosine_sim = cosine_similarity(rating_matrix)
    user_index = rating_matrix.index.tolist().index(user_id)
    user_similarities = cosine_sim[user_index]

    similar_users = {
        other_id: user_similarities[i]
        for i, other_id in enumerate(rating_matrix.index)
        if other_id != user_id and user_similarities[i] > 0
    }

    if not similar_users:
        return []

    user_movies = set(df[df.user_id == user_id].movie_id)
    candidate_scores = {}

    movies = session.exec(select(Movie)).all()
    movie_info = {movie.id: (movie.genre, movie.director, movie.actors.split(", ")) for movie in movies}

    for other_user_id, similarity in similar_users.items():
        other_user_movies = df[df.user_id == other_user_id]
        for _, row in other_user_movies.iterrows():
            if row.movie_id in user_movies:
                continue

            if row.movie_id not in candidate_scores:
                candidate_scores[row.movie_id] = 0

            candidate_scores[row.movie_id] += row.score * similarity

            movie = movie_info.get(row.movie_id)
            if movie:
                user_movie_info = [movie_info[m] for m in user_movies if m in movie_info]
                if any(movie[0] == info[0] for info in user_movie_info):
                    candidate_scores[row.movie_id] += 0.5
                if any(movie[1] == info[1] for info in user_movie_info):
                    candidate_scores[row.movie_id] += 0.5
                if any(actor in movie[2] for info in user_movie_info for actor in info[2]):
                    candidate_scores[row.movie_id] += 0.5

    if not candidate_scores:
        return []

    sorted_movies = sorted(candidate_scores.items(), key=lambda x: x[1], reverse=True)
    top_movie_ids = [movie_id for movie_id, _ in sorted_movies]

    recommended_movies = session.exec(
        select(Movie).where(Movie.id.in_(top_movie_ids))
    ).all()

    recommended_movies.sort(key=lambda movie: top_movie_ids.index(movie.id))
    return recommended_movies
