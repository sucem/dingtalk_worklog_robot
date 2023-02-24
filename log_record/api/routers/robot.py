import logging
from datetime import datetime
import os
from dotenv import load_dotenv

import requests
from alibabacloud_dingtalk.robot_1_0 import models as dingtalk_models
from alibabacloud_dingtalk.robot_1_0.client import Client as DingTalkClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from tinydb import TinyDB

from log_record.dingtalk_robot import DingTalkRobot
from log_record.modules import WorkLog
from log_record.repositories import FileRepository

from ..dependencies.robot import validate_robot_received_msg

router = APIRouter()


class Environs:
    """读取环境变量"""

    app_sec: str
    app_key: str
    tiny_db_path = "./data/tiny_db.json"

    def __init__(self) -> None:
        if (app_key := os.environ.get("app_key")) == None or (
            app_sec := os.environ.get("app_sec")
        ) == None:
            raise SystemError("app_key and app_sec environments can not be none")
        else:
            self.app_key = app_key
            self.app_sec = app_sec

        if db_path := os.environ.get("tiny_db") != None:
            self.tiny_db_path = db_path


logging.basicConfig(level=logging.DEBUG)
load_dotenv()


environs = Environs()
logging.debug(f"db file: {environs.tiny_db_path}")
logging.debug(f"app_sec environment: {environs.app_sec}")
logging.debug(f"app_key environment: {environs.app_key}")

tiny_db = TinyDB(environs.tiny_db_path)

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
    config.protocol = "https"
    config.region_id = "central"
    return DingTalkClient(config)


@router.post("/robot", tags=["dingtalk robot"], description="webhook for receive msg")
def receive_robot_msg(
    msg: RobotMsg, validated: bool = Depends(validate_robot_received_msg)
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
            environs.app_key, environs.app_sec, requester=requests.get
        )
        if token is None:
            logging.error("get token failure")
            raise HTTPException(status_code=400, detail="get user token failure")
        else:
            logging.debug(f"get token success: {token}")

            dingtalk_robot.send_worklog_received_message(
                token,
                conversation_id=msg.conversationId,
                robot_code=environs.app_key,
                client=create_dingtalk_client(),
                model=dingtalk_models,
                util_model=util_models,
            )

    else:
        raise HTTPException(status_code=500, detail="sign incorrected!")
