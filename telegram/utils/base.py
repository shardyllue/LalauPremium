from typing import List

from asyncio import sleep
from core import bot

from aiogram import types

from db import AsyncSession
from db.sql import select
from db.base import AppTable

from core import bot
from utils.config import STORAGE_GROUP, MODER_GROUP


async def is_moder(user_id : int) -> bool:
    user = await bot.get_chat_member(chat_id=MODER_GROUP, user_id=user_id)
    return user.status != "left"


def splite_array(
    array : list, chunk : int
) -> list:
    """
    
    split a python list in half.
    
    """
    count_chunks = len(array)//chunk
    new_list = []

    for i in range(0, count_chunks + 1):

        start_with = 0 + chunk*i
        finish_with = chunk + chunk*i


        new_list.append(
            array[start_with:finish_with]
        )


    return new_list

    
async def get_app(
    db : AsyncSession,
    user_id : int,
) -> AppTable | None:
    """
    
    Get app from db
    
    """
    request = await db.execute(
        select(AppTable).where(
            AppTable.user_id == user_id
        )
    )

    if (app:=request.fetchone()) is None:
        return None
    
    return app[0]


async def get_apps(db : AsyncSession, gender : str, public = False) -> List[AppTable]:
    """
    
    Get apps from db
    
    """


    if not public:
        request = await db.execute(
            select(AppTable).where(
                (AppTable.moderated == True),
                (AppTable.gender == gender)
            ).order_by(AppTable.score)
        )

    else:
        request = await db.execute(
            select(AppTable).\
                where(AppTable.moderated == True))

    apps = request.fetchall()[::-1]

    return [app[0] for app in apps]


async def delay(
    ctx : types.Message,
    time : int = 5
) -> None:
    """
    
    send a delaied message

    """

    message = await ctx

    await sleep(time)

    return await message.delete()


async def get_save_photo_id(ctx : types.Message) -> int:
    """
    
    get video_id from the storage group

    """
    data = await bot.send_photo(
        photo=ctx.photo[0].file_id,
        chat_id=STORAGE_GROUP
    )

    return data.photo[0].file_id


async def get_save_video_id(ctx : types.Message) -> int:
    """
    
    get photo_id from the storage group

    """


    data = await bot.send_video_note(
        video_note=ctx.video_note.file_id,
        chat_id=STORAGE_GROUP
    )

    return data.video_note.file_id


