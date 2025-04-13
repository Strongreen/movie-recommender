from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, conint

regex=r'^[a-zA-Z0-9À-ÿ, \-]+$'

class UserCreate(BaseModel):
    name: str = Field(..., pattern=regex, min_length=1, max_length=100)

    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "name": "Usuario"
            }
        }
    )

class UserRead(BaseModel):
    id: int
    name: str = Field(..., pattern=regex, min_length=1, max_length=100)

    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "name": "Usuario"
            }
        }
    )

class MovieCreate(BaseModel):
    title: str = Field(..., pattern=regex, min_length=1, max_length=100)
    genre: str = Field(..., pattern=regex, min_length=1, max_length=100)
    director: str = Field(..., pattern=regex, min_length=1, max_length=100)
    actors: str = Field(..., pattern=regex, min_length=1, max_length=100)

    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "title": "Filme",
                "genre": "Ação, Comédia",
                "director": "John Doe",
                "actors": "Ator1, Ator2"
            }
        }
    )

class MovieRead(BaseModel):
    id: int
    title: str = Field(..., pattern=regex, min_length=1, max_length=100)
    genre: str = Field(..., pattern=regex, min_length=1, max_length=100)
    director: str = Field(..., pattern=regex, min_length=1, max_length=100)
    actors: str = Field(..., pattern=regex, min_length=1, max_length=100)

    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "title": "Filme",
                "genre": "Ação, Comédia",
                "director": "John Doe",
                "actors": "Ator1, Ator2"
            }
        }
    )

class RatingCreate(BaseModel):
    user_id: int
    movie_id: int
    score: Optional[float] = conint(ge=1, le=5)

    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "score": 2,
            }
        }
    )

class RatingRead(BaseModel):
    user_id: int
    movie_id: int
    score: Optional[float] = conint(ge=1, le=5)

    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "score": 2,
            }
        }
    )

