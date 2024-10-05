# app/dao/chat.py

from sqlalchemy.orm import Session
from app.models.chat import ChatSession, ChatMessage
from app.schemas.chat import ChatSessionCreate, ChatMessageCreate
import uuid
from datetime import datetime

class ChatDAO:
    @staticmethod
    def create_session(db: Session):
        session_id = str(uuid.uuid4())
        db_session = ChatSession(session_id=session_id)
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        return db_session

    @staticmethod
    def get_session_by_id(db: Session, session_id: str):
        return db.query(ChatSession).filter(ChatSession.session_id == session_id).first()

    @staticmethod
    def create_message(db: Session, message: ChatMessageCreate):
        db_message = ChatMessage(
            sender=message.sender,
            content=message.content,
            message_type=message.message_type,
            session_id=1,  # Replace with actual session logic
            created_at=datetime.utcnow()
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message  # Return the full ChatMessage, which includes the ID, session_id, and created_at


    @staticmethod
    def get_chat_history(db: Session, session_id: int, limit: int = 10):
        return db.query(ChatMessage).filter(ChatMessage.id == session_id).order_by(ChatMessage.created_at.desc()).limit(limit).all()
