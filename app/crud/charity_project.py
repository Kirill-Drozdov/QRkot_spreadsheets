from typing import Optional, List
from http import HTTPStatus

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):
    """Расширенный класс CRUD для проекта."""
    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession,
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        if obj_data.get('fully_invested'):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Закрытый проект нельзя редактировать!'
            )
        if 'full_amount' in update_data:
            value_in = update_data.get('full_amount')
            value_db = obj_data.get('full_amount')
            if value_in > value_db:
                raise HTTPException(
                    status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                    detail=('Новая требуемая сумма для'
                            ' проекта должна быть не меньше старой!')
                )
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession,
    ):
        if db_obj.fully_invested:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='В проект были внесены средства, не подлежит удалению!'
            )
        elif db_obj.invested_amount > 0:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='В проект были внесены средства, не подлежит удалению!'
            )
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_charity_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return db_project_id.scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession
    ) -> List[dict[str, int]]:
        closed_projects = await session.execute(
            select(
                self.model
            ).where(
                self.model.fully_invested == 1
            )
        )
        return sorted(
            closed_projects.scalars().all(),
            key=lambda project: project.close_date - project.create_date
        )


charity_project_crud = CRUDCharityProject(CharityProject)
