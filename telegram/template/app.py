from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from json import dumps

from db.base import AppTable

from aiogram.utils.deep_linking import get_start_link

from utils.base import is_moder

import module.app as Mapp
import template.base as Tbase
import module.edit as Medit
import module.premium as Mpremium
import module.moder as Mmoder
import module.payment as Mpayment



class AppUser:

    text = """
Город:  {app.city}
Возраст:  {app.years}
Имя:  {app.name}
Пол:  {app.gender}
Рейтинг:  {app.score}
Пользователь:  {username}
    """

    delete =  """<b>Вы удалили анкету</b>\n\n<i>В любой момент Вы сможете создать её занова!</i>"""

    def kb(app : AppTable):

        _kb = InlineKeyboardMarkup(row_width=1)


 
        
        if app.video_id is not None:
            _kb.add(
                InlineKeyboardButton(
                    text="👁 Моё видео",
                    callback_data=Mapp.UserCall.new(
                        action="open.video"
                    )
                ),    
                InlineKeyboardButton(
                    text=(
                        "🟢 Статус видео: Публичный" 
                        if app.pub_video else 
                        "*️⃣ Статус видео: Приватный"),
                    callback_data=(
                        Medit.EditCall.new(value="switch.video.off") 
                        if app.pub_video else 
                        Medit.EditCall.new(value="switch.video.on") 
                    )
                )
            )

        _kb.add(
            InlineKeyboardButton(
                text="📝 Редактировать",
                callback_data=Mapp.UserCall.new(
                    action="open.edit"
                )
            )
        ).row(
            InlineKeyboardButton(
                text="❌ Удалить",
                callback_data=Mapp.UserCall.new(
                    action="delete"
                )
            ),InlineKeyboardButton(
                text="🔝 Рейтинг",
                callback_data=Mpayment.UserCall.new(
                    action="form",
                    from_id=app.user_id,
                    to_id=app.user_id,
                    page=-1
                )
            ),        
        )
        
        if app.moderated is False:
            _kb.add(
                InlineKeyboardButton(
                    text="⏺ На модерации ...",
                    callback_data="."
                )
            )

        elif app.moderated is None:
            _kb.add(
                InlineKeyboardButton(
                    text="Анкета отклонена",
                    callback_data="."
                )
            )   

        return _kb


class AppPremium:

    text = """
Город:  {app.city}
Возраст:  {app.years}
Имя:  {app.name}\n
Пол:  {app.gender}
Рейтинг:  {app.score}
Пользователь:  {username}
    """
    err = """📎 Походу пользователь решил удалить свою анкету или изменить её, подождите пока пользователю одобрять анкету или он её создать!"""
    getting = """🔍 Подождите... ищем анкету пользователя"""

    def delete_app(page : int, gender : str):
        _kb = InlineKeyboardMarkup()

        _kb.add(InlineKeyboardButton(
            text=Tbase.Back.btn_text,
            callback_data=Mpremium.bandCall.new(action="open", page=page, gender=gender)
        ))

        return _kb


    def kb(
        app : AppTable, 
        chat_id : int,
        gender : str,
        photo_mode : bool = True, 
        page : int = 0,
        moder : int = False
    ):
        _kb = InlineKeyboardMarkup()


        if (app.video_id is not None) and (app.pub_video is True):

            if photo_mode:
                _kb.add(
                    InlineKeyboardButton(
                        text="📸 Видео", 
                        callback_data=Mpremium.appCall.new(
                            action="video", 
                            user_id=app.user_id, 
                            page=page
                        )
                    ),
                )
            else:
                _kb.add(
                    InlineKeyboardButton(
                        text="📸 фото", 
                        callback_data=Mpremium.appCall.new(
                            action="open", 
                            user_id=app.user_id, 
                            page=page
                        )
                    ),
                )

        _kb.row(
            InlineKeyboardButton(
                text="🎁 Чаевые", 
                callback_data=Mpayment.UserCall.new(
                    action="form",
                    from_id=chat_id,
                    to_id=app.user_id,
                    page=page
                )
            ),
            InlineKeyboardButton(
                text=Tbase.Back.btn_text,
                callback_data=Mpremium.bandCall.new(action="open", gender=gender, page=page)
            ),
        )

        if moder:
            _kb.add(InlineKeyboardButton(
                text="Удалить",
                callback_data=Mpremium.moderCall.new(user_id=app.user_id, action="delete", page=page, gender=app.gender)
            ),)

        return _kb


class Posting:

    text = """
Город:  {app.city}
Возраст:  {app.years}
Имя:  {app.name}\n
Пол:  {app.gender}
Рейтинг:  {app.score}
    """


    async def kb(user_id : int, page : int, gender : str):
        
        return InlineKeyboardMarkup().add(InlineKeyboardButton(
            text="Перейти в профиль",
            url=await get_start_link(payload=dumps({
                    "user_id" : user_id,
                    "page" : page,
                    "gender" : gender
                }))
            )
        )


class Video:

    text = "Видео отправлено ниже"
    btn_skip = "Убрать"

    def kb():
        return InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                text=Video.btn_skip,
                callback_data=Mapp.UserCall.new(
                    action="close.video"
                )
            )
        )

