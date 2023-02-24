from datetime import datetime
import os

from fastapi import Depends, HTTPException, Header
from tinydb import TinyDB
from log_record.dingtalk_robot import DingTalkRobot

from log_record.repositories import FileRepository

from . import secret


class AppEnviron:
    """AppEnviron is  Denpend class.
    Read environment."""

    app_sec: str
    app_key: str
    tiny_db = "data/database.json"

    def __init__(self) -> None:
        app_key = os.environ.get("app_key")
        app_sec = os.environ.get("app_sec")

        if app_key is None or app_sec is None:
            raise ValueError("can not read app_key or app_sec environment")
        else:
            self.app_key = app_key
            self.app_sec = app_sec

        if (tiny_db := os.environ.get("tiny_db_path")) != None:
            self.tiny_db = tiny_db


def _validate_time(timestamp_now: datetime, msg_timestamp: datetime) -> bool:
    """validate_date 返回时间戳之间的间隔是否在60分钟以上"""
    return (timestamp_now - msg_timestamp).seconds < 1 * 60 * 60


def _validate_robot_sign(timestamp: int, app_sec: str, sign: str) -> bool:
    """validate_robot_sign 检查头里面的 sign 和根据 timestamp, app_sec 计算出来的结果是否相等"""
    return sign.encode("utf-8") == secret.cal_sign(str(timestamp), app_sec)


def validate_robot_received_msg(
    timestamp: int = Header(),
    sign: str = Header(),
    app_env: AppEnviron = Depends(AppEnviron),
):
    """validate_robot_received_msg check the msg from user.
    return the msg wheather correct"""

    current_time = datetime.now()
    msg_time = datetime.fromtimestamp(timestamp / 1000)  # 精确到秒

    if app_env.app_sec is None:
        raise HTTPException(status_code=400, detail="app_sec or app_key is none")

    if not _validate_time(current_time, msg_time) or not _validate_robot_sign(
        timestamp, app_env.app_sec, sign
    ):
        raise HTTPException(status_code=400, detail="validate sign failure")


def create_db(app_env: AppEnviron = Depends()):
    db = TinyDB(app_env.tiny_db)
    yield db
    db.close()


def create_dingtalk_robot(db: TinyDB = Depends(create_db)):
    return DingTalkRobot(FileRepository(db))
