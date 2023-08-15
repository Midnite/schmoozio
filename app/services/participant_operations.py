from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException


def to_dict(model_instance):
    return {
        c.name: getattr(model_instance, c.name)
        for c in model_instance.__table__.columns
    }


def create_participant_logic(
    participant: schemas.ParticipantCreate, conversation_id: int, db: Session
):
    count = (
        db.query(models.Participant)
        .filter(models.Participant.conversation_id == conversation_id)
        .count()
    )
    if count >= 30:
        raise HTTPException(
            status_code=400,
            detail="Conversation already has maximum number of participants",
        )

    db_participant = models.Participant(
        **participant.dict(), conversation_id=conversation_id
    )
    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)
    return schemas.Participant(
        **to_dict(db_participant), id=db_participant.participant_id
    )


def read_participants_logic(conversation_id: int, db: Session):
    participants_with_users = (
        db.query(models.Participant, models.User.username)
        .join(models.User, models.Participant.user_id == models.User.user_id)
        .filter(models.Participant.conversation_id == conversation_id)
        .all()
    )

    return [
        schemas.Participant(
            **{
                **to_dict(participant),
                "username": username,
                "is_owner": participant.is_owner,
            }
        )
        for participant, username in participants_with_users
    ]
