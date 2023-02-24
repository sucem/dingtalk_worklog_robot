import logging
from datetime import datetime
from dotenv import load_dotenv

import requests
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel


from log_record.dingtalk_robot import DingTalkRobot
from log_record.modules import WorkLog

from ..dependencies.dingtalk.robot import (
    create_dingtalk_robot,
    validate_robot_received_msg,
)
from ..dependencies.dingtalk.router import AppEnviron


class RobotMsgContent(BaseModel):
    content = ""


class RobotMsg(BaseModel):
    msgtype: str
    conversationId: str
    text: RobotMsgContent
    senderNick: str


router = APIRouter()
load_dotenv()


@router.post("/robot", tags=["dingtalk robot"], description="webhook for receive msg")
def receive_robot_msg(
    msg: RobotMsg,
    validated: bool = Depends(validate_robot_received_msg),
    app_env: AppEnviron = Depends(),
    dingtalk_robot: DingTalkRobot = Depends(create_dingtalk_robot),
):
    logging.debug(f"receive msg: {msg.text.content} from {msg.senderNick}")

    if validated:
        wl = dingtalk_robot.save(
            WorkLog(
                content=msg.text.content,
                record_time=datetime.now(),
                nick_name=msg.senderNick,
            )
        )
        logging.info(f"saved {wl.content} from {wl.nick_name}")

        token = dingtalk_robot.get_usertoken(
            app_env.app_key, app_env.app_sec, requester=requests.get
        )
        if token is None:
            logging.error("get token failure")
            raise HTTPException(status_code=400, detail="get user token failure")
        else:
            logging.debug(f"get token success: {token}")

    else:
        raise HTTPException(status_code=500, detail="sign incorrected!")
