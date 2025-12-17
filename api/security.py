from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from config import Security


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        timedelta(minutes=Security.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({'exp': expire})
    return jwt.encode(
        to_encode,
        Security.JWT_SECRET_KEY,
        algorithm=Security.ALGORITHM
    )


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            Security.JWT_SECRET_KEY,
            algorithms=[Security.ALGORITHM]
        )
    except JWTError:
        raise ValueError('Invalid token')
