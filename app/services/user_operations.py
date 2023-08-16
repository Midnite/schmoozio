from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import schemas, models
from datetime import timedelta
import auth
import re


def validate_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if re.match(pattern, email):
        return True
    return False


def validate_password(password: str) -> bool:
    if (
        len(password) >= 8 and
        any(char.isdigit() for char in password) and
        any(char.isupper() for char in password) and
        any(char.islower() for char in password) and
        any(char in "!@#$%^&*()_+{}:;<>,.?~" for char in password)
    ):
        return True
    return False


def create_new_user(user: schemas.UserCreate, db: Session):
    if not validate_email(user.email):
        raise HTTPException(status_code=400, detail="Invalid email format")

    if not validate_password(user.password):
        raise HTTPException(
            status_code=400, detail="Password must be at least 8 characters, contain an uppercase letter, a lowercase letter, a digit, and a special character.")

    db_user = db.query(models.User).filter(
        models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        username=user.username, email=user.email, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_conversations(db: Session, current_user: schemas.User):
    return (
        db.query(models.Conversation)
        .join(
            models.Participant,
            models.Participant.conversation_id == models.Conversation.conversation_id,
        )
        .filter(models.Participant.user_id == current_user.user_id)
        .all()
    )


def get_user_by_id(user_id: int, db: Session):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def authenticate_user(data: schemas.LoginData, db: Session):
    user = auth.get_user(db, data.username)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not auth.verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.user_id,
    }
