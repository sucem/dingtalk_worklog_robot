import os
from fastapi import FastAPI
from dotenv import load_dotenv
from tinydb import TinyDB

from .routers import robot


def init():
    """side effect"""
    load_dotenv()


app_sec = os.environ.get('app_sec')
app_key = os.environ.get('app_key')

if app_sec == None or app_key == None:
    raise ValueError('app_sec or app_key can not be none!')
    os.exit(1)

tiny_db_path = os.environ.get('tiny_db')
if tiny_db_path == None:
    tiny_db_path = '.data/tiny_db.json'

tiny_db = TinyDB(tiny_db_path)


init()
app = FastAPI()
app.include_router(router=robot.router)


@app.get('/')
def root():
    return {"message": "钉钉机器人服务端"}
