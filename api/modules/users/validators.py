from pydantic import Annotated, Field
from pydantic.functional_validators import AfterValidator
import re

from config import UserData as UD

TELEGRAM_ID_PATTERN = (
    f'^\d{{{UD.MIN_LENGHT_TELEGRAM_ID},{UD.MAX_LENGHT_TELEGRAM_ID}}}$'
)

# -------------------
# ВАЛИДАТОРЫ
# -------------------
def validate_telegram_id(value: str) -> str:
    if not value.isdigit():
        raise ValueError('telegram id должен состоять из цифр')
    if (
        len(value) < UD.MIN_LENGHT_TELEGRAM_ID) or (
        len(value) > UD.MAX_LENGHT_TELEGRAM_ID):
        raise ValueError(
            f'telegram id должен быть не длиннее '
            f'{UD.MAX_LENGHT_TELEGRAM_ID} и не короче '
            f'{UD.MIN_LENGHT_TELEGRAM_ID}'
        )
    return value

def validate_cyrillic(value: str) -> str:
    if not re.match(r'^[А-Яа-яЁё\s\-]+$', value):
        raise ValueError(
            'ФИО должно содержать только кириллицу, пробелы и дефисы'
        )
    if len(value) < UD.MIN_LENGHT_NAME:
        raise ValueError('Имя/Фамилия слишком короткие')
    return value

def validate_phone(value: str) -> str:
    digits = re.sub(r'\D', '', value)
    if not digits.startswith('7') and not digits.startswith('8'):
        raise ValueError('Номер должен начинаться с 7 или 8')
    if len(digits) != 11:
        raise ValueError('Номер должен содержать 11 цифр')
    if not digits[1:].startswith('9'):
        raise ValueError('Код оператора должен начинаться с 9')
    return f'+7{digits[1:]}'

# -------------------
# АННОТАЦИИ
# -------------------
TelegramId = Annotated[
    str,
    Field(
        pattern=TELEGRAM_ID_PATTERN,
        description='Уникальный ID пользователя в Telegram (только цифры)',
        examples=['123456789']
    ),
    AfterValidator(validate_telegram_id)
]

CyrillicName = Annotated[
    str,
    Field(
        pattern=r'^[А-Яа-яЁё\s\-]+$',
        description=(f'Только кириллица, пробелы, дефисы. ' 
                     f'Минимум {UD.MIN_LENGHT_NAME} символов.'
        ),
        examples=['Иванов', 'Анна-Мария']
    ),
    AfterValidator(validate_cyrillic)
]

RussianPhoneNumber = Annotated[
    str,
    Field(
        pattern=(
            r'^(\+7|8)?\s?\(?9\d{2}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$'
        ),
        description=(f'Номер телефона в российском формате. '
                     f'Должен начинаться с 7 или 8, '
                     f'содержать 11 цифр, код оператора — с 9.'
        ),
        examples=['+79991234567', '8 (999) 123-45-67', '79991234567']
    ),
    AfterValidator(validate_phone)
]
