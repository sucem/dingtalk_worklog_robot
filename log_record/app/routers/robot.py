from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from tinydb import TinyDB
from log_record.domains import WorkLog

from log_record.repositories import FileRepository

from ..dependencies.robot import validate_robot_received_msg

router = APIRouter()
db = TinyDB('work_log_db.json')
repo = FileRepository(db)


class RobotMsgContent(BaseModel):
    content = ""


class RobotMsg(BaseModel):
    msgtype: str
    conversationId: str
    text: RobotMsgContent
    senderNick: str


@router.post('/robot', tags=['dingtalk robot'], description="webhook for receive msg")
def receive_robot_msg(msg: RobotMsg, validated: bool = Depends(validate_robot_received_msg)):
    if validated:
        now = datetime.now()
        repo.save(WorkLog(content=msg.text.content,
                          record_time=now,
                          nick_name=msg.senderNick))
    else:
        raise HTTPException(status_code=500, detail="sign incorrected!")
