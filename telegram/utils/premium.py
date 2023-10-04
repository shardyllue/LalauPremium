from sqlalchemy.util import generic_repr
from db import AsyncSession
from db.base import AppTable

from core import bot

from utils import config

from utils.base import is_moder

import utils.base as Ubase
import template.app as Tapp
import template.premium as Tpremium
import static


async def send_band(
    chat_id : int, 
    db : AsyncSession,
    gender : str,
    page : int = 0,
):
    apps = await Ubase.get_apps(db, gender)
    kb = Tpremium.Band.kb(apps, gender, page)

    return await bot.send_message(
        chat_id=chat_id,
        text=Tpremium.Band.text,
        reply_markup=kb
    )


async def send_app_premium(
    chat_id  : int, app : AppTable, page : int = 0
):

    moder_user = await is_moder(chat_id)

    kb = Tapp.AppPremium.kb(app=app, chat_id=chat_id, gender=app.gender, page=page, moder=moder_user)
    caption = Tapp.AppPremium.text.format(app=app)


    return await bot.send_photo(
        chat_id=chat_id,
        caption=caption,
        photo=app.photo_id if app.photo_id else static.anon,
        reply_markup=kb
    )


async def send_app_premium_group(app : AppTable, page : int = 0):

    me = await bot.get_me()

    kb = await Tapp.Posting.kb(
        user_id=app.user_id,
        page=page,
        gender=app.gender
    )


    caption = Tapp.Posting.text.format(app=app)

    return await bot.send_photo(
        chat_id=config.PUBLIC_GROUP,
        caption=caption,
        photo=app.photo_id,
        reply_markup=kb
    )


async def send_video_premium(
    chat_id : int, app : AppTable, page : int = 0
):
    return await bot.send_video_note(
        chat_id=chat_id,
        video_note=app.video_id,
        reply_markup=Tapp.AppPremium.kb(
            app=app, 
            chat_id=chat_id, 
            page=page, 
            photo_mode=False
        )
    )
