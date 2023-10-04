from asyncio import gather, create_task

from core import dp, bot

from aiogram import types
from aiogram.dispatcher import FSMContext

from db import AsyncSession
from db.base import AppTable
from db.sql import delete 

import utils.base as Ubase
import utils.premium as Upremium
import template.app as Tapp
import module.premium as Mpremium


@dp.callback_query_handler(
    Mpremium.appCall.filter(action="open"),
    state=None
)
async def open_handler(
    query : types.CallbackQuery, 
    callback_data : dict,
    db : AsyncSession,
):
    """
    open app handler
    """

    app_user_id = int(callback_data["user_id"])
    page = int(callback_data["page"])
    user_id = query.from_user.id
    app = await Ubase.get_app(db, app_user_id)

    if not app:
        return await gather(
            create_task(query.answer(Tapp.AppPremium.err)),
            create_task(db.close())
        )

    return await gather(
        create_task(query.message.delete()),
        create_task(Upremium.send_app_premium(user_id, app, page)),
        create_task(db.close()),
    )


@dp.callback_query_handler(Mpremium.moderCall.filter(action="delete"), state=None)
async def Moder_delete(
    query : types.CallbackQuery, 
    callback_data : dict,
    db : AsyncSession,
):
    """
    open app handler
    """
    stmt = delete(AppTable).where(AppTable.user_id == int(callback_data["user_id"]))
    await db.execute(stmt)
    await db.commit()

    await query.message.edit_reply_markup(reply_markup=Tapp.AppPremium.delete_app(callback_data["page"], callback_data["gender"]))

    

@dp.callback_query_handler(
    Mpremium.appCall.filter(action="video"),
    state=None
)
async def video_handler(
    query : types.CallbackQuery, 
    callback_data : dict,
    db : AsyncSession,
):
    """
    Video handler
    """
    app_user_id = int(callback_data["user_id"])
    page = int(callback_data["page"])
    user_id = query.from_user.id

    app = await Ubase.get_app(db, app_user_id)

    if not app:
        return await gather(
            create_task(query.answer(Tapp.AppPremium.err)),
            create_task(db.close()),
        )

    return await gather(
        create_task(query.message.delete()),
        create_task(Upremium.send_video_premium(user_id,app,page)),
        create_task(db.close()),
    )
