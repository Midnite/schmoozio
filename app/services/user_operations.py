from sqlalchemy.orm import Session
from datetime import timedelta
import auth
import crud.users as crud
import re


def validate_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None


def validate_password(password: str) -> bool:
    return (
        len(password) >= 8 and
        any(char.isdigit() for char in password) and
        any(char.isupper() for char in password) and
        any(char.islower() for char in password) and
        any(char in "!@#$%^&*()_+{}:;<>,.?~" for char in password)
    )


def create_new_user(username: str, email: str, password: str, db: Session):
    if not validate_email(email):
        raise ValueError("Invalid email format")
    if not validate_password(password):
        raise ValueError("Password requirements not met")

    if crud.get_user_by_email(db, email):
        raise ValueError("Email already registered")

    hashed_password = auth.get_password_hash(password)
    return crud.create_user(db, username, email, hashed_password)


def get_user_conversations(db: Session, user_id: int):
    return crud.get_user_conversations(db, user_id)


def get_user_by_id(user_id: int, db: Session):
    return crud.get_user_by_id(db, user_id)


def authenticate_user(username: str, password: str, db: Session):
    user = crud.get_user_by_username(db, username)
    if not user:
        raise ValueError("Incorrect username")
    if not auth.verify_password(password, user.hashed_password):
        raise ValueError("Incorrect password")

    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.user_id,
    }
