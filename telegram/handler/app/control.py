from core import dp
from asyncio import gather, create_task

from utils import base as Ubase
from utils import moder as Umoder

from aiogram import types
from aiogram.dispatcher import FSMContext

from db import AsyncSession
from db.sql import delete
from db.base import AppTable


import template.app as Tapp
import template.edit as Tedit
import template.start as Tstart
import module.app as Mapp


@dp.callback_query_handler(
    Mapp.UserCall.filter(
        action="open.edit"),
    state=None
)
async def open_edit_handler(
    query : types.CallbackQuery,
    callback_data : dict,
    db : AsyncSession,
    state : FSMContext,
) -> None:
    return await gather(
        create_task(db.close()),
        create_task(query.message.edit_reply_markup(
            reply_markup=Tedit.kb_edit()
        ))
    )


@dp.callback_query_handler(
    Mapp.UserCall.filter(
        action="open.control"),
    state=None
)
async def open_edit_handler(
    query : types.CallbackQuery,
    callback_data : dict,
    db : AsyncSession,
    state : FSMContext,
) -> None:
    app = await Ubase.get_app(db, query.from_user.id)

    if app is None:
        return await db.close()

    if app.moderated is False:
        await Umoder.moderate(app, db)

    return await gather(
        create_task(db.close()),
        create_task(query.message.edit_reply_markup(
            reply_markup=Tapp.AppUser.kb(app)
        ))
    )


@dp.callback_query_handler(
    Mapp.UserCall.filter(
        action="delete"),
    state=None,
)
async def delete_app_handler(
    query : types.CallbackQuery,
    callback_data : dict,
    db : AsyncSession,
    state : FSMContext,
) -> None:
    """
    Delete user's app
    """
    user_id = query.from_user.id 
    await db.execute(
        delete(AppTable).where(
            AppTable.user_id == user_id
        )
    )

    return await gather(
        create_task(query.message.delete()),
        create_task(db.commit()),
        create_task(query.message.answer(
            text=Tapp.AppUser.delete, 
            reply_markup=Tstart.Start.kb()
        ))
    )


@dp.callback_query_handler(
    Mapp.UserCall.filter(action="open.video"), 
    state=None
)
async def open_video_handler(
    query : types.CallbackQuery,
    db : AsyncSession,
    state : FSMContext
):
    app = await Ubase.get_app(db,  query.from_user.id)

    if app is None:
        return await db.close()

    await gather(
        create_task(query.answer(Tapp.Video.text)),
        create_task(query.message.answer_video_note(
            video_note=app.video_id,
            reply_markup=Tapp.Video.kb()
        ))
    )

    return await db.close()


@dp.callback_query_handler(
    Mapp.UserCall.filter(action="close.video"), 
    state="*"
)
async def close_video_handler(
    query : types.CallbackQuery,
    db : AsyncSession,
    state : FSMContext
):

    return await gather(
        create_task(db.close()),
        create_task(query.message.delete()),
    )

