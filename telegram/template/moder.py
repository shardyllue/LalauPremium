from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from db.base import AppTable

import module.moder as Mmoder 


class Moder:


    text = """
Город:  {app.city}
Возраст:  {app.years}
Имя:  {app.name}\n
Пол:  {app.gender}
Рейтинг:  {app.score}
Пользователь:  {app.usrname}\n
    """

    check = "Ваша анкета отправлена на модерацию.\n\nВам придет уведомление, когда модератор подтвердит Вашу анкету"
    accept = "<b>Поздравляем! 🍾</b>\nВаша анкета одобрена!"
    decline = "К сожалению в размещении вашей анкеты отказано. Напишите администратору @chesters_mill"


    def kb(app : AppTable):
        return InlineKeyboardMarkup().row(
            InlineKeyboardButton(
                text="✅",
                callback_data=Mmoder.ModerCall.new(
                    action="accept",
                    user_id=app.user_id
                )
            ),
            InlineKeyboardButton(
                text="❌",
                callback_data=Mmoder.ModerCall.new(
                    action="decline",
                    user_id=app.user_id
                )
            )
        )

    
    def kb_accept():
        return InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                text="✅",
                callback_data="."
            )
        )


    def kb_decline():
        return InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                text="❌",
                callback_data="."
            )
        )
    
    
    def moder_kb(from_id, to_id, page):

        return InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                text="Ввести сумму",
                callback_data=Mmoder.PaymentCall.new(
                    action="accept",
                    from_id=from_id,
                    to_id=to_id,
                    page=page
                )
            ),
            InlineKeyboardButton(
                text="Отмена",
                callback_data=Mmoder.PaymentCall.new(
                    action="decline",
                    from_id=from_id,
                    to_id=to_id,
                    page=page
                )
            )
        )

    

class Payment:

    text = "Отправьте "

    decline = ""
    accept = ""

    def kb_transfer_close():
        return InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                text="Вы его отменили",
                callback_data="."
            )
        )
    
    def kb_transfer_score(count):
        return InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                text=f"Было зачислено {count} рейтинга",
                callback_data="."
            )
        )
    
    cancel_transferred = "К сожалению в пополнение рейтинга отказано. Напишите администратору @chesters_mill"
    transferred_to = "На Ваш рейтинг зачислено: {score}"
    transferred_from = "Оплата прошла успешно.\n\nСпасибо за покупку"