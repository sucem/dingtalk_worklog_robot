from dataclasses import dataclass
from datetime import datetime

@dataclass
class WorkLog():
    """WorkLog is a entry for database stored"""
    content: str
    record_time: datetime
    nick_name: str
