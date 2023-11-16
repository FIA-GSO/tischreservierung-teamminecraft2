import json
import random
from datetime import datetime
from typing import Union, Tuple

import flask
from flask import request, Response

from sql import get_all_tables, get_free_tables, insert_reservation

TABLE_ID: int = 0
TABLE_PERSONS: int = 1

DATE_FORMAT: str = '%Y-%m-%d %H:%M'


def get_request_date_or_error(data: dict) -> Union[Tuple[str, int], datetime]:
    if 'now' in data:
        return datetime.now().replace(minute=30)
    raw_date = data.get('at')
    if raw_date is None:
        error = {'error': 'request argument "?at=yy-mm-dd hh:mm" or "?now" is not specified'}
        return json.dumps(error), 400
    if not isinstance(raw_date, str):
        error = {'error': 'request argument "?at=yy-mm-dd hh:mm" must be a str.', 'at': raw_date}
        return json.dumps(error), 400
    try:
        return datetime.strptime(raw_date.strip("\""), DATE_FORMAT)
    except ValueError:
        error = {'error': 'the date in the "?at=yy-mm-dd hh:mm" argument is not a valid datetime.', 'at': raw_date}
        return json.dumps(error), 400


def generate_pin() -> int:
    return random.randint(1000, 9999)


if __name__ == '__main__':
    app = flask.Flask(__name__)
    app.config["DEBUG"] = True


    @app.get('/api/v1/tables')
    def tables():
        return json.dumps(get_all_tables())


    @app.get('/api/v1/free-tables')
    def free_tables():
        date = get_request_date_or_error(request.args)
        if isinstance(date, Response):
            return date
        return json.dumps(get_free_tables(date))


    @app.post('/api/v1/table/reserve')
    def reserve_table():
        date = get_request_date_or_error(request.json)
        if not isinstance(date, datetime):
            return date
        if date < datetime.now():
            error = {'error': 'date is in the past',
                     'at': date.strftime(DATE_FORMAT)}
            return json.dumps(error), 400
        if date.minute != 30:
            error = {'error': 'tables can only be reserved every hour at minute 30',
                     'at': date.strftime(DATE_FORMAT),
                     'min': date.minute}
            return json.dumps(error), 400
        persons = request.json.get('persons')
        if persons is None:
            error = {'error': 'persons not provided'}
            return json.dumps(error), 400
        if not isinstance(persons, int):
            error = {'error': 'persons has to be an integer'}
            return json.dumps(error), 400
        persons = int(persons)
        possible_choices = (table for table in get_free_tables(date) if table[TABLE_PERSONS] >= persons)
        possible_choices_sorted = sorted(possible_choices, key=lambda table: table[TABLE_PERSONS])
        if not possible_choices_sorted:
            error = {'error': 'no free tables at requested time', 'at': date.strftime(DATE_FORMAT)}
            return json.dumps(error), 404
        table = possible_choices_sorted[0]
        pin = generate_pin()
        insert_reservation(date, table[TABLE_ID], pin)
        result = {'table_id': table[TABLE_ID],
                  'table_persons': table[TABLE_PERSONS],
                  'requested_persons': persons,
                  'date': date.strftime(DATE_FORMAT),
                  'pin': pin}
        return json.dumps(result), 200


    @app.get('/api/v1/coffee')
    def coffee():
        error = {'error': 'i am a teapot'}
        return json.dumps(error), 418


    @app.get('/api/v1/tea')
    def tea():
        error = {'response': 'yes'}
        return json.dumps(error), 418


    app.run()
