"""使用 tinydb 存储工作日志
"""

from logging import exception
from typing import Any, Dict

from tinydb import TinyDB

from log_record.modules import WorkLog


class FileRepository:
    """使用 tinydb 的将日志文件的 json 写入到文件中"""

    def __init__(self, db: TinyDB) -> None:
        self.db = db

    def save(self, work_log: WorkLog) -> WorkLog:
        """save work_log object to the tinydb.
        return saved work_log info"""

        self.db.insert(
            {
                "content": work_log.content,
                "record_time": work_log.record_time.timestamp(),
                "nick_name": work_log.nick_name,
            }
        )

        return work_log
