import os
from fastapi import FastAPI
from dotenv import load_dotenv
from tinydb import TinyDB

from .routers import robot





app = FastAPI()
app.include_router(router=robot.router)


@app.get('/')
def root():
    return {"message": "钉钉机器人服务端"}
