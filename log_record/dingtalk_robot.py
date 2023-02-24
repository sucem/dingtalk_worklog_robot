import json
from typing import Any, Callable, Dict, Optional, Protocol

from .modules import WorkLog


class Repository(Protocol):
    def save(self, work_log: WorkLog) -> WorkLog:
        ...


class DingTalkRobot():
    token_url = "https://oapi.dingtalk.com/gettoken?appkey={}&appsecret={}"

    def __init__(self, repo: Repository):
        self.repo = repo

    def save(self, work_log: WorkLog) -> WorkLog:
        """save the work_log object to the repo, return saved work log info"""
        return self.repo.save(work_log)

    # TODO: 可以将 client， model， util_mode 参数去掉, 重构成一个发送对象
    def send_worklog_received_message(self, token: str,
                                      conversation_id: str,
                                      robot_code: str,
                                      client: Any, model: Any, util_model: Any):
        """send_worklog_received_message 会在确认收到消息以后发送一条消息给发送者"""
        send_headers = model.OrgGroupSendHeaders()
        send_headers.x_acs_dingtalk_access_token = token
        send_req = model.OrgGroupSendRequest(
            msg_param=json.dumps({'content': '工作日志已经收到'}, indent=4),
            msg_key="simpleText",
            open_conversation_id=conversation_id,
            robot_code=robot_code
        )

        client.org_group_send_with_options(
            send_req, send_headers, util_model.RuntimeOptions())
