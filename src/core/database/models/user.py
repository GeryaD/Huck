from datetime import datetime
from email.policy import default
from uuid import uuid4, UUID as uuid_type
from sqlalchemy import Index, text, Column, Integer, String, DateTime, ForeignKey, UUID, BINARY, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.mysql import VARCHAR

from src.core.database.models.base import Base


class User(Base):
    __tablename__ = "user"
    __table_args__ = (
        Index("email_index", "email"),
    )
    uuid = Column(VARCHAR(36), primary_key=True, default=text("uuid()"))
    email = Column(VARCHAR(255), nullable=False, unique=True)
    pwd_hash = Column(BINARY, nullable=False)
    reg_at = Column(DateTime, nullable=False, default=text("TIMEZONE('utc', now())"))
    active = Column(Boolean, nullable=False, server_default=text("TRUE"))
