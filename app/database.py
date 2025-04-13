from sqlmodel import create_engine, Session, SQLModel
from typing import Generator

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator:
    with Session(engine) as session:
        yield session

