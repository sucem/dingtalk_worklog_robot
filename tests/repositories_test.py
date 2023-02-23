from datetime import datetime
from tinydb import Query, TinyDB
from tinydb.storages import MemoryStorage
from log_record.modules import WorkLog

from log_record.repositories import FileRepository

def test_file_repostory_save_worklog():
    db = TinyDB(storage=MemoryStorage)
    repo = FileRepository(db)

    work_log = WorkLog(content="content", nick_name="foo", record_time=datetime.now())
    repo.save(work_log)

    assert len(db.all()) == 1

    WorkLogQuery = Query()
    result = db.search(WorkLogQuery.nick_name == "foo")[0]

    assert result['content'] == "content"
    assert result['nick_name'] == "foo"
