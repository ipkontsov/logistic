# api/modules/user/router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_db
from api.modules.users import models, schemas
from api.security import create_access_token

router = APIRouter(prefix='/user', tags=['User'])


@router.post(
    '/reserve',
    response_model=schemas.TelegramAccountResponse,
    status_code=201
)
async def reserve_telegram_account(
    account: schemas.WhiteListAdd,
    db: AsyncSession = Depends(get_db)
):
    """Резервация telegram_id и разрешение на регистрацию.
    Заполняется admin или grand_driver."""
    result = await db.execute(
        select(models.WhiteList).where(
            models.WhiteList.telegram_id == account.telegram_id
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(400, 'Telegram ID уже зарезервирован')

    new_account = models.WhiteList(telegram_id=account.telegram_id)
    db.add(new_account)
    await db.commit()
    await db.refresh(new_account)
    return new_account


@router.post(
    '/register',
    response_model=schemas.FullUserResponse,
    status_code=201
)
async def register_user(
    request: schemas.UserRegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    """Регистрация водителя. Заполняется driver."""
    result = await db.execute(
        select(models.TelegramAccount).where(
            models.TelegramAccount.telegram_id == request.telegram_id
        )
    )
    telegram_acc = result.scalar_one_or_none()
    if not telegram_acc:
        raise HTTPException(403, 'Ваш Telegram ID не приглашён')
    if telegram_acc.user_id is not None:
        raise HTTPException(400, 'Вы уже зарегистрированы')

    # Создание профиля
    new_user = models.User(
        first_name=request.user.first_name,
        last_name=request.user.last_name,
        license_number=request.user.license_number,
        phone_number=request.user.phone_number,
        role=request.user.role
    )
    db.add(new_user)
    await db.flush()  # Получаем id

    # Привязка
    telegram_acc.user_id = new_user.id
    telegram_acc.telegram_name = request.telegram_name
    await db.commit()
    await db.refresh(new_user)
    await db.refresh(telegram_acc)

    return schemas.FullUserResponse(
        user=schemas.UserResponse.model_validate(new_user),
        telegram_account=(
            schemas.TelegramAccountResponse.model_validate(telegram_acc)
        )
    )


@router.post('/auth', response_model=schemas.Token)
async def auth_by_telegram(
    auth_data: schemas.TelegramAuthRequest,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(models.TelegramAccount).where(
            models.TelegramAccount.telegram_id == auth_data.telegram_id
        )
    )
    telegram_acc = result.scalar_one_or_none()

    if not telegram_acc or telegram_acc.user_id is None:
        raise HTTPException(403, 'Доступ запрещён')

    token = create_access_token({'sub': str(telegram_acc.user_id)})
    return {'access_token': token, 'token_type': 'bearer'}
