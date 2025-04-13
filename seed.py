from sqlmodel import Session, select
from app.models import User, Movie, Rating
from app.database import engine
from random import sample, uniform, choice

def seed():
    with Session(engine) as session:
        existing_users = session.exec(select(User)).first()
        if existing_users:
            print("⚠️  O banco já foi populado. Pule ou limpe antes de rodar novamente.")
            return

        users = [User(name=f"User {i}") for i in range(1, 6)]
        session.add_all(users)
        session.commit()

        genres = ["Action", "Comedy", "Drama", "Horror", "Sci-Fi"]
        directors = ["Christopher Nolan", "Quentin Tarantino", "Steven Spielberg"]
        actors_list = [
            "Leonardo DiCaprio, Joseph Gordon-Levitt",
            "Brad Pitt, Margot Robbie",
            "Tom Hanks, Matt Damon",
            "Natalie Portman, Keanu Reeves"
        ]

        movies = [
            Movie(
                title=f"Movie {i}",
                genre=choice(genres),
                director=choice(directors),
                actors=choice(actors_list)
            )
            for i in range(1, 11)
        ]
        session.add_all(movies)
        session.commit()

        for user in users:
            rated_movies = sample(movies, k=min(len(movies), 5))
            for movie in rated_movies:
                rating = Rating(
                    user_id=user.id,
                    movie_id=movie.id,
                    score=round(uniform(1, 5), 1)
                )
                session.add(rating)

        session.commit()
        print(f"✅ Banco populado com: {len(users)} usuários, {len(movies)} filmes e avaliações geradas!")

if __name__ == "__main__":
    seed()
