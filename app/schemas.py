from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    user_id: int
    created_at: datetime
    class Config:
        from_attributes = True
        orm_mode = True
        
class ConversationBase(BaseModel):
    conversation_name: str

class ConversationCreate(ConversationBase):
    pass

class Conversation(ConversationBase):
    conversation_id: int
    created_at: datetime
    class Config:
        from_attributes = True

class MessageBase(BaseModel):
    conversation_id: int
    user_id: int
    content: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    message_id: int
    sent_at: datetime
    class Config:
        from_attributes = True
        populate_by_name = True

class ParticipantBase(BaseModel):
    user_id: int
    is_owner: bool = False

class ParticipantCreate(ParticipantBase):
    pass

class Participant(ParticipantBase):
    id: int
    conversation_id: int
    
    class Config:
        from_attributes = True

class TokenData(BaseModel):
    username: Optional[str] = None
    
class LoginData(BaseModel):
    username: str
    password: str
