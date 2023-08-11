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
        orm_mode = True


class MessageBase(BaseModel):
    conversation_id: int
    user_id: int
    content: str


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    message_id: int
    sent_at: datetime
    user: UserBase

    class Config:
        from_attributes = True
        populate_by_name = True
        extra = "allow"
        orm_mode = True


class ParticipantBase(BaseModel):
    user_id: int
    is_owner: bool = False
    username: str


class ParticipantDetail(BaseModel):
    participant_id: int
    username: str
    is_owner: bool = False


class ParticipantCreate(ParticipantBase):
    pass


class Participant(ParticipantBase):
    participant_id: int
    conversation_id: int

    class Config:
        from_attributes = True
        orm_mode = True


class TokenData(BaseModel):
    username: Optional[str] = None


class LoginData(BaseModel):
    username: str
    password: str


class InvitationBase(BaseModel):
    conversation_id: int
    conversation_name: str  # Add this line
    inviting_user_id: int
    inviting_user_email: EmailStr  # Add this line
    invited_email: EmailStr


class InvitationCreate(InvitationBase):
    pass


class Invitation(InvitationBase):
    id: int
    token: str
    created_at: datetime
    used: bool

    class Config:
        orm_mode = True
