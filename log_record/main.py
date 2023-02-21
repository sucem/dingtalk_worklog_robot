from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Header
from pydantic import BaseModel

from . import secret


def validate_time(timestamp_now: datetime, req_timestamp: datetime) -> bool:
    """validate_date 返回时间戳之间的间隔是否在60分钟以上"""
    return (timestamp_now - req_timestamp).seconds > 1 * 60 * 60


def validate_robot_sign(timestamp: int, sign: str):
    """validate_robot_sign 检查头里面的 sign 和根据 timestamp 已经 app_sec 计算出来的结果是否相等"""
    return sign.encode('utf-8') == secret.cal_sign(str(timestamp), "")


def validate_robot_received_msg(timestamp: int = Header(), sign: str = Header()):
    """ validate_robot_received_msg 检查机器人收到的消息是否合法 """
    current_time = datetime.now()
    msg_time = datetime.fromtimestamp(timestamp/1000)  # 精确到秒

    return validate_time(current_time, msg_time) and validate_robot_sign(timestamp, sign)


class RobotMsgContent(BaseModel):
    content: str


class RobotMsg(BaseModel):
    msgtype: str
    conversationId: str
    text: Optional[RobotMsgContent]
    senderNick: str


app = FastAPI()


@app.post("/robot")
def receive_robot_msg(msg: RobotMsg,
                      timestamp: int = Header(default=None),
                      sign: str = Header(default=None)):
    if msg.text is not None:
        print(f"timestamp: {timestamp}")
        print(f"sign: {sign}")
        print(
            f"receive msg: {msg.text.content}, from {msg.senderNick}, in {msg.conversationId}")

        cal_sign = secret.cal_sign(str(
            timestamp), "g_VSgB9tbLIR3d9aXYeGL8oT8ZSgrIBkc2_2BjeCZvSA50ut3gZ2HAK7Jjsiyh_s")
        print(f"the calced sign is: {cal_sign}")
        print(f"{sign.encode('utf-8') == cal_sign}")
    else:
        print("receive msg error")
