from pydantic import Annotated, Field
from pydantic.functional_validators import AfterValidator
import re

from config import settings


# -------------------
# ПАТТЕРНЫ
# -------------------
TELEGRAM_ID_PATTERN = (
    f'^\d{{{settings.MIN_LENGTH_TELEGRAM_ID},'
    f'{settings.MAX_LENGTH_TELEGRAM_ID}}}$'
)
CYRILLIC_NAME_PATTERN = r'^[А-Яа-яЁё\s\-]+$'
RUSSIAN_PHONE_PATTERN = (
    r'^(\+?7|8)'                 # Код страны: +7, 7 или 8
    r'(?:\s|-)?'                 # Не захватывающий опциональный разделитель
    r'(?:\(9\d{2}\)|9\d{2})'     # Код оператора: (9XX) или 9XX
    r'(?:[\s\-])?'               # Не захватывающий разделитель
    r'\d{3}'                     # 3 цифры
    r'(?:[\s\-])?'               # Не захватывающий разделитель
    r'\d{2}'                     # 2 цифры
    r'(?:[\s\-])?'               # Не захватывающий разделитель
    r'\d{2}$'                    # 2 цифры + конец строки
)

# -------------------
# ВАЛИДАТОРЫ И НОРМАЛИЗАТОРЫ
# -------------------
def validate_phone(value: str) -> str:
    cleaned = re.sub(r'[\s\-\(\)]', '', value)
    if cleaned.startswith('8'):
        cleaned = '+7' + cleaned[1:]
    elif not cleaned.startswith('+7'):
        cleaned = '+7' + cleaned
    
    if len(cleaned) != settings.PHONE_NUM_LENGTH or not cleaned[2:].isdigit():
        raise ValueError(f'Некорректный формат номера {cleaned}')
    return cleaned

def validate_cyrillic(value: str) -> str:
    """Проверка на некорректные дефисы."""
    if '--' in value:
        raise ValueError('Недопустимое сочетание символов: "--"')
    if value.startswith('-') or value.endswith('-'):
        raise ValueError('Дефис не может быть в начале/конце')
    return value

# -------------------
# АННОТАЦИИ
# -------------------

RussianPhoneNumber = Annotated[
    str,
    Field(
        pattern=RUSSIAN_PHONE_PATTERN,
        description=(f'Номер телефона в российском формате. '
                        f'Должен начинаться с 7/+7 или 8, '
                        f'содержать 11 цифр, код оператора — с 9.'
        ),
        examples=['+79991234567', '8 (999) 123-45-67', '79991234567']
    ),
    AfterValidator(validate_phone)
]

CyrillicName = Annotated[
    str,
    Field(
        pattern=CYRILLIC_NAME_PATTERN,
        min_length=settings.MIN_LENGTH_NAME,
        max_length=settings.MAX_LENGTH_NAME,
        description=(f'Только кириллица, пробелы, дефисы. '
                     f'Минимум {settings.MIN_LENGTH_NAME} символов.'),
        examples=['Иванов', 'Анна-Мария']
    ),
    AfterValidator(validate_cyrillic)
]

TelegramId = Annotated[
    str,
    Field(
        pattern=TELEGRAM_ID_PATTERN,
        min_length=settings.MIN_LENGTH_TELEGRAM_ID,
        max_length=settings.MAX_LENGTH_TELEGRAM_ID,
        description=(
            'Уникальный ID пользователя в Telegram. '
            f'Длина: {settings.MIN_LENGTH_TELEGRAM_ID}–'
            f'{settings.MAX_LENGTH_TELEGRAM_ID} цифр.'
        ),
        examples=['123456789', '987654321']
    )
]
