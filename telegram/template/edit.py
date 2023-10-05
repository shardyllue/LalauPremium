from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

import template.base as Tbase
import module.app as Mapp
import module.edit as Medit
import module.plug as Mplug


def title(text : str):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(
            text=text, 
            callback_data=Mplug.MessageCall.new(
                message=text
            )
        ),
        InlineKeyboardButton(
            text=Tbase.Back.btn_text, 
            callback_data=Medit.EditCall.new(
                value="cancel"
            )
        )
    )



def kb_edit():

    return InlineKeyboardMarkup().add(
            InlineKeyboardButton(
            text="📝 Редактировние",
            callback_data=Medit.EditCall.new(
                value="."
            )
        )
    ).row(
        InlineKeyboardButton(
            text="Имя",
            callback_data=Medit.EditCall.new(
                value="name"
            )
        ),
        InlineKeyboardButton(
            text="Возраст",
            callback_data=Medit.EditCall.new(
                value="years"
            )
        ),
        InlineKeyboardButton(
            text="Город",
            callback_data=Medit.EditCall.new(
                value="city"
            )
        ),
    ).row(
        InlineKeyboardButton(
            text="Фото",
            callback_data=Medit.EditCall.new(
                value="photo"
            )
        ),       
        InlineKeyboardButton(
            text="Видео",
            callback_data=Medit.EditCall.new(
                value="video"
            )
        ),
        InlineKeyboardButton(
            text=" ",
            callback_data="empty_value"
        )
    ).add(        
        InlineKeyboardButton(
            text="✅ Применить",
            callback_data=Mapp.UserCall.new(
                action="open.control"
            )
        )
    )


edit_title_name = "Отправьте новое имя"
edit_title_years = "Отправьте возраст"
edit_title_city = "Отправьте новый город"
edit_title_usrname = "Отправьте новое @имя"
edit_title_photo = "Отправьте новое фото"
edit_title_video = "Отправьте новое видео"