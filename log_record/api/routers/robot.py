from datetime import datetime
from dotenv import load_dotenv


from fastapi import APIRouter, Depends
from pydantic import BaseModel


from log_record.dingtalk_robot import DingTalkRobot
from log_record.modules import WorkLog

from ..dependencies.dingtalk.robot import (
    create_dingtalk_robot,
    validate_robot_received_msg,
)


class RobotMsgContent(BaseModel):
    content = ""


class RobotMsg(BaseModel):
    msgtype: str
    conversationId: str
    text: RobotMsgContent
    senderNick: str


router = APIRouter()
load_dotenv()


@router.post(
    "/robot",
    tags=["dingtalk robot"],
    description="receive robot msg router",
)
def receive_robot_msg(
    msg: RobotMsg,
    dingtalk_robot: DingTalkRobot = Depends(create_dingtalk_robot),
):
    wl = dingtalk_robot.save(
        WorkLog(
            content=msg.text.content,
            record_time=datetime.now(),
            nick_name=msg.senderNick,
        )
    )

    return wl
