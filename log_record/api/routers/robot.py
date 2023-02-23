from datetime import datetime
import os
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, config
import requests
from tinydb import TinyDB
from log_record.dingtalk_robot import DingTalkRobot
from log_record.modules import WorkLog
from alibabacloud_dingtalk.robot_1_0.client import Client as DingTalkClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_dingtalk.robot_1_0 import models as dingtalk_models

from log_record.repositories import FileRepository

from ..main import app_key, app_sec, tiny_db
from ..dependencies.robot import validate_robot_received_msg


router = APIRouter()

repo = FileRepository(tiny_db)
dingtalk_robot = DingTalkRobot(repo)


class RobotMsgContent(BaseModel):
    content = ""


class RobotMsg(BaseModel):
    msgtype: str
    conversationId: str
    text: RobotMsgContent
    senderNick: str


def create_dingtalk_client() -> DingTalkClient:
    config = open_api_models.Config()
    config.protocol = 'https'
    config.region_id = 'central'
    return DingTalkClient(config)


@router.post('/robot', tags=['dingtalk robot'], description="webhook for receive msg")
def receive_robot_msg(msg: RobotMsg, validated: bool = Depends(validate_robot_received_msg)):
    if validated:
        dingtalk_robot.save(WorkLog(content=msg.text.content,
                                    record_time=datetime.now(),
                                    nick_name=msg.senderNick))

        if app_key is None or app_sec is None:
            raise HTTPException(
                status_code=400, detail="app_key or app_secret can not be found")

        token = dingtalk_robot.get_usertoken(
            app_key, app_sec, requester=requests.get)
        if token is None:
            raise HTTPException(
                status_code=400, detail="get user token failure")
        else:
            dingtalk_robot.send_worklog_received_message(
                token,
                conversation_id=msg.conversationId,
                robot_code=app_key,
                client=create_dingtalk_client(),
                model=dingtalk_models,
                util_model=util_models,
            )

    else:
        raise HTTPException(status_code=500, detail="sign incorrected!")
