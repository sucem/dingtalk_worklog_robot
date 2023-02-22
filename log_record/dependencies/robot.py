from datetime import datetime
import os

from fastapi import Header
from . import secret

def validate_time(timestamp_now: datetime, req_timestamp: datetime) -> bool:
    """validate_date 返回时间戳之间的间隔是否在60分钟以上"""
    return (timestamp_now - req_timestamp).seconds < 1 * 60 * 60


def validate_robot_sign(timestamp: int, app_sec: str, sign: str):
    """validate_robot_sign 检查头里面的 sign 和根据 timestamp, app_sec 计算出来的结果是否相等"""
    return sign.encode('utf-8') == secret.cal_sign(str(timestamp), app_sec)


def validate_robot_received_msg(timestamp: int = Header(),
                                sign: str = Header()):
    """ validate_robot_received_msg 检查机器人收到的消息是否合法 """
    current_time = datetime.now()
    msg_time = datetime.fromtimestamp(timestamp/1000)  # 精确到秒
    app_sec = os.environ.get('app_sec')
