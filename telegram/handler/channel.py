from core import dp, bot
from aiogram import types

from db import AsyncSession

import utils.config as config
import template.start as Tstart


@dp.message_handler(commands=["post"])
async def post_channel_handler(
    ctx : types.Message,
    db : AsyncSession
):
    
    if ctx.chat.id != config.MODER_GROUP:
        return await db.close()
    
    me = await bot.get_me()

    await bot.send_message(
        chat_id=config.PUBLIC_GROUP,
        text=Tstart.Channel.text,
        reply_markup=Tstart.Channel.kb(me.username)
    )

    return await db.close()