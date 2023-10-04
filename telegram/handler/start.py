from core import dp
from asyncio import gather, create_task

from aiogram.types import Message
from aiogram.dispatcher import filters
from aiogram.dispatcher import FSMContext
from aiogram.utils.deep_linking import decode_payload

from json import loads, decoder


from db import AsyncSession

import template.start as Tstart
import template.app as Tapp
import utils.base as Ubase
import utils.premium as Upremium




@dp.message_handler(filters.CommandStart(), state="*")
async def start_handler(ctx : Message, db : AsyncSession, state : FSMContext) -> None:
    """
    /start
    """

    if ctx.chat.type != "private":
        return await db.close()
    

    args = ctx.get_args()


    if args == "":

        await ctx.answer(
            text=Tstart.Start.text.format(
                message=ctx
            ),
            reply_markup=Tstart.Start.kb()
        )

        return await gather(
            create_task(db.close()),
            create_task(state.set_state(None))
        )
    
    
    user_id = int(args)
    
    app = await Ubase.get_app(db, user_id)

    await ctx.answer(
        text=Tapp.AppPremium.getting,
        reply_markup=Tstart.Start.kb()
    )


    if (app is None):
        return await gather(
            create_task(db.close()),
            create_task(ctx.answer(Tapp.AppPremium.err))
        )

    if (app.moderated is not True):
        return await gather(
            create_task(db.close()),
            create_task(ctx.answer(Tapp.AppPremium.err))
        )

    return await gather(
        create_task(db.close()),
        create_task(Upremium.send_app_premium(ctx.chat.id, app, 0))
    )



    


