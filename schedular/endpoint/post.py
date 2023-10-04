from typing import Annotated

import aioschedule

from fastapi import APIRouter, Query
from lalau.values import sent_apps

router = APIRouter(prefix="/post")


