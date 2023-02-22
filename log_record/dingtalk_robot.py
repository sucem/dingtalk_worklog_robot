from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass
class WorkLog():
    content: str
    record_time: datetime
    nick_name: str


class Repository(Protocol):
    def save(self, work_log: WorkLog):
        pass


class DingTalkRobot():
    def __init__(self, repo: Repository):
        self.repo = repo

    def save(self, work_log: WorkLog):
        self.repo.save(work_log)
