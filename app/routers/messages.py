from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import schemas, models
from typing import List
from database import get_db

router = APIRouter()

@router.post("/conversations/{conversation_id}/messages", response_model=schemas.Message)
def create_message(
    message: schemas.MessageCreate, 
    conversation_id: int,
    db: Session = Depends(get_db)
):
    message_dict = message.model_dump()
    message_dict.pop("conversation_id", None)
    db_message = models.Message(**message_dict, conversation_id=conversation_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@router.get("/conversations/{conversation_id}/messages", response_model=List[schemas.Message])
def read_messages(conversation_id: int, db: Session = Depends(get_db)):
    db_messages = db.query(models.Message).filter(models.Message.conversation_id == conversation_id).all()
    return db_messages