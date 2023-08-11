from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from database import get_db

router = APIRouter()

def to_dict(model_instance):
    return {c.name: getattr(model_instance, c.name) for c in model_instance.__table__.columns}

@router.post("/conversations/{conversation_id}/participants", response_model=schemas.Participant)
def create_participant(
    participant: schemas.ParticipantCreate, 
    conversation_id: int,
    db: Session = Depends(get_db)
):
    # max 30 participants per conversation?
    count = db.query(models.Participant).filter(models.Participant.conversation_id == conversation_id).count()
    if count >= 30:
        raise HTTPException(status_code=400, detail="Conversation already has maximum number of participants")

    db_participant = models.Participant(**participant.model_dump(), conversation_id=conversation_id)
    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)
    return schemas.Participant(**to_dict(db_participant), id=db_participant.participant_id)


@router.get("/conversations/{conversation_id}/participants", response_model=List[schemas.Participant])
def read_participants(conversation_id: int, db: Session = Depends(get_db)):
    participants_with_users = (
        db.query(models.Participant, models.User.username)
        .join(models.User, models.Participant.user_id == models.User.user_id)
        .filter(models.Participant.conversation_id == conversation_id)
        .all()
    )

    return [
        schemas.Participant(**{
            **to_dict(participant),
            "username": username,
            "is_owner": participant.is_owner
        })
        for participant, username in participants_with_users
    ]

