from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from routers import users, conversations, participants
import models
import schemas
import uvicorn
from database import get_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(users.router, prefix="/users")
# app.include_router(conversations.router)
# app.include_router(participants.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/conversations/", response_model=schemas.Conversation)
def create_conversation(conversation: schemas.ConversationCreate, db: Session = Depends(get_db)):
    db_conversation = models.Conversation(**conversation.model_dump())
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

def to_dict(model_instance):
    return {c.name: getattr(model_instance, c.name) for c in model_instance.__table__.columns}


@app.post("/conversations/{conversation_id}/participants", response_model=schemas.Participant)
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


@app.get("/conversations/{conversation_id}", response_model=schemas.Conversation)
def read_conversation(conversation_id: int, db: Session = Depends(get_db)):
    db_conversation = db.query(models.Conversation).filter(models.Conversation.conversation_id == conversation_id).first()
    if db_conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return db_conversation


@app.post("/conversations/{conversation_id}/messages", response_model=schemas.Message)
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


@app.get("/conversations/{conversation_id}/participants", response_model=List[schemas.Participant])
def read_participants(conversation_id: int, db: Session = Depends(get_db)):
    db_participants = db.query(models.Participant).filter(models.Participant.conversation_id == conversation_id).all()
    return db_participants

@app.get("/conversations/{conversation_id}/messages", response_model=List[schemas.Message])
def read_messages(conversation_id: int, db: Session = Depends(get_db)):
    db_messages = db.query(models.Message).filter(models.Message.conversation_id == conversation_id).all()
    return db_messages

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)