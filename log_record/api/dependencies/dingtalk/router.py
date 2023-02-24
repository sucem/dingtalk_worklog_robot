"""router contains router scope dependencies"""

import os
from fastapi import Depends
from tinydb import TinyDB
import tinydb


class AppEnviron:
    """AppEnviron is  Denpend class.
    Read environment."""

    app_sec: str
    app_key: str
    tiny_db = "database.json"

    def __init__(self) -> None:
        app_key = os.environ.get("app_key")
        app_sec = os.environ.get("app_sec")

        if app_key is None or app_sec is None:
            raise ValueError("can not read app_key or app_sec environment")
        else:
            self.app_key = app_key
            self.app_sec = app_sec

        if tiny_db := os.environ.get('tiny_db_path') != None:
            self.tiny_db = tiny_db
            


def create_db(tiny_db_path:str = Depends(AppEnviron)):
    return TinyDB(tiny_db_path)
