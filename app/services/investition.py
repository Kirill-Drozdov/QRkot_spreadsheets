from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.charity_project import CharityProjectCreate
from app.schemas.donation import DonationCreate
from app.models import CharityProject, Donation, User


async def make_donation(
    donation: DonationCreate,
    session: AsyncSession,
    user: User
):
    """Запуск процесса инвестирования при пожертвовании."""
    donation_data = donation.dict()
    donation_db = Donation(
        user_id=user.id,
        full_amount=donation_data.get('full_amount'),
        comment=donation_data.get('comment'),
        invested_amount=0,
        close_date=None,
    )
    full_amount = donation_db.full_amount
    open_projects = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested == 0
        )
    )
    open_projects = open_projects.scalars().all()
    items_to_commit = []
    if open_projects:
        for project in open_projects:
            need_amount = project.full_amount - project.invested_amount
            if full_amount < need_amount:
                project.invested_amount += full_amount
                items_to_commit.append(project)

                donation_db.fully_invested = True
                donation_db.invested_amount += full_amount
                donation_db.close_date = datetime.now()
                break
            elif full_amount == need_amount:
                project.invested_amount += full_amount
                project.fully_invested = True
                project.close_date = datetime.now()
                items_to_commit.append(project)

                donation_db.fully_invested = True
                donation_db.invested_amount += full_amount
                donation_db.close_date = datetime.now()
                break
            else:
                # Остаток.
                balance = full_amount - need_amount
                project.invested_amount += need_amount
                project.fully_invested = True
                project.close_date = datetime.now()
                items_to_commit.append(project)

                donation_db.invested_amount += need_amount
                full_amount = balance
                continue
    items_to_commit.append(donation_db)
    for item in items_to_commit:
        session.add(item)
        await session.commit()
        await session.refresh(item)

    return donation_db


async def create_project(
        donation: CharityProjectCreate,
        session: AsyncSession,
):
    """Запуск процесса инвестирования при создании проекта."""
    project_data = donation.dict()
    project_db = CharityProject(
        name=project_data.get('name'),
        description=project_data.get('description'),
        full_amount=project_data.get('full_amount'),
        invested_amount=0,
        close_date=None,
    )
    need_amount = project_db.full_amount
    open_donations = await session.execute(
        select(Donation).where(
            Donation.fully_invested == 0
        )
    )
    open_donations = open_donations.scalars().all()
    items_to_commit = []
    if open_donations:
        print(open_donations)
        print(need_amount)
        for donation in open_donations:
            amount_to_invest = donation.full_amount - donation.invested_amount
            if amount_to_invest < need_amount:
                donation.invested_amount += amount_to_invest
                donation.fully_invested = True
                donation.close_date = datetime.now()
                items_to_commit.append(donation)

                project_db.invested_amount += amount_to_invest
                continue
            elif amount_to_invest == need_amount:
                donation.invested_amount += amount_to_invest
                donation.fully_invested = True
                donation.close_date = datetime.now()
                items_to_commit.append(donation)

                project_db.invested_amount += amount_to_invest
                project_db.fully_invested = True
                project_db.close_date = datetime.now()
                break
            else:
                donation.invested_amount += need_amount
                items_to_commit.append(donation)

                project_db.invested_amount += need_amount
                project_db.fully_invested = True
                project_db.close_date = datetime.now()
                break

    items_to_commit.append(project_db)
    for item in items_to_commit:
        session.add(item)
        await session.commit()
        await session.refresh(item)

    return project_db
