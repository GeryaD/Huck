import os
from pathlib import Path

from pydantic_settings import BaseSettings


class SettingsApp(BaseSettings):
    BASE_DIR: Path = Path(__file__).parent.parent
    PRIVATE_KEY_PATH: Path = BASE_DIR / "core" / "certs" / "jwt-private.pem"
    PUBLIC_KEY_PATH: Path = BASE_DIR / "core" / "certs" / "jwt-public.pem"
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "RS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 43200)  # заменить потом на 15
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = os.getenv("JWT_REFRESH_TOKEN_EXPIRE_MINUTES", 43_200)
    CHECK_EMAIL_DELIVERABILITY: bool = os.getenv("CHECK_EMAIL_DELIVERABILITY", False)


class SettingsDataBase(BaseSettings):
    MYSQL_ROOT_PASSWORD: str = os.getenv("MYSQL_ROOT_PASSWORD", "QQqq11!!")
    MYSQL_DATABASE: str = os.getenv("MYSQL_DATABASE", "huckparser")
    MYSQL_USER: str = os.getenv("MYSQL_USER", "huckparseruser")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "QQqq11!!")
    MYSQL_PORT: int = os.getenv("MYSQL_PORT", 3306)
    MYSQL_HOST: str = os.getenv("MYSQL_HOST", "db")
    # MYSQL_HOST: str = "localhost"
    MYSQL_DBMS: str = 'mysql'
    MYSQL_ENGINE: str = 'aiomysql'
    SQL_ECHO: bool = os.getenv("SQL_ECHO", True)
    MYSQL_URL: str = f'{MYSQL_DBMS}+{MYSQL_ENGINE}://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8'


class SettingsRedis(BaseSettings):
    REDIS_HOST: str = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT: int = os.getenv("REDIS_PORT", 5370)
    REDIS_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}"


class AccessType:
    neutral = "neutral"
    access = "access"
    refresh = "refresh"


ACCESS_TYPE = AccessType()
app = SettingsApp()
redis = SettingsRedis()
db = SettingsDataBase()
