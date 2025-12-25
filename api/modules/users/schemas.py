import re
from enum import Enum

from pydantic import BaseModel

from api.modules.users.validators import (
    TelegramId, CyrillicName, RussianPhoneNumber)



class UserRole(str, Enum):
    """Роли пользователей."""
    admin = 'admin'
    grand_driver = 'grand_driver'
    driver = 'driver'


# -------------------
# БАЗОВЫЕ СХЕМЫ
# -------------------
class UserBase(BaseModel):
    first_name: CyrillicName
    last_name: CyrillicName
    license_number: str
    phone_number: RussianPhoneNumber
    telegram_id: TelegramId
    telegram_name: str

    class Config:
        from_attributes = True

# -------------------
# ОТВЕТЫ
# -------------------
class UserResponse(UserBase):
    id: int
    access: bool

class Token(BaseModel):
    access_token: str
    token_type: str

# -------------------
# ЗАПРОСЫ
# -------------------
class TelegramAuthRequest(BaseModel):
    telegram_id: TelegramId

class UserRegisterRequest(UserBase):
    pass

class WhiteListAdd(BaseModel):
    telegram_id: str
