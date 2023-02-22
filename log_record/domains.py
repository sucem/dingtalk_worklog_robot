from dataclasses import dataclass
from datetime import datetime

@dataclass
class WorkLog():
    content: str
    record_time: datetime
    nick_name: str