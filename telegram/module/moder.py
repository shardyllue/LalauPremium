from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters.state import (
    StatesGroup, State
)

ModerCall = CallbackData(
    "moder", 
    "action", 
    "user_id"
)

PaymentCall = CallbackData(
    "payment-moder",
    "action",
    "from_id",
    "to_id",
    "page"
)

class PaymentState(StatesGroup):

    count = State()