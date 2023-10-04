from core import dp

from aiogram import types

from db import AsyncSession

import module.plug as Mplug
import utils.base as Ubase



@dp.callback_query_handler(
    Mplug.MessageCall.filter(), 
    state="*"
)
async def message_plug_callback_handler(
    query : types.CallbackQuery,
    callback_data : dict,
    db : AsyncSession,
):
    
    message = callback_data.get("message")

    await Ubase.delay(
        query.message.answer(text=message)
    )
    return await db.close()