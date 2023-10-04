from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)


class Back:

    btn_text = "🔙 Назад"


    def btn():
        return KeyboardButton(text=Back.btn_text)
    

