# app/schemas/chat.py

from datetime import datetime
from typing import List
from pydantic import BaseModel

class ChatMessageBase(BaseModel):
    sender: str
    content: str
    message_type: str  # 'user' or 'bot'

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessage(ChatMessageBase):
    id: int
    session_id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Use this instead of 'orm_mode = True'

class ChatSessionBase(BaseModel):
    pass

class ChatSessionCreate(ChatSessionBase):
    pass

class ChatSession(ChatSessionBase):
    id: int
    session_id: str
    created_at: datetime
    messages: List[ChatMessage] = []

    class Config:
        from_attributes = True  # Use this instead of 'orm_mode = True'

