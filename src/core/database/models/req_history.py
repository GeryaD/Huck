from datetime import datetime
from uuid import uuid4, UUID as uuid_type
from sqlalchemy import Index, text, Column, Integer, String, DateTime, ForeignKey, UUID, BINARY, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.mysql import VARCHAR, TEXT

from src.core.database.models.base import Base


class RequestHistory(Base):
    __tablename__ = "request_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid_user = Column(VARCHAR(length=36), nullable=False)
    name = Column(VARCHAR(length=255), nullable=False)
    url_card = Column(TEXT, nullable=False)
    url_img = Column(TEXT, nullable=False)