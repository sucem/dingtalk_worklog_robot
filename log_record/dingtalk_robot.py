from typing import Protocol

from .domains import WorkLog

class Repository(Protocol):
    def save(self, work_log: WorkLog):
        pass


class DingTalkRobot():
    def __init__(self, repo: Repository):
        self.repo = repo

    def save(self, work_log: WorkLog):
        self.repo.save(work_log)
