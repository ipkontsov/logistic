from enum import Enum as PyEnum

from api.database import Base
from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class UserRole(PyEnum):
    """Роли пользователей:
    Администратор, Воитель, Старший водитель.
    """

    admin = 'admin'
    driver = 'driver'
    grand_driver = 'grand_driver'


class User(Base):
    """Модель пользователя c полями:
    Идентификационный номер, Имя, Фамилия, Номер водительских прав,
    Номер телефона для связи, Телеграм id, Ник в телеграме, Роль.
    """

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    license_number = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.driver, nullable=False)

    telegram_account = relationship(
        'TelegramAccount',
        back_populates='user',
        uselist=False
    )


class TelegramAccount(Base):
    """База допущенных Telegram_id"""

    __tablename__ = 'telegram_account'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, nullable=False, index=True)
    telegram_name = Column(String, nullable=False)

    user_id = Column(
        Integer,
        ForeignKey('user.id', ondelete='SET NULL'),
        unique=True,
        nullable=True
    )
    user = relationship(
        'User', back_populates='telegram_account'
    )
