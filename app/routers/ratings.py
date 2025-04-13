from fastapi import APIRouter, Depends, HTTPException
from app.database import engine
from sqlmodel import Session, select
from app.database import get_session
from app.models import Rating, User, Movie
from app.schemas import MovieRead, RatingCreate, RatingRead
from app.recommender import get_recommendations

router = APIRouter()

@router.post("/", response_model=RatingRead)
def rate_movie(rating: RatingCreate):
    if rating.score is None:
        raise HTTPException(status_code=400, detail="É necessário fornecer uma avaliação.")
    
    with Session(engine) as session:
        db_rating = Rating(**rating.model_dump())
        session.add(db_rating)
        session.commit()
        session.refresh(db_rating)
        return db_rating


@router.get("/{user_id}/recomendacoes", response_model=list[MovieRead])
def get_user_recommendations(user_id: int, session: Session = Depends(get_session)):
    return get_recommendations(user_id, session)


@router.get("/usuarios/{user_id}")
def list_ratings_by_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="O usuário não foi encontrado")
    ratings = session.exec(select(Rating).where(Rating.user_id == user_id)).all()
    return ratings

@router.get("/filmes/{movie_id}")
def list_ratings_by_movie(movie_id: int, session: Session = Depends(get_session)):
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="O filme não foi encontrado")
    ratings = session.exec(select(Rating).where(Rating.movie_id == movie_id)).all()
    return ratings
