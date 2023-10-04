import aioschedule as schedule
from loguru import logger
from asyncio import sleep
from datetime import datetime

from random import choice, randint

from db import AsyncSession, async_sessionmaker
from db.base import AppTable
from sqlalchemy import update

import utils.base as Ubase
import utils.premium as Upremium


showen = []


async def main_posting(db : AsyncSession):
    """
    
    Posting to main group
    
    """
    data = datetime.now()

    if not (datetime(data.year, data.month, data.day, 3, 0) < datetime.now() < datetime(data.year, data.month, data.day, 20, 0)):
        return await db.close()
    
    print("Hello world")

    apps = await Ubase.get_apps(db, gender="No matter", public=True)
    await db.close()

    if len(apps) == 0:
        return

    
    pages = Ubase.splite_array(apps, 9)
    random_page = randint(0, len(pages)-1)

    def get_unque():
        random_app = choice(pages[random_page])

        if len(showen) == len(apps):
            showen.clear()

        if (user:=random_app.user_id) not in showen:
            showen.append(user)
            return random_app
        
        return get_unque()
    
    
    random_app = get_unque()

    logger.info("Posting")

    return await Upremium.send_app_premium_group(random_app, random_page)

    
async def sqlachmey_zeroing(
    db : AsyncSession
):
    """
    Set everybody score to 0 
    """

    logger.info("Zeroing")

    sql = update(AppTable).values(score=0)

    await db.execute(sql)

    return await db.commit()


async def scheduler_startup(
    async_session : async_sessionmaker
) -> None:
    """
    schedular 
    """

    schedule.every(30).days.do(
        sqlachmey_zeroing, 
        db = async_session()
    )
    schedule.every().minute.do(
        main_posting, 
        db = async_session()
    )

    while True:
        await schedule.run_pending()
        await sleep(1)
