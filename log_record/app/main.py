import os
from fastapi import FastAPI
from dotenv import load_dotenv

from .routers import robot


def init():
    """side effect"""
    load_dotenv()


init()
app = FastAPI()
app.include_router(router=robot.router)


@app.get('/')
def root():
    return {"message": "钉钉机器人服务端"}
