from core import dp, bot
from asyncio import gather, create_task

from utils import base
from utils import userApp as UUapp
from aiogram.types import Message
from aiogram.dispatcher import filters
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageToDeleteNotFound

from db import AsyncSession


import template.start as Tstart
import template.register as Tregister
import module.register as Mregister


@dp.message_handler(
    filters.Text(Tstart.Start.btn_app),
    state=None)
async def main_handler(
    ctx : Message,
    db : AsyncSession,
    state : FSMContext,
) -> None:
    """
    Handler of app.
    """
    if ctx.chat.type != "private":
        return await db.close()
    
    chat_id = ctx.chat.id
    
    app, data = await gather(
        create_task(base.get_app(db, chat_id)),
        create_task(state.get_data())
    )

    if app is None:
        await ctx.answer(
            text=Tregister.Register.text,
            reply_markup=Tregister.Register.kb()
        )

        return await gather(
            create_task(db.close()),
            create_task(Mregister.RegisterState.form.set())
        )
    
    app = await UUapp.send_app(chat_id, app)

    if (app_id:=data.get("app_id")) is not None:
        try:
            await bot.delete_message(chat_id, app_id)
        except MessageToDeleteNotFound:
            ...

    return await gather(
        create_task(db.close()),
        create_task(state.update_data(app_id = app.message_id)),
    )

