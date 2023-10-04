from os import environ

from dotenv import load_dotenv


load_dotenv()


PG_URL = environ.get("PG_URL")
PUBLIC_GROUP = int(environ.get("PUBLIC_GROUP_ID"))
TOKEN = environ.get("TOKEN")