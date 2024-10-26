from datetime import datetime

from pydantic import BaseModel, field_validator
from email_validator import validate_email

from src.core import settings


class RegUserSch(BaseModel):
    email: str
    pwd: str

    @field_validator("pwd")
    def check_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must have at least 8 characters")
        if len(value) > 255:
            raise ValueError("Password must be no more than 255 characters")
        if not any(c.isupper() for c in value):
            raise ValueError("Password must have at least one uppercase letter")
        if not any(c.islower() for c in value):
            raise ValueError("Password must have at least one lowercase letter")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must have at least one digit")
        return value

    @field_validator("email")
    def check_email(cls, value):
        try:
            value = validate_email(value, check_deliverability=settings.app.CHECK_EMAIL_DELIVERABILITY).normalized
            return value
        except ValueError:
            raise ValueError("Incorrect email")


class LoginUserSch(BaseModel):
    email: str
    pwd: str

    @field_validator("pwd")
    def check_password(cls, value):
        if (
                len(value) < 8 or
                len(value) > 255 or
                (not any(c.isupper() for c in value)) or
                (not any(c.islower() for c in value)) or
                (not any(c.isdigit() for c in value))
        ):
            raise ValueError("Incorrect email or password PW")
        return value

    @field_validator("email")
    def check_email(cls, value):
        try:
            value = validate_email(value, check_deliverability=settings.app.CHECK_EMAIL_DELIVERABILITY).normalized
            return value
        except ValueError:
            raise ValueError("Incorrect email or password E")


class OutUserSch(BaseModel):
    uuid: str
    email: str
    reg_at: datetime
    active: bool


class ORMUserSch(OutUserSch):
    pwd_hash: bytes
