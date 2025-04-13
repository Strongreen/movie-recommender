from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import Movie
from app.schemas import MovieCreate, MovieRead

router = APIRouter()

@router.post("/", response_model=MovieRead)
def create_movie(movie: MovieCreate, session: Session = Depends(get_session)):
    db_movie = Movie(**movie.model_dump())
    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)
    return db_movie

@router.get("/", response_model=list[MovieRead])
def list_movies(session: Session = Depends(get_session)):
    movies = session.exec(select(Movie)).all()
    return movies

@router.get("/{movie_id}")
def list_ratings_by_movie(movie_id: int, session: Session = Depends(get_session)):
    movies = session.get(Movie, movie_id)
    if not movies:
        raise HTTPException(status_code=404, detail="O filme não foi encontrado")
    return movies

@router.delete("/{movie_id}")
def delete_user(movie_id: int, session: Session = Depends(get_session)):
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="O filme não foi encontrado")
    session.delete(movie)
    session.commit()
    return {"message": f"O filme {movie_id} deletado"}
