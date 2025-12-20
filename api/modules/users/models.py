from enum import Enum as PyEnum

from api.database import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean


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
    Номер телефона для связи, Телеграм id, Ник в телеграме,
    Роль, Доступен ли сервис для пользователя.
    """

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    license_number = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.driver, nullable=False)
    telegram_id = Column(String, unique=True, nullable=False, index=True)
    telegram_name = Column(String, nullable=False)


class WhiteList(Base):
    """Доступ по Telegram_id.
    Таблица с telegram_id, имеющими доступ к сервису.
    """
    __tablename__ = 'white_list'

    telegram_id = Column(String, unique=True, primary_key=True, index=True)
