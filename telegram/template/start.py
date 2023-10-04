from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


class Start:

    text = """<b>Добро пожаловать, {message.from_user.first_name}!</b>\n\nВыберите действие из предложенных ниже.
    """

    btn_app = "Моя анкета"
    btn_premiun = "Premium пользователи lalau"


    def kb():
        return ReplyKeyboardMarkup(
            one_time_keyboard=False,
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton(text=Start.btn_app)],
                [KeyboardButton(text=Start.btn_premiun)] 
            ]
        )
    



class Channel:

    text = """
☝️Уважаемые подписчики премиум-канала "lalau", для удобства знакомства с другими участниками, мы создали бота со списком анкет участников канала, которые ищут знакомства.
Если вы не добавили свою анкету, пожалуйста, добавьте её в бота.

⚠️Напоминаем, что "lalau" категорически против услуг проституции, порнографии и всего, что запрещено Уголовным кодексом Российской Федерации.

👇Пожалуйста, перейдите в бота.
    """

    def kb(username : str) -> InlineKeyboardMarkup:

        return InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                text="Анкеты участников",
                url=f"https://t.me/{username}?start"
            )
        )
