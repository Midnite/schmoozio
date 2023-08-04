from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from typing import List
import bcrypt
import models
import os
import schemas
import uvicorn

load_dotenv()
app = FastAPI()
DATABASE_URL = os.getenv('DATABASE_URL')

# for running tests
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@app.get("/")
async def root():
    return {"message": "Hello World"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_password_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

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