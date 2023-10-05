from core import dp
from asyncio import gather, create_task

from utils import base as Ubase
from utils import valid as Uvalid
from utils import userApp as UUapp
from utils import moder as Umoder

from aiogram import types
from aiogram.dispatcher import filters
from aiogram.dispatcher import FSMContext

from db import AsyncSession
from db.base import AppTable


import template.base as Tbase
import template.register as Tregister
import template.start as Tstart
import template.moder as Tmoder
import module.register as Mregister



async def send_user_app(
    db : AsyncSession,
    ctx : types.Message, 
    app : AppTable,
    state : FSMContext
):
    await ctx.answer(
        text=Tregister.success,
        reply_markup=Tstart.Start.kb()
    )

    _app = await UUapp.send_app(
        chat_id = ctx.from_user.id,
        app=app
    )

    return await gather(
        create_task(db.commit()),
        create_task(state.update_data(app_id=_app.message_id)),
        create_task(state.set_state(None)),
    )

#
# Handler for question about creating a app for user
#
@dp.message_handler(
    filters.Text(Tregister.Register.btn_yes),
    state=Mregister.RegisterState.form
)
async def form_handler(
    ctx : types.Message,
    db : AsyncSession,
    state : FSMContext,
) -> None:
    
    await ctx.answer(
        text=Tregister.Gender.text,
        reply_markup=Tregister.Gender.kb()
    )

    return await gather(
        create_task(db.close()),
        create_task(Mregister.RegisterState.gender.set())
    )


@dp.message_handler(
    filters.Text([Tbase.Back.btn_text]),
    state=Mregister.RegisterState
)
async def comeback_handler(
    ctx : types.Message,
    db : AsyncSession,
    state : FSMContext
):
    """

    Handler for comebacking
    
    """
    reponse = await gather(
        create_task(state.get_state()),
        create_task(state.get_data())
    )

    current_state = reponse[0]
    data = reponse[1]
    gender = data.get("gender")

    
    
    if (
        (current_state == Mregister.RegisterState.gender.state) or 
        (current_state == Mregister.RegisterState.form.state)
    ):
        return await gather(
            create_task(db.close()),
            create_task(state.set_state(None)),
            create_task(ctx.answer(
                text=Tstart.Start.text.format(message=ctx),
                reply_markup=Tstart.Start.kb()
            ))
        )

    elif current_state == Mregister.RegisterState.name.state:
        return await gather(
            create_task(db.close()),
            create_task(Mregister.RegisterState.gender.set()),
            create_task(ctx.answer(
                text=Tregister.Gender.text,
                reply_markup=Tregister.Gender.kb()
            ))
        )
    elif current_state == Mregister.RegisterState.years.state:
        return await gather(
            create_task(db.close()),
            create_task(Mregister.RegisterState.name.set()),
            create_task(ctx.answer(
                text=Tregister.name,
                reply_markup=Tregister.Back.kb()
            ))
        )
    elif current_state == Mregister.RegisterState.city.state:
        return await gather(
            create_task(db.close()),
            create_task(Mregister.RegisterState.years.set()),
            create_task(ctx.answer(
                text=Tregister.years.format(message=ctx),
                reply_markup=Tregister.Back.kb()
            ))
        )
    elif current_state == Mregister.RegisterState.usr.state:
        return await gather(
            create_task(db.close()),
            create_task(Mregister.RegisterState.city.set()),
            create_task(ctx.answer(
                text=Tregister.city,
                reply_markup=Tregister.Back.kb()
            ))
        )
    elif current_state == Mregister.RegisterState.photo.state:
        return await gather(
            create_task(db.close()),
            create_task(Mregister.RegisterState.usr.set()),
            create_task(ctx.answer_photo(
                photo=Tregister.Usr.photo,
                caption=Tregister.Usr.text,
                reply_markup=Tregister.Usr.kb()
            ))
        )
    elif current_state == Mregister.RegisterState.video.state:

        if gender == Tregister.Gender.btn_male:

            await ctx.answer(
                text=Tregister.Photo.text_male,
                    reply_markup=Tregister.Photo.kb(
                    gender=gender
                )
            )
        else:
            await ctx.answer(
                text=Tregister.Photo.text_female,
                reply_markup=Tregister.Photo.kb(
                    gender=gender
                )
            )


        return await gather(
            create_task(db.close()),
            create_task(Mregister.RegisterState.photo.set()),
        )

    elif current_state == Mregister.RegisterState.pub_video.state:

        if gender == Tregister.Gender.btn_male:

            await ctx.answer(
                text=Tregister.Video.text_male,
                reply_markup=Tregister.Photo.kb(
                    gender=data.get("gender")
                )
            )
        else:
            await ctx.answer(
                text=Tregister.Video.text_female,
                reply_markup=Tregister.Video.kb(
                    gender=data.get("gender")
                )
            )

        return await gather(
            create_task(db.close()),
            create_task(Mregister.RegisterState.video.set())
        )

    return await db.close()


@dp.message_handler(
    filters.Text([
        Tregister.Gender.btn_male, 
        Tregister.Gender.btn_female
    ]),
    state=Mregister.RegisterState.gender
)
async def register_gender_handler(
    ctx : types.Message,
    db : AsyncSession,
    state : FSMContext
):
    """
    App main.

    give a ppp to users
    """
    await ctx.answer(
        text=Tregister.name,
        reply_markup=Tregister.Back.kb()
    )

    return await gather(
        create_task(db.close()),
        create_task(state.update_data(gender=ctx.text)),
        create_task(Mregister.RegisterState.name.set())
    )


@dp.message_handler(
    content_types=types.ContentTypes.TEXT,
    state=Mregister.RegisterState.name
)
async def register_name_handler(
    ctx : types.Message,
    db : AsyncSession,
    state : FSMContext
):
    """
    App main.

    give a ppp to users
    """

    if not Uvalid.valid_name(name:=ctx.text):
        return await gather(
            create_task(db.close()),
            create_task(ctx.delete()),
            create_task(Ubase.delay(
                ctx.answer(Tregister.err_name))
            ),
        )

    await ctx.answer(
        text=Tregister.years.format(message=ctx),
        reply_markup=Tregister.Back.kb()
    )

    return await gather(
        create_task(db.close()),
        create_task(state.update_data(name=name)),
        create_task(Mregister.RegisterState.years.set())
    )


@dp.message_handler(
    content_types=types.ContentTypes.TEXT,
    state=Mregister.RegisterState.years
)
async def register_years_handler(
    ctx : types.Message,
    db : AsyncSession,
    state : FSMContext
):
    """
    App main.

    give a ppp to users
    """

    if not Uvalid.valid_years(years:=ctx.text):
        return await gather(
            create_task(db.close()),
            create_task(ctx.delete()),
            create_task(Ubase.delay(
                ctx.answer(Tregister.err_years))
            ),
        )


    await ctx.answer(
        text=Tregister.city,
        reply_markup=Tregister.Back.kb()
    )

    return await gather(
        create_task(db.close()),
        create_task(state.update_data(years=int(years))),
        create_task(Mregister.RegisterState.city.set())
    )


@dp.message_handler(
    content_types=types.ContentTypes.TEXT,
    state=Mregister.RegisterState.city
)
async def register_city_handler(
    ctx : types.Message,
    db : AsyncSession,
    state : FSMContext
):
    """
    App main.

    give a ppp to users
    """
    
    if not Uvalid.valid_city(city:=ctx.text):
        return await gather(
            create_task(db.close()),
            create_task(ctx.delete()),
            create_task(Ubase.delay(
                ctx.answer(Tregister.err_city))
            ),
        )

    data = await state.get_data()
    gender = data.get("gender")
    
    if gender == Tregister.Gender.btn_male: 

        await ctx.answer(
            text=Tregister.Photo.text_male,
            reply_markup=Tregister.Photo.kb(
                gender=data.get("gender")
            )
        )
    else:
        await ctx.answer(
            text=Tregister.Photo.text_female,
            reply_markup=Tregister.Photo.kb(
                gender=data.get("gender")
            )
        )

    return await gather(
        create_task(db.close()),
        create_task(state.update_data(city=city)),
        create_task(Mregister.RegisterState.photo.set())
    )


@dp.message_handler(
    filters.Text(Tregister.Photo.btn_next),
    state=Mregister.RegisterState.photo
)
@dp.message_handler(
    content_types=types.ContentTypes.PHOTO,
    state=Mregister.RegisterState.photo
)
async def register_photo_handler(
    ctx : types.Message,
    db : AsyncSession,
    state : FSMContext
):
    """
    App main.

    give a ppp to users
    """

    data = await state.get_data()
    gender = data.get("gender")  
    
    if (
        (ctx.text == Tregister.Photo.btn_next) and 
        (gender == Tregister.Gender.btn_male)
    ):
        photo_id = None
    elif (
        (ctx.text == Tregister.Video.btn_next) and 
        (gender == Tregister.Gender.btn_female)
    ):
        return await gather(
            create_task(db.close()),
            create_task(ctx.delete()),
            create_task(Ubase.delay(ctx.answer(Tregister.Photo.err_text)))
        )
    else:
        photo_id = await Ubase.get_save_photo_id(ctx)


    await ctx.answer(
        text=(
            Tregister.Video.text_male 
            if gender == Tregister.Gender.btn_male
            else Tregister.Video.text_female
        ),
        reply_markup=Tregister.Video.kb(
            gender=gender
        )
    )


    return await gather(
        create_task(db.close()),
        create_task(state.update_data(photo_id=photo_id)),
        create_task(Mregister.RegisterState.video.set())
    )


@dp.message_handler(
    filters.Text(Tregister.Video.btn_next),
    state=Mregister.RegisterState.video
)
@dp.message_handler(
    content_types=types.ContentTypes.VIDEO_NOTE,
    state=Mregister.RegisterState.video
)
async def register_video_handler(
    ctx : types.Message,
    db : AsyncSession,
    state : FSMContext
):
    """
    App main.

    give a ppp to users
    
    """
    data = await state.get_data()
    gender = data.get("gender")  
    chat_id = ctx.from_user.id

    if (
        (ctx.text == Tregister.Video.btn_next) and 
        (gender == Tregister.Gender.btn_male)
    ):
        video_id = None
    elif (
        (ctx.text == Tregister.Video.btn_next) and 
        (gender == Tregister.Gender.btn_female)
    ):
        return await gather(
            create_task(db.close()),
            create_task(ctx.delete()),
            create_task(Ubase.delay(ctx.answer(Tregister.Video.err_text)))
        )
    else:
        video_id = await Ubase.get_save_video_id(ctx)

    if video_id is None:
        db.add(app:=AppTable(
            chat_id=chat_id,
            gender=data.get("gender"),
            name=data.get("name"),
            years=data.get("years"),
            city=data.get("city"),
            photo_id=data.get("photo_id"),
            video_id=video_id,
            pub_video=False,
            moderated=False,
        ))

        await Umoder.moderate(
            user=app,
            db=db
        )

        await ctx.answer(
            text=Tmoder.Moder.check, 
            reply_markup=Tstart.Start.kb()
        )
        await state.set_state(None)

        return await db.commit()

    await ctx.answer(
        text=Tregister.Pub_video.text,
        reply_markup=Tregister.Pub_video.kb()
    )


    return await gather(
        create_task(db.close()),
        create_task(state.update_data(video_id=video_id)),
        create_task(Mregister.RegisterState.pub_video.set())
    )


@dp.message_handler(
    filters.Text([
        Tregister.Pub_video.btn_accept, 
        Tregister.Pub_video.btn_dicline
    ]),
    state=Mregister.RegisterState.pub_video
)
async def register_finish_handler(
    ctx : types.Message,
    db : AsyncSession,
    state : FSMContext
):
    data = await state.get_data()
    chat_id = ctx.chat.id

    if ctx.text == Tregister.Pub_video.btn_accept:
        pub_video = True
    else:
        pub_video = False

    db.add(app:=AppTable(
        chat_id=chat_id,
        gender=data.get("gender"),
        name=data.get("name"),
        years=data.get("years"),
        city=data.get("city"),
        photo_id=data.get("photo_id"),
        video_id=data.get("video_id"),
        pub_video=pub_video,
        moderated=False
    ))

    await Umoder.moderate(
        user=app,
        db=db
    )


    await ctx.answer(
        text=Tmoder.Moder.check, 
        reply_markup=Tstart.Start.kb()
    )

    await state.set_state(None)

    return await db.commit()
