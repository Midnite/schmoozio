from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app import models, schemas, database
from typing import List
import uuid

router = APIRouter()

@router.post("/", response_model=schemas.Invitation)
def send_invite(invitation: schemas.InvitationCreate, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == invitation.invited_email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No user found with this email.")
    
    conversation = db.query(models.Conversation).filter(models.Conversation.conversation_id == invitation.conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found.")
    
    inviting_user = db.query(models.User).filter(models.User.user_id == invitation.inviting_user_id).first()
    if not inviting_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inviting user not found.")

    db_invitation = models.Invitation(
        token=str(uuid.uuid4()),
        inviting_user_id=invitation.inviting_user_id,
        inviting_user_email=inviting_user.email,
        invited_email=invitation.invited_email,
        conversation_id=invitation.conversation_id,
        conversation_name=conversation.conversation_name
    )
    db.add(db_invitation)
    db.commit()
    db.refresh(db_invitation)
    return db_invitation


@router.get("/received/{user_id}", response_model=List[schemas.Invitation])
def get_received_invites(user_id: int, db: Session = Depends(database.get_db)):
    user_email = db.query(models.User.email).filter(models.User.user_id == user_id).first()
    if not user_email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    
    received_invitations = db.query(models.Invitation).filter(models.Invitation.invited_email == user_email.email).all()
    return received_invitations


@router.get("/sent/{user_id}", response_model=List[schemas.Invitation])
def get_sent_invites(user_id: int, db: Session = Depends(database.get_db)):
    # Get all invitations sent by the user
    sent_invitations = db.query(models.Invitation).filter(models.Invitation.inviting_user_id == user_id).all()
    return sent_invitations


@router.put("/{token}/invalidate", response_model=schemas.Invitation)
def invalidate_invite(token: str, db: Session = Depends(database.get_db)):
    db_invitation = db.query(models.Invitation).filter(models.Invitation.token == token).first()
    if not db_invitation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invitation not found.")
    
    db_invitation.used = True
    db.commit()
    db.refresh(db_invitation)
    return db_invitation

@router.put("/{token}/accept", response_model=schemas.Invitation)
def accept_invite(token: str, db: Session = Depends(database.get_db)):
    db_invitation = db.query(models.Invitation).filter(models.Invitation.token == token).first()
    if not db_invitation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invitation not found.")
    
    # Check if the user is already a participant in the conversation.
    user = db.query(models.User).filter(models.User.email == db_invitation.invited_email).first()
    existing_participant = db.query(models.Participant).filter(
        models.Participant.user_id == user.user_id,
        models.Participant.conversation_id == db_invitation.conversation_id
    ).first()

    if existing_participant:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is already a participant in this conversation.")
    
    db_participant = models.Participant(user_id=user.user_id, conversation_id=db_invitation.conversation_id)
    db.add(db_participant)
    db.commit()
    
    db_invitation.used = True
    db.commit()
    db.refresh(db_invitation)
    return db_invitation

@router.put("/{token}/decline", response_model=schemas.Invitation)
def decline_invite(token: str, db: Session = Depends(database.get_db)):
    db_invitation = db.query(models.Invitation).filter(models.Invitation.token == token).first()
    if not db_invitation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invitation not found.")
    
    db_invitation.used = True
    db.commit()
    db.refresh(db_invitation)
    return db_invitation
