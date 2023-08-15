from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app import schemas
from database import get_db
from typing import List
import auth
import services.conversation_operations as conversation_operations


router = APIRouter()


@router.post("/", response_model=schemas.Conversation)
def create_conversation(
    conversation: schemas.ConversationCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user),
):
    return conversation_operations.create_new_conversation(
        conversation, db, current_user
    )


@router.get(
    "/{conversation_id}/participants", response_model=List[schemas.ParticipantDetail]
)
def get_participants_for_conversation(
    conversation_id: int, db: Session = Depends(get_db)
):
    return conversation_operations.get_participants(conversation_id, db)


@router.get("/{conversation_id}", response_model=schemas.Conversation)
def read_conversation(conversation_id: int, db: Session = Depends(get_db)):
    db_conversation = conversation_operations.get_conversation(conversation_id, db)
    if db_conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return db_conversation
