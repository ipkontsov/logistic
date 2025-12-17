# api/modules/user/schemas.py
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class UserRole(str, Enum):
    admin = 'admin'
    grand_driver = 'grand_driver'
    driver = 'driver'


# ------------------------------------------------------------
# 1. Резервирование Telegram ID (только для админа/старшего водителя)
# ------------------------------------------------------------
class TelegramAccountReserve(BaseModel):
    telegram_id: str
    telegram_name: str


# ------------------------------------------------------------
# 2. Данные профиля для регистрации
# ------------------------------------------------------------
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    license_number: str
    phone_number: str
    role: UserRole = UserRole.driver


# ------------------------------------------------------------
# 3. Полный запрос на регистрацию
# ------------------------------------------------------------
class UserRegisterRequest(BaseModel):
    telegram_id: str
    telegram_name: str
    user: UserCreate


# ------------------------------------------------------------
# 4. Ответ: Telegram-аккаунт (без профиля)
# ------------------------------------------------------------
class TelegramAccountResponse(BaseModel):
    telegram_id: str
    telegram_name: str

    class Config:
        from_attributes = True


# ------------------------------------------------------------
# 5. Ответ: Профиль пользователя
# ------------------------------------------------------------
class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    license_number: str
    phone_number: str
    role: UserRole

    class Config:
        from_attributes = True


# ------------------------------------------------------------
# 6. Полный ответ: профиль + (опционально) telegram
# ------------------------------------------------------------
class FullUserResponse(BaseModel):
    user: UserResponse
    telegram_account: Optional[TelegramAccountResponse] = None


# ------------------------------------------------------------
# 7. Аутентификация
# ------------------------------------------------------------
class TelegramAuthRequest(BaseModel):
    telegram_id: str


class Token(BaseModel):
    access_token: str
    token_type: str
