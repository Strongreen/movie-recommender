from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import User
from app.schemas import UserCreate, UserRead

router = APIRouter()

@router.post("/")
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    db_user = User(**user.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user 


@router.get("/", response_model=list[UserRead])
def list_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users


@router.get("/{user_id}")
def get_user_id(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="O usuário não foi encontrado")
    return user



@router.delete("/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="O usuário não foi encontrado")
    session.delete(user)
    session.commit()
    return {"message": f"Usuário {user_id} deletado"}
