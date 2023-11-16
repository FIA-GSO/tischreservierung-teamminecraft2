import sqlite3
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from sqlite3 import Cursor
from typing import List, Any, Dict


def dict_factory(cursor: Cursor, row: List[Any]) -> Dict[str, Any]:
    return dict(zip(cursor.description, row))


def get_all_tables():
    return _cursor().execute(_sql_script('all_tables.sql')).fetchall()


def get_free_tables(time: datetime):
    return _cursor().execute(_sql_script('free_tables.sql'), (time,)).fetchall()


@lru_cache()
def _sql_script(name: str) -> str:
    path = _sql_path() / name
    with open(path, mode='r', encoding='utf-8') as file:
        return file.read()


def _sql_path() -> Path:
    return Path(__file__).parent.parent / 'sql'


def _cursor() -> Cursor:
    connection = sqlite3.connect('buchungssystem.sqlite')
    return connection.cursor()
