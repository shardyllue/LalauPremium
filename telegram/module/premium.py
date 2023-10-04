from aiogram.utils.callback_data import CallbackData


bandCall = CallbackData(
    "premium.band", 
    "action", 
    "page",
    "gender",
)

appCall = CallbackData(
    "premium.app", 
    "action", 
    "user_id", 
    "page",
)

moderCall = CallbackData(
    "premium.moder", 
    "action", 
    "page",
    "gender",
    "user_id"
)

