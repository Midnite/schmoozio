from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, database
from typing import List
import services.invitation_operations as invitation_operations

router = APIRouter()


@router.post("/", response_model=schemas.Invitation)
def send_invite(
    invitation: schemas.InvitationCreate, db: Session = Depends(database.get_db)
):
    return invitation_operations.send_invitation(invitation, db)


@router.get("/received/{user_id}", response_model=List[schemas.Invitation])
def get_received_invites(user_id: int, db: Session = Depends(database.get_db)):
    return invitation_operations.get_received_invitations(user_id, db)


@router.get("/sent/{user_id}", response_model=List[schemas.Invitation])
def get_sent_invites(user_id: int, db: Session = Depends(database.get_db)):
    return invitation_operations.get_sent_invitations(user_id, db)


@router.put("/{token}/invalidate", response_model=schemas.Invitation)
def invalidate_invite(token: str, db: Session = Depends(database.get_db)):
    return invitation_operations.invalidate_invitation(token, db)


@router.put("/{token}/accept", response_model=schemas.Invitation)
def accept_invite(token: str, db: Session = Depends(database.get_db)):
    return invitation_operations.accept_invitation(token, db)


@router.put("/{token}/decline", response_model=schemas.Invitation)
def decline_invite(token: str, db: Session = Depends(database.get_db)):
    return invitation_operations.decline_invitation(token, db)
