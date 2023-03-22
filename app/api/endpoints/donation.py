from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.schemas.donation import (
    DonationCreate,
    DonationSuperuserCaseDB,
    DonationUserCaseDB
)
from app.models import User
from app.services.investition import make_donation

router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationSuperuserCaseDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    """Получение списка всех пожертвований. Только для суперюзеров."""
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=List[DonationUserCaseDB],
)
async def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Получение списка пожертвований текущего пользователя."""
    return await donation_crud.get_by_user(user, session)


@router.post(
    '/',
    response_model=DonationUserCaseDB,
    response_model_exclude_none=True
)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Создание пожертвования."""
    return await make_donation(
        donation,
        session,
        user
    )
