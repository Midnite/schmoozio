from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
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
    message_dict = message.dict()
    message_dict.pop("conversation_id", None)
    db_message = models.Message(**message_dict, conversation_id=conversation_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    db.refresh(db_message.user)

    user_data = {
        "username": db_message.user.username,
        "email": db_message.user.email
    }
    message_data = {
        "conversation_id": db_message.conversation_id,
        "user_id": db_message.user_id,
        "content": db_message.content,
        "message_id": db_message.message_id,
        "sent_at": db_message.sent_at,
        "user": user_data
    }
    
    return schemas.Message(**message_data)

@router.get("/conversations/{conversation_id}/messages", response_model=List[schemas.Message])
def read_messages(conversation_id: int, db: Session = Depends(get_db)):
    db_messages = (
        db.query(models.Message)
        .options(joinedload(models.Message.user))
        .filter(models.Message.conversation_id == conversation_id)
        .order_by(models.Message.sent_at)
        .all()
    )
    
    # Manual serialization because pydantic is weird
    serialized_messages = []
    for message_orm in db_messages:
        user_data = {
            "username": message_orm.user.username,
            "email": message_orm.user.email
        }
        message_data = {
            "conversation_id": message_orm.conversation_id,
            "user_id": message_orm.user_id,
            "content": message_orm.content,
            "message_id": message_orm.message_id,
            "sent_at": message_orm.sent_at,
            "user": user_data
        }
        serialized_message = schemas.Message(**message_data)
        serialized_messages.append(serialized_message)
    
    return serialized_messages


    


