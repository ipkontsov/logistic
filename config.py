from pathlib import Path

from decouple import config as decouple_config


class DataBase:
    PROD = decouple_config('PROD', default=False, cast=bool)

    if PROD:
        DATABASE_URL = f'postgresql+asyncpg://{...}'
    else:
        BASE_DIR = Path(__file__).parent
        DB_PATH = BASE_DIR / 'instance' / 'dispatch.db'
        DATABASE_URL = f'sqlite+aiosqlite:///{DB_PATH}'


class Security:
    ALGORITHM = 'HS256'
    JWT_SECRET_KEY = decouple_config('JWT_SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_MINUTES = decouple_config(
        'ACCESS_TOKEN_EXPIRE_MINUTES', default=15, cast=int
    )
