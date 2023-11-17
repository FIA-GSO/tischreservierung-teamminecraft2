import sqlite3
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from sqlite3 import Cursor
from typing import List, Any, Dict


def get_all_tables():
    with DbConnection() as cursor:
        return cursor.execute(_sql_script('all_tables.sql')).fetchall()


def get_free_tables(time: datetime):
    with DbConnection() as cursor:
        return cursor.execute(_sql_script('free_tables.sql'), (time,)).fetchall()


def insert_reservation(time: datetime, table: int, pin: int):
    with DbConnection(commit=True) as cursor:
        cursor.execute(_sql_script('insert_reservation.sql'), (time, table, pin))


@lru_cache()
def _sql_script(name: str) -> str:
    path = _sql_path() / name
    with open(path, mode='r', encoding='utf-8') as file:
        return file.read()


def _project_dir() -> Path:
    return Path(__file__).parent.parent


def _sql_path() -> Path:
    return _project_dir() / 'sql'


class DbConnection:

    ROW_NAME_MAPPING: Dict[str, str] = {
        'tischnummer': 'table_id',
        'anzahlPlaetze': 'persons'
    }

    def __init__(self, commit: bool = False):
        self.connection = sqlite3.connect(_project_dir() / 'buchungssystem.sqlite')
        self.connection.row_factory = self._dict_factory
        self.commit = commit

    def __enter__(self):
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        no_error_occurred = exc_type is None and exc_val is None and exc_tb is None
        if self.commit and no_error_occurred:
            self.connection.commit()
        self.connection.close()

    def _dict_factory(self, cursor: Cursor, row: List[Any]) -> Dict[str, Any]:
        return dict(zip((self.ROW_NAME_MAPPING[description[0]] for description in cursor.description), row))
