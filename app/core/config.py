from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    """Конфигурация настроек."""
    APP_TITLE: str = 'Кошачий благотворительный фонд'
    APP_DESCRIPTION: str = 'Наш сервис сделает жизнь кошек лучше!'
    DATABASE_URL: str = 'sqlite+aiosqlite:///./charity_fund.db'
    SECRET: str = 'SECRET'
    TOKEN_LIFETIME_SECONDS: int = 36000
    FIRST_SUPERUSER_EMAIL: Optional[EmailStr] = None
    FIRST_SUPERUSER_PASSWORD: Optional[str] = None
    # GoogleCloud info
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
