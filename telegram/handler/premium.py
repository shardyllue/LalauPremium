from core import dp, bot
from asyncio import gather, create_task

from aiogram import types
from aiogram.dispatcher import filters
from aiogram.dispatcher import FSMContext

from sqlalchemy import delete

from db import AsyncSession
from db.base import AppTable

import utils.base as Ubase
import template.start as Tstart
import template.premium as Tpremium
import module.premium as Mpremium
import utils.premium as Upremium


@dp.message_handler(
    filters.Text(Tstart.Start.btn_premiun),
    state=None)
async def premium_handler(
    ctx : types.Message,
    db : AsyncSession,
) -> None:
    """
    Premium.
    """

    if ctx.chat.type != "private":
        return await db.close()
    
    await ctx.answer(text=Tpremium.Band.text, reply_markup=Tpremium.chose_gender_kb)

    return await db.close()
    


@dp.callback_query_handler(
    Mpremium.bandCall.filter(),
    state=None
)
async def band_handler(
    query : types.CallbackQuery,
    callback_data : dict, 
    db : AsyncSession
):
    page = int(callback_data.get('page'))
    gender = callback_data.get("gender")
    act = callback_data.get('action')
    apps = await Ubase.get_apps(db, gender)
    user_id = query.from_user.id

    print(gender)

    if act == "open":

        try:
            await query.message.delete()
        except:
            #bad
            ...

        await Upremium.send_band(user_id, db, gender,page)
            
        return await db.close()

    elif act == "right":
        kb = Tpremium.Band.kb(apps, gender, page+1)

    else:
        kb = Tpremium.Band.kb(apps, gender, page-1)


    return await gather(
        create_task(db.close()),
        create_task(query.message.edit_text(Tpremium.Band.text, reply_markup=kb))
    )

