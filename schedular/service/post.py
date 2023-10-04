from lalau import logger

from lalau import Session, bot
from lalau.base import AppTable

from utils.config import PUBLIC_GROUP
from utils.post import get_post_app

import template


async def post_app(app : AppTable):
    """
    
    Отправка поста в группу
    
    """
    me = await bot.get_me()

    caption = template.post.text.format(app=app)
    markup = template.post.kb(app.user_id, me.username)

    await bot.send_photo(
        chat_id=PUBLIC_GROUP,
        photo=app.photo_id,
        caption=caption,
        reply_markup=markup
    )

    # await bot.send_message(
    #     chat_id=PUBLIC_GROUP,
    #     text=caption,
    #     reply_markup=markup
    # )

async def post():
    """
    The posting apps at public group
    """

    logger.log("POST", "Posting")

    async with Session() as session:

        logger.log("POST", "Getting a post app")
        app = await get_post_app(session)


    logger.log("POST", "Sending the post app")
    await post_app(app)    

