from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app import schemas
from typing import List
from database import get_db
import auth
import services.user_operations as user_operations

router = APIRouter()


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = user_operations.create_new_user(
            user.username, user.email, user.password, db)
        return schemas.User.from_orm(db_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/conversations", response_model=List[schemas.Conversation])
def list_user_conversations(db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    return user_operations.get_user_conversations(db, current_user.user_id)


@router.get("/me", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(auth.get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_operations.get_user_by_id(user_id, db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.User.from_orm(db_user)


@router.post("/token")
def login_for_access_token(data: schemas.LoginData = Body(...), db: Session = Depends(get_db)):
    return user_operations.authenticate_user(data.username, data.password, db)
