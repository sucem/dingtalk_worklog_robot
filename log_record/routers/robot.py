from fastapi import APIRouter, Depends
from pydantic import BaseModel

from log_record.dependencies.robot import validate_robot_received_msg

router = APIRouter()


class RobotMsgContent(BaseModel):
    content = ""


class RobotMsg(BaseModel):
    msgtype: str
    conversationId: str
    text: RobotMsgContent
    senderNick: str


@router.post('/robots')
def receive_robot_msg(msg: RobotMsg, validated: bool = Depends(validate_robot_received_msg)):
    if validated:
        print(f"receive msg: {msg.text.content}")
    else:
        raise
