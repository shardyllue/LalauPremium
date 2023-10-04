from db.base import AppTable

from core import bot
from aiogram import types

from utils.base import is_moder

import template.app as Tapp
import static


async def send_app(
    chat_id : int,
    app : AppTable
) -> types.Message:
    """
    
    Send app to user
    
    """


    photo_id = (
        app.photo_id 
        if app.photo_id is not None else static.anon
    ) 

    return await bot.send_photo(
        chat_id=chat_id,
        photo=photo_id,
        caption=Tapp.AppUser.text.format(app=app),
        reply_markup=Tapp.AppUser.kb(app)
    )