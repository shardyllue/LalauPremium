from asyncio import create_task, get_event_loop
from aiogram import executor
from loguru import logger

from utils import schedular_main

from core import Dispatcher, dp
from core.middleware import TelegramMiddleware

from db import Session, SessionPosting

from handler import dp

async def on_startup(dp : Dispatcher):
    logger.info("Start up")
    dp.middleware.setup(TelegramMiddleware(
        Session
    ))

async def on_shutdown(dp : Dispatcher):
    logger.info("Shutdown down")


if __name__ == "__main__":
    executor.start_polling(
        dispatcher=dp,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
    )