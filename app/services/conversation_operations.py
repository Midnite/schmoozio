from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app import schemas, models


def create_new_conversation(
    conversation: schemas.ConversationCreate, db: Session, current_user: schemas.User
):
    if (
        not conversation.conversation_name
        or conversation.conversation_name.strip() == ""
    ):
        return JSONResponse(
            status_code=400, content={"detail": "Conversation name cannot be empty."}
        )

    db_conversation = models.Conversation(**conversation.dict())
    db.add(db_conversation)

    owner = models.Participant(
        user_id=current_user.user_id,
        conversation_id=db_conversation.conversation_id,
        is_owner=True,
    )
    db.add(owner)

    try:
        db.commit()
        db.refresh(db_conversation)
        return schemas.Conversation.from_orm(db_conversation)
    except IntegrityError:
        db.rollback()
        return JSONResponse(
            status_code=400,
            content={"detail": "A conversation with that name already exists."},
        )


def get_participants(conversation_id: int, db: Session):
    participants_with_users = (
        db.query(
            models.Participant.participant_id,
            models.User.username,
            models.Participant.is_owner,
        )
        .join(models.User, models.User.user_id == models.Participant.user_id)
        .filter(models.Participant.conversation_id == conversation_id)
        .all()
    )

    return [
        {"participant_id": item[0], "username": item[1], "is_owner": item[2]}
        for item in participants_with_users
    ]


def get_conversation(conversation_id: int, db: Session):
    return (
        db.query(models.Conversation)
        .filter(models.Conversation.conversation_id == conversation_id)
        .first()
    )
