from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Rating(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
    movie_id: Optional[int] = Field(default=None, foreign_key="movie.id", primary_key=True)
    score: float
    user: Optional["User"] = Relationship(back_populates="ratings")
    movie: Optional["Movie"] = Relationship(back_populates="ratings")

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    ratings: List[Rating] = Relationship(back_populates="user")

class Movie(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    genre: str
    director: str
    actors: str
    ratings: List[Rating] = Relationship(back_populates="movie")
