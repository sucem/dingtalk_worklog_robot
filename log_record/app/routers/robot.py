from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from ..dependencies.robot import validate_robot_received_msg

router = APIRouter()


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
        print(f"receive msg: {msg.text.content}")
    else:
        raise HTTPException(status_code=500, detail="sign incorrected!")
