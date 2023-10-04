from fastapi import APIRouter

from . import post

routers = APIRouter()
routers.include_router(post.router)
