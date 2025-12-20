# api/modules/user/schemas.py
from enum import Enum

from pydantic import BaseModel


class UserRole(str, Enum):
    """Роли пользователей."""
    admin = 'admin'
    grand_driver = 'grand_driver'
    driver = 'driver'


# -------------------
# Базовые схемы
# -------------------
class UserBase(BaseModel):
    first_name: str
    last_name: str
    license_number: str
    phone_number: str
    role: UserRole
    telegram_id: str
    telegram_name: str

    class Config:
        from_attributes = True

# -------------------
# Ответы
# -------------------
class UserResponse(UserBase):
    id: int
    access: bool

class Token(BaseModel):
    access_token: str
    token_type: str

# -------------------
# Запросы
# -------------------
class TelegramAuthRequest(BaseModel):
    telegram_id: str

class UserRegisterRequest(UserBase):
    pass

class WhiteListAdd(BaseModel):
    telegram_id: str