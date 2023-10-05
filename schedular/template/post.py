from json import dumps

from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton

from utils.deep import link

from lalau.base import AppTable


text = """
Город:  {app.city}
Возраст:  {app.years}
Имя:  {app.name}

Рейтинг:  {app.score}
"""


kb : InlineKeyboardMarkup = lambda user_id, username : InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(
        text="Перейти в профиль",
        url=link(user_id, username)
    )
]])
