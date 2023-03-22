from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate,
    check_charity_project_exists
)
from app.crud.charity_project import charity_project_crud
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate
)
from app.services.investition import create_project

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    """Получение всех проектов."""
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Создание проекта. Только для суперюзеров."""
    await check_name_duplicate(charity_project.name, session)
    return await create_project(charity_project, session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Редактирование проекта. Только для суперюзеров."""
    project = await check_charity_project_exists(
        project_id,
        session
    )

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    return await charity_project_crud.update(
        project,
        obj_in,
        session
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Удаление проекта. Только для суперюзеров."""
    project = await check_charity_project_exists(
        project_id,
        session
    )
    return await charity_project_crud.remove(
        project,
        session
    )
