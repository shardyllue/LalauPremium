from typing import List

from db.base import AppTable

from aiogram.types import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup
)

import module.premium as Mpremium


chose_gender_kb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(
        text="Ищу девушку", 
        callback_data=Mpremium.bandCall.new(action="open", page=0, gender="Девушка")
    ), 
    InlineKeyboardButton(
        text="Ищу мужчину", 
        callback_data=Mpremium.bandCall.new(action="open", page=0, gender="Мужчина")
    )
]])


class Band:

    text = """Уважаемые подписчики премиум-канала "lalau", для удобства знакомства с другими участниками мы создали список анкет участников проекта, которые ищут знакомства.Напоминаем, что "lalau" категорически против услуг проституции, порнографии и всему, что запрещено Уголовным кодексом Российской Федерации."""

    nums = {0 : "🥇", 1 : "🥈", 2 : "🥉"}

    def kb(
        apps : List[AppTable],
        gender : str,
        page : int = 0,
    ):
        _kb = InlineKeyboardMarkup()

        pages = apps.__len__() // 9
        start_with = 0 + 9*page
        finish_with = 9 + 9*page
        
        for index, app in enumerate(apps[start_with:finish_with]):
            if (index in range(0, 3)) and (page == 0):
                front = f"{Band.nums[index]}"
                back = ""
            else:
                front = ""
                back = f", Рейтинг: {app.score}"
    
            _kb.add(
                InlineKeyboardButton(
                    text=f"{front}{app.city}, {app.name}, {app.years} лет{back}", 
                    callback_data=Mpremium.appCall.new(action="open", user_id=app.user_id, page=page)
                ),
            )
        

        return _kb.row(
            InlineKeyboardButton(
                text="⬅️" if page > 0 else " ", 
                callback_data=Mpremium.bandCall.new(
                    action="left", page=page, gender=gender
                ) if page > 0 else " "
            ),
            InlineKeyboardButton(
                text=f"{page + 1} / {pages + 1}", 
                callback_data="."
            ),
            InlineKeyboardButton(
                text="➡️" if page < pages else " ", 
                callback_data=Mpremium.bandCall.new(
                    action="right", page=page, gender=gender
                ) if page < pages else " "
            ),
        )
