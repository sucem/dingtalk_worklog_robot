from datetime import datetime

from fastapi import Depends, File, Header
from tinydb import TinyDB
from log_record.dingtalk_robot import DingTalkRobot

from log_record.repositories import FileRepository

from . import secret
from .router import AppEnviron


def _validate_time(timestamp_now: datetime, msg_timestamp: datetime) -> bool:
    """validate_date 返回时间戳之间的间隔是否在60分钟以上"""
    return (timestamp_now - msg_timestamp).seconds < 1 * 60 * 60


def _validate_robot_sign(timestamp: int, app_sec: str, sign: str):
    """validate_robot_sign 检查头里面的 sign 和根据 timestamp, app_sec 计算出来的结果是否相等"""
    return sign.encode("utf-8") == secret.cal_sign(str(timestamp), app_sec)


def validate_robot_received_msg(
    timestamp: int = Header(),
    sign: str = Header(),
    app_env: AppEnviron = Depends(AppEnviron),
) -> bool:
    """validate_robot_received_msg check the msg from user.
    return the msg wheather correct"""

    current_time = datetime.now()
    msg_time = datetime.fromtimestamp(timestamp / 1000)  # 精确到秒

    if app_env.app_sec is None:
        raise ValueError("app secret is none")

    return _validate_time(
        timestamp_now=current_time, msg_timestamp=msg_time
    ) and _validate_robot_sign(timestamp, app_env.app_sec, sign)


def create_db(app_env: AppEnviron = Depends()):
    db = TinyDB(app_env.tiny_db)
    yield db
    db.close()


def create_dingtalk_robot(db: TinyDB = Depends(create_db)):
    return DingTalkRobot(FileRepository(db))
