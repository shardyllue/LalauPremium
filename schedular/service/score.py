from datetime import datetime
from calendar import monthrange

from lalau import Session, logger
from utils.score import clean_score


def is_last_data():
    
    now = datetime.now()
    last_day_month = monthrange(now.year, now.month)[-1]
    return now.day == last_day_month, now, last_day_month


async def score():

    logger.log("SCORE", "Score")

    if not (it:=is_last_data())[0]:
        return logger.log("SCORE", f"Is not last day. Day is {it[1].day}. Last day at {it[1].year}-{it[1].month}-{it[2]}")
    
    logger.log("SCORE", "Clean everybody the score")

    async with Session() as session:
        await clean_score(session)





