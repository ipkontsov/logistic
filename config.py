from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from decouple import config as decouple_config
import redis.asyncio as redis


@dataclass
class AppSettings:
    # Основной режим
    PROD: bool = decouple_config('PROD', default=False, cast=bool)

    # Настройки пользователя
    MIN_LENGTH_TELEGRAM_ID: int = 5
    MAX_LENGTH_TELEGRAM_ID: int = 20
    MIN_LENGTH_NAME: int = 2
    MAX_LENGTH_NAME: int = 30
    PHONE_NUM_LENGTH: int = 12

    # База данных
    @property
    def DATABASE_URL(self) -> str:
        if self.PROD:
            user = decouple_config('DB_USER')
            password = decouple_config('DB_PASSWORD')
            host = decouple_config('DB_HOST')
            port = decouple_config('DB_PORT', default='5432')
            name = decouple_config('DB_NAME')
            return (
                f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}'
            )
        else:
            BASE_DIR = Path(__file__).parent
            DB_PATH = BASE_DIR / 'instance' / 'dispatch.db'
            return f'sqlite+aiosqlite:///{DB_PATH}'

    # Redis
    REDIS_HOST: str = decouple_config('REDIS_HOST', default='localhost')
    REDIS_PORT: int = decouple_config('REDIS_PORT', default=16379, cast=int)
    REDIS_DB: int = decouple_config('REDIS_DB', default=0, cast=int)
    REDIS_PASSWORD: Optional[str] = decouple_config(
        'REDIS_PASSWORD', default=None
    )

    # Кэшируем клиент (создаём один раз)
    _redis_client: Optional[redis.Redis] = field(init=False, default=None)

    @property
    def redis_client(self) -> redis.Redis:
        if self._redis_client is None:
            self._redis_client = redis.Redis(
                host=self.REDIS_HOST,
                port=self.REDIS_PORT,
                db=self.REDIS_DB,
                password=self.REDIS_PASSWORD,
                decode_responses=True,
                max_connections=20,
                retry_on_timeout=True
            )
        return self._redis_client


settings = AppSettings()