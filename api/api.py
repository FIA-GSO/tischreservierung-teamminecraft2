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


def get_request_date_or_error() -> Union[Response, datetime]:
    if 'now' in request.args:
        return datetime.now().replace(minute=30)
    raw_date = request.args.get('at')
    if raw_date is None:
        error = {'error': 'request argument "?at=yy-mm-dd hh:mm" or "?now" is not specified'}
        return json_error(error)
    if not isinstance(raw_date, str):
        error = {'error': 'request argument "?at=yy-mm-dd hh:mm" must be a str.', 'at': raw_date}
        return json_error(error)
    try:
        return datetime.strptime(raw_date.strip("\""), '%Y-%m-%d %H:%M')
    except ValueError:
        error = {'error': 'the date in the "?at=yy-mm-dd hh:mm" argument is not a valid datetime.', 'at': raw_date}
        return json_error(error)


if __name__ == '__main__':
    app = flask.Flask(__name__)
    app.config["DEBUG"] = True


    @app.get('/api/v1/tables')
    def tables():
        return json.dumps(get_all_tables())


    @app.get('/api/v1/free-tables')
    def free_tables():
        date = get_request_date_or_error()
        if isinstance(date, Response):
            return date
        return json.dumps(get_free_tables(date))


    @app.post('/api/v1/table/reserve')
    def reserve_table():
        date = get_request_date_or_error()
        if not isinstance(date, datetime):
            return date
        if date.minute != 30:
            return json_error(
                {'error': 'tables can only be reserved every hour at minute 30',
                 'at': date.strftime('%Y-%m-%d %H:%M'),
                 'min': date.minute})
        possible_choices = get_free_tables(date)
        if not possible_choices:
            return json_error({'error': 'no free tables at requested time', 'at': date.strftime('%Y-%m-%d %H:%M')})
        table = random.choice(possible_choices)
        # Todo reserve in database
        return json.dumps(table)

    @app.get('/api/v1/coffee')
    def coffee():
        return json_error({'error': 'i am a teapot'}, status=418)

    @app.get('/api/v1/tea')
    def tea():
        return json_response({'response': 'yes'}, status=418)


    app.run()
