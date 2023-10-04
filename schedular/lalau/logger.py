from loguru import logger

logger.level("POST", no=38, color="<yellow>", icon="post")
logger.level("SCORE", no=38, color="<yellow>", icon="score")

logger.add(sink="logs/score.log", 
    format="{time} {level} {message}", 
    level="SCORE",
)

logger.add(sink="logs/post.log", 
    format="{time} {level} {message}", 
    level="POST",
)

