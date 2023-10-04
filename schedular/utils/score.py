from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update

from lalau.base import AppTable



async def clean_score(session : AsyncSession):

    stmt = update(AppTable).values(score=0)

    await session.execute(stmt)
    await session.commit()