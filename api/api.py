import json
import random
from datetime import datetime
from typing import Union, Any

import flask
from flask import request, Response

from sql import get_all_tables, get_free_tables


def json_error(obj: Any, status=400) -> Response:
    return json_response(obj, status)


def json_response(obj: Any, status=200) -> Response:
    return Response(json.dumps(obj), status)


def get_request_date() -> Union[Response, datetime]:
    raw_date = request.args.get('at')
    if raw_date is None:
        error = {'error': 'request argument "?at=yy-mm-dd hh:mm" is not specified'}
        return json_response(error, status=400)
    if not isinstance(raw_date, str):
        error = {'error': 'request argument "?at=yy-mm-dd hh:mm" must be a str.', 'at': raw_date}
        return json_response(error, status=400)
    try:
        return datetime.fromisoformat(raw_date.strip("\""))
    except ValueError:
        error = {'error': 'the date in the "?at=yy-mm-dd hh:mm" argument is not a valid datetime.', 'at': raw_date}
        return json_response(error, status=400)


if __name__ == '__main__':
    app = flask.Flask(__name__)
    app.config["DEBUG"] = True


    @app.get('/api/v1/tables')
    def tables():
        return json.dumps(get_all_tables())


    @app.get('/api/v1/free-tables')
    def free_tables():
        date = get_request_date()
        if isinstance(date, Response):
            return date
        return json.dumps(get_free_tables(date))


    @app.post('/api/v1/table/reserve')
    def reserve_table():
        date = get_request_date()
        if isinstance(date, Response):
            return date
        if date.minute != 30:
            error = {'error': 'tables can only be reserved every hour at minute 30',
                     'at': date.strftime('%Y-%m-%d %H:%M'),
                     'min': date.minute}
            return json_error(error)
        possible_choices = get_free_tables(date)
        if not possible_choices:
            error = {'error': 'no free tables at requested time', 'at': date.strftime('%Y-%m-%d %H:%M')}
            return json_error(error)
        table = random.choice(possible_choices)
        # Todo reserve in database
        return json.dumps(table)


    app.run()
