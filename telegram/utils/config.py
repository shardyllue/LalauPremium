from dotenv import load_dotenv
from os import environ

load_dotenv()

TOKEN = environ.get("TOKEN")

PG_URL = environ.get("PG_URL")

MODER_GROUP = int(environ.get("MODER_GROUP_ID"))
STORAGE_GROUP = int(environ.get("STORAGE_GROUP_ID"))
PUBLIC_GROUP = environ.get("PUBLIC_GROUP_ID")


ALLOW_SYMBOL_RU = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя-_@ "
ALLOW_SYMBOL_EN = "abcdefghijklmnopqrstuvwxyz-_@ "

