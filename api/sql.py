import functools
import sqlite3
from datetime import datetime
from sqlite3 import Cursor, Connection
from typing import List, Any, Dict


def dict_factory(cursor: Cursor, row: List[Any]) -> Dict[str, Any]:
    return dict(zip(cursor.description, row))


def get_all_tables():
    return _cursor().execute(_all_tables_statement()).fetchall()


@functools.lru_cache
def _all_tables_statement() -> str:
    with open('sql/all_tables.sql', mode='r', encoding='utf8') as file:
        return file.read()


def get_free_tables(time: datetime):
    return _cursor().executescript(_free_tables_statement()).fetchall()


@functools.lru_cache
def _free_tables_statement() -> str:
    with open('sql/free_tables.sql', mode='r', encoding='utf8') as file:
        return file.read()


def _cursor() -> Cursor:
    return _database().cursor()


@functools.lru_cache
def _database() -> Connection:
    connection = sqlite3.connect('buchungssystem.sqlite')
    return connection
