from core import dp, bot
from asyncio import gather, create_task

from utils import config

from aiogram import types
from aiogram.dispatcher import filters
from aiogram.dispatcher import FSMContext

from db import AsyncSession

import utils.userApp as UUapp
import utils.base as Ubase
import module.payment as Mpayemnt

import utils.premium as Upremium
import template.base as Tbase
import template.payment as Tpayment
import template.start as Tstart
import template.moder as Tmoder



@dp.callback_query_handler(
    Mpayemnt.UserCall.filter(action="form"),
    state=None
)
async def main_handler(
    query : types.CallbackQuery, 
    callback_data : dict,
    db : AsyncSession
):
    """
    About payment
    """

    from_id = callback_data.get("from_id")
    to_id = callback_data.get("to_id")
    page = int(callback_data.get("page"))
    kb = Tpayment.User.kb(from_id, to_id, page)

    if page < 0:
        await query.message.answer(Tpayment.User.text_user, reply_markup=kb)
    else:
        await  query.message.answer(Tpayment.User.text_premium, reply_markup=kb)


    return await gather(
        create_task(db.close()),
        create_task(query.message.delete())
    )


@dp.callback_query_handler(
    Mpayemnt.UserCall.filter(action="cancel"),
    state=None
)
async def cancel_handler(
    query : types.CallbackQuery, 
    db : AsyncSession,
    state : FSMContext
):
    """
    Cancel payment
    """
    user_id = query.from_user.id
    app = await Ubase.get_app(db, user_id)

    if app is None:
        return await gather(
            create_task(db.close()),
            create_task(
                Ubase.delay(query.message.answer(Tpayment.User.delete_app))
            )
        )


    return await gather(
        create_task(db.close()),
        create_task(query.message.delete()),
        create_task(state.set_state(None)),
        create_task(UUapp.send_app(user_id, app))
    )
  

@dp.callback_query_handler(
    Mpayemnt.UserCall.filter(action="pay"),
    state=None
)
async def pay_handler(
    query : types.CallbackQuery, 
    callback_data : dict,
    db : AsyncSession,
    state : FSMContext
):
    """
    Payment hander.
    Set waiting the screenshot
    """
    from_id = callback_data.get("from_id")
    to_id = callback_data.get("to_id")
    page = int(callback_data.get("page"))

    check = await query.message.answer(
        text=Tpayment.User.text_pay,
        reply_markup=Tpayment.User.kb_cancel(from_id, to_id, page),
        parse_mode=types.ParseMode.MARKDOWN
    )

    return await gather(
        create_task(db.close()),
        create_task(query.message.delete()),
        create_task(Mpayemnt.UserState.payment.set()),
        create_task(state.update_data(from_id=from_id)),
        create_task(state.update_data(to_id=to_id)),
        create_task(state.update_data(page=page)),
        create_task(state.update_data(check_id=check.message_id))
    )




@dp.message_handler(
    filters.Text(Tbase.Back.btn_text),
    state=Mpayemnt.UserState.payment,
)
@dp.message_handler(
    content_types=types.ContentType.PHOTO,
    state=Mpayemnt.UserState.payment
)
async def screen_handler(
    ctx : types.Message, 
    state : FSMContext, 
    db : AsyncSession
):
    """
    Get screen
    """

    data = await state.get_data()
    from_id = int(data.get("from_id"))
    chat_id = ctx.from_user.id
    to_id = int(data.get("to_id"))
    page = int(data.get("page"))
    check_id = int(data.get("check_id"))


    if ctx.text == Tbase.Back.btn_text:

        await ctx.answer(Tpayment.User.close_payment, reply_markup=Tstart.Start.kb())

    else:

        photo_id = await Ubase.get_save_photo_id(ctx)

        caption = Tpayment.User.text_form.format(
            from_id=from_id,
            username=ctx.from_user.username,
            to_id=to_id,
        )

        await ctx.answer(Tpayment.User.paid, reply_markup=Tstart.Start.kb())

        await bot.send_photo(
            chat_id=config.MODER_GROUP,
            photo=photo_id,
            caption=caption,
            reply_markup=Tmoder.Moder.moder_kb(from_id, to_id, page)
        )

    if page < 0:
        app = await Ubase.get_app(db, chat_id)

        if app is not None:
            await UUapp.send_app(chat_id, app)

    else:   
        app = await Ubase.get_app(db, to_id)
        await Upremium.send_app_premium(chat_id, app, page)
        

    return await gather(
        create_task(db.close()), 
        create_task(state.set_state(None)),
        create_task(ctx.delete()),
        create_task(bot.delete_message(chat_id, check_id))
    )
