from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas
from typing import List
from database import get_db
import services.message_operations as message_operations
from app.socketio_manager import sio

router = APIRouter()


@sio.on('connect', namespace='/')
@sio.event
async def connect(sid, environ, auth):
    print("Client connected:", sid)


@sio.event
async def disconnect(sid):
    print("Client disconnected:", sid)


@sio.event
async def join_room(sid, conversation_id):
    sio.enter_room(sid, conversation_id)
    print("Rooms socket is in:", sio.rooms(sid))
    print("conversation_id, sid", conversation_id, sid)


@sio.event
async def leave_room(sid, conversation_id):
    sio.leave_room(sid, conversation_id)
    print(f"Socket {sid} left room {conversation_id}")


@router.post("/conversations/{conversation_id}/messages", response_model=schemas.Message)
async def create_message(message: schemas.MessageCreate, conversation_id: int, db: Session = Depends(get_db)):
    message_data = message_operations.create_new_message(
        message, conversation_id, db)
    formatted_message = {
        "message_id": str(message_data.message_id),
        "user": {"username": message_data.user.username},
        "content": message_data.content
    }
    await sio.emit("new_message", formatted_message, room=conversation_id)
    return message_data


@router.get("/conversations/{conversation_id}/messages", response_model=List[schemas.Message])
def read_messages(conversation_id: int, db: Session = Depends(get_db)):
    return message_operations.get_messages_for_conversation(conversation_id, db)
