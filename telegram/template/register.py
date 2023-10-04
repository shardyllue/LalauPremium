from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)

import template.base as Tbase
import static


class Register:

    text = """
    <b>Походу Мы не нашли анкету на Ваше имя.</b>\n\nХотите создать анкету?
    """


    btn_yes = "✅ Да, хочу создать анкету"

    def kb():
        return ReplyKeyboardMarkup(
            one_time_keyboard=True,
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton(Register.btn_yes)],
                [Tbase.Back.btn()]
            ]
        )
    

class Gender:

    text = "<b>Вы мужчина или девушка?</b>"

    btn_male = "Мужчина"
    btn_female = "Девушка"

    def kb():
        return ReplyKeyboardMarkup(
            one_time_keyboard=True,
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(Gender.btn_male), 
                    KeyboardButton(Gender.btn_female)],
                [
                    Tbase.Back.btn()]
            ]
        )

class Back:


    def kb():
        return ReplyKeyboardMarkup(
            one_time_keyboard=True,
            resize_keyboard=True,
            keyboard=[
                [Tbase.Back.btn()]
            ]
        )



name = "<b>Как Вас зовут?</b>"
err_name = "⚠️<b>Невалидное имя!</b>\n\n<i>• Используйте только буквы Русского/Английского языка.\n• Имя не может быть длинее 15 символов.</i>"

years = "<b>{message.text}, cколько Вам лет?</b>"
err_years = "⚠️<b>Невалидный возраст!</b>\n\n<i>• Используйте только цифры.\n• Вам должно быть 18 лет или больше.</i>"

city = "<b>Из какого Вы города?</b>"
err_city = "⚠️<b>Невалидный город!</b>\n\n<i>• Используйте только буквы Русского/Английского языка.\n• Город не может быть длинее 20 символов.</i>"


class Usr:

    photo = static.usrname

    text = "<b>Теперь определимся с именем пользователя</b>\n\nПример: @lalau"
    err = "⚠️<b>Невалидное имя пользователя!</b>.\n\n<i>• Имя должно начинаться c «@».</i>\n<i>• Имя должно быть от 5 символов.</i>"
    err_tg = "⚠️<b>Невалидное имя пользователя!</b>\n\n<i>• Имя пользователя должно быть установлено.</i>"

    btn_usr = "Взять с моего аккаунта"

    def kb():
        return ReplyKeyboardMarkup(
            one_time_keyboard=True,
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton(Usr.btn_usr)],
                [Tbase.Back.btn()]
            ]
        )


class Photo:

    text_female = """
<b>Отлично! Отправьте свою фотографию</b>

⚠️<i>Ваша фотография будет видна только участникам premium канала.</i>
    """
    text_male = """
<b>Отлично! Отправьте свою фотографию</b>

⚠️<i>Если Вы переживаете за свою конфиденциальность и не хотите показывать свою фотографию, нажмите кнопку «👤Анонимное фото».</i>
    """
    btn_next = "👤 Анонимное фото"
    err_text = "Отправьте фотографию!"


    def kb(gender : str):

        

        return ReplyKeyboardMarkup(
            one_time_keyboard=True,
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton(Photo.btn_next)] if gender == Gender.btn_male else [],
                [Tbase.Back.btn()]
            ]
        )

class Video:
    text_female = "<b>Теперь Вам нужно записать видеосообщение («видео в кружочке»)</b>"
    text_male = """
<b>Теперь Вам нужно записать видеосообщение («видео в кружочке»)</b>

<i>Для мужчин необязательное требование, можно пропустить нажатием кнопки «🔜 Пропустить шаг»</i>
    """
    
    btn_next = "🔜 Пропустить шаг"
    err_text = "Отправьте видео!"

    def kb(gender : str):
        return ReplyKeyboardMarkup(
            one_time_keyboard=True,
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton(Video.btn_next)] if gender == Gender.btn_male else [],
                [Tbase.Back.btn()]
            ]
        )


class Pub_video:

    text = "<b>Разрешаете ли показывать Ваше видеосообщение («видео в кружочке») участникам премиум канала?</b>"  

    btn_accept = "✅ Да, Я разрешаю!"
    btn_dicline = "*️⃣ Нет!"

    def kb():
        return ReplyKeyboardMarkup(
            one_time_keyboard=True,
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton(Pub_video.btn_accept), KeyboardButton(Pub_video.btn_dicline)],
                [Tbase.Back.btn()]
            ]
        )

success = """
✅ Проверьте анкету и отправьте на модерацию администратору!
"""
