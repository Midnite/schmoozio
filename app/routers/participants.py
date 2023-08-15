from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import schemas
from database import get_db
import services.participant_operations as participant_operations

router = APIRouter()


@router.post(
    "/conversations/{conversation_id}/participants", response_model=schemas.Participant
)
def create_participant(
    participant: schemas.ParticipantCreate,
    conversation_id: int,
    db: Session = Depends(get_db),
):
    return participant_operations.create_participant_logic(
        participant, conversation_id, db
    )


@router.get(
    "/conversations/{conversation_id}/participants",
    response_model=List[schemas.Participant],
)
def read_participants(conversation_id: int, db: Session = Depends(get_db)):
    return participant_operations.read_participants_logic(conversation_id, db)
