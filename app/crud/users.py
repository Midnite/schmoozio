from sqlalchemy.orm import Session
from app import models

def create_user(db: Session, username: str, email: str, hashed_password: str) -> models.User:
    db_user = models.User(username=username, email=email,
                          hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_conversations(db: Session, user_id: int):
    return (
        db.query(models.Conversation)
        .join(
            models.Participant,
            models.Participant.conversation_id == models.Conversation.conversation_id,
        )
        .filter(models.Participant.user_id == user_id)
        .all()
    )
