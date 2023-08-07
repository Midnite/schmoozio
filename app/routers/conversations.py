from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import schemas, models
from database import get_db
import auth

router = APIRouter()

# @router.post("/", response_model=schemas.Conversation)
# def create_conversation(
#     conversation: schemas.ConversationCreate,
#     db: Session = Depends(get_db),
#     current_user: schemas.User = Depends(auth.get_current_user)
# ):
#     db_conversation = models.Conversation(**conversation.dict())
#     db.add(db_conversation)
#     db.commit()
#     db.refresh(db_conversation)

#     owner = models.Participant(user_id=current_user.user_id, conversation_id=db_conversation.conversation_id, is_owner=True)
#     db.add(owner)
#     db.commit()

#     db.refresh(db_conversation)
    
#     return schemas.Conversation.from_orm(db_conversation)

@router.post("/", response_model=schemas.Conversation)
def create_conversation(
    conversation: schemas.ConversationCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    # Check if conversation name is empty or just whitespace
    if not conversation.conversation_name or conversation.conversation_name.strip() == "":
        return JSONResponse(status_code=400, content={"detail": "Conversation name cannot be empty."})

    db_conversation = models.Conversation(**conversation.dict())
    
    try:
        db.add(db_conversation)
        db.commit()
        db.refresh(db_conversation)
        
        owner = models.Participant(user_id=current_user.user_id, conversation_id=db_conversation.conversation_id, is_owner=True)
        db.add(owner)
        db.commit()
        db.refresh(db_conversation)
        
        return schemas.Conversation.from_orm(db_conversation)
    except IntegrityError:
        db.rollback()  # Rollback the transaction in case of an error
        return JSONResponse(status_code=400, content={"detail": "A conversation with that name already exists."})


@router.get("/{conversation_id}", response_model=schemas.Conversation)
def read_conversation(conversation_id: int, db: Session = Depends(get_db)):
    db_conversation = db.query(models.Conversation).filter(models.Conversation.conversation_id == conversation_id).first()
    if db_conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return db_conversation