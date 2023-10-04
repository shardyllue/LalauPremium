from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from utils.config import PG_URL

DRIVER = "postgresql+asyncpg://"

engine = create_async_engine(url=DRIVER + PG_URL)
Session = async_sessionmaker(
    bind=engine, 
    autoflush=False, 
    expire_on_commit=False
)