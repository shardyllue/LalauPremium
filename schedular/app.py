import asyncio
from asyncio import sleep

import aioschedule
from fastapi import FastAPI
from lalau import logger
from service import post, score
# from endpoint import routers


app = FastAPI()
# app.include_router(routers)


async def run_pending():

    aioschedule.every(3).seconds.do(post)
    aioschedule.every().day.at("12:00").do(score)

    logger.info("Running pending")

    while True:
        await aioschedule.run_pending()
        await sleep(1)

        
@app.on_event("startup")
async def on_startup():
   
    loop = asyncio.get_running_loop()
    loop.create_task(run_pending())








    




