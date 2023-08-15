from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas
from typing import List
from database import get_db
import services.message_operations as message_operations

router = APIRouter()


@router.post(
    "/conversations/{conversation_id}/messages", response_model=schemas.Message
)
def create_message(
    message: schemas.MessageCreate, conversation_id: int, db: Session = Depends(get_db)
):
    return message_operations.create_new_message(message, conversation_id, db)


@router.get(
    "/conversations/{conversation_id}/messages", response_model=List[schemas.Message]
)
def read_messages(conversation_id: int, db: Session = Depends(get_db)):
    return message_operations.get_messages_for_conversation(conversation_id, db)
