from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters.state import (
    StatesGroup, State
)


UserCall = CallbackData(
    "payment", 
    "action", 
    "from_id", 
    "to_id", 
    "page"
)



class UserState(StatesGroup):


    payment = State()
    data = State()
