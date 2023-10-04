from typing import Sequence
from random import choice

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lalau import logger

from lalau.base import AppTable
from lalau.values import sent_apps


def get_unique(apps : Sequence[AppTable]) -> AppTable:
    app = choice(apps)

    if len(sent_apps) == 1:

        sent_apps.clear()

        return get_unique(apps)

    elif len(sent_apps) == len(apps):

        logger.log("POST", "Clear a sent apps")

        last_value = list(sent_apps.items())[-1]
        sent_apps.clear()
        sent_apps.setdefault(*last_value)
        
        return get_unique(apps)

    elif sent_apps.get(app.user_id):
        return get_unique(apps)
    
    sent_apps.setdefault(app.user_id, True)

    logger.log("POST", f"Current lenght of a sent app is {len(sent_apps)}. Apps is {len(apps)}")

    return app
    



async def get_user_apps(session : AsyncSession) -> Sequence[AppTable]:
    
    stmt = select(AppTable).\
        where(AppTable.moderated == True)
    
    it = await session.execute(stmt)
    
    return it.scalars().all()

async def get_post_app(session : AsyncSession) -> AppTable:
    
    apps = await get_user_apps(session)

    return get_unique(apps)

