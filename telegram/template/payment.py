from aiogram.types import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton
)

import module.premium as Mpremium
import module.payment as Mpayemnt
import template.base as Tbase


class User:


    paid = """
    Спасибо за покупку.\n\nОжидайте ответа модератора!
    """

    delete_app = "Анкета удалена"

    text_user = "<b>Описание товара:</b>\n<i>Рейтинг поднимает Вас в Premium списке. Это значит, что Вас смогут найти больше людей!\n<b>Баланс рейтинга ежемесячно обнуляется.</b></i>\n\n<b>Цена: сумма от 100 до 5000 рублей.</b>\n"
    text_premium = "<b>Описание товара:</b>\n\n<i>Чаевые не уходят на карту человека, но они поднимают рейтинг его в выдаче Premium списка.\n<b>Баланс рейтинга ежемесячно обнуляется.</b></i>\n\n<b>Цена: сумма от 100 до 5000 рублей</b>\n"

    close_payment = "Вы отменили оплату"

    text_pay = "`6764 5444 4360 9839` - Сбербанк\n`W1SEFOX` - Qiwi\n\n*Тыкни на номер, он автоматически скопируется!*\nОтправьте боту квитанцию об оплате.\nНа квитанции должны быть четко видны: *дата*, *время* и *сумма платежа*!'"

    def kb(from_id, to_id, page):
        _kb = InlineKeyboardMarkup()

        _kb.add(
            InlineKeyboardButton(
                text="Оплатить", 
                callback_data=Mpayemnt.UserCall.new(
                    action="pay",
                    from_id=from_id,
                    to_id=to_id,
                    page=page
                ),
            ),
        )

        if page >= 0:
            _kb.add(
                InlineKeyboardButton(
                    text="Отмена", 
                    callback_data=Mpremium.appCall.new(
                        action="open", 
                        user_id=to_id, 
                        page=page,
                    )
                )
            )
        else:
            _kb.add(
                InlineKeyboardButton(
                    text="Отмена", 
                    callback_data=Mpayemnt.UserCall.new(
                        action="cancel",
                        from_id=from_id,
                        to_id=to_id,
                        page=page
                    ),
                ),
            )

        return _kb


    def kb_cancel(from_id, to_id, page):
        return ReplyKeyboardMarkup(
            one_time_keyboard=True,
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton(Tbase.Back.btn_text)]
            ]
        )

    

    text_form = """
    <b>Ожидение пополнение рейтига</b>

    От: 
    - id{from_id} 
    - @{username}

    Кому:
    - id{to_id}
    """

    def paid_kb(to_id, page):
        kb = InlineKeyboardMarkup()
        
        
        kb.add(
            InlineKeyboardButton(
                text="Вернуться к анкете", 
                callback_data=Mpremium.appCall.new(
                    action="open", 
                    user_id=to_id, 
                    page=page,
                )
            )
        )

        return kb