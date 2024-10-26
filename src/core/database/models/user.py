from datetime import datetime
from email.policy import default
from uuid import uuid4, UUID as uuid_type
from sqlalchemy import Index, text, Column, Integer, String, DateTime, ForeignKey, UUID, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.mysql import VARCHAR, BINARY, TINYBLOB
from datetime import datetime

from src.core.database.models.base import Base


class User(Base):
    __tablename__ = "user"
    __table_args__ = (
        Index("email_index", "email"),
    )
    uuid = Column(VARCHAR(36), primary_key=True, default=uuid4().hex)
    email = Column(VARCHAR(255), nullable=False, unique=True)
    pwd_hash = Column(TINYBLOB, nullable=False)
    reg_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    active = Column(Boolean, nullable=False, server_default=text("TRUE"))
