import json
from datetime import datetime

import flask
from flask import jsonify  # übersetzt python-dicts in json
from flask import request  # wird benötigt, um die HTTP-Parameter abzufragen

from sql import get_all_tables, get_free_tables

if __name__ == '__main__':
    app = flask.Flask(__name__)
    app.config["DEBUG"] = True  # Zeigt Fehlerinformationen im Browser, statt nur einer generischen Error-Message


    @app.get('/api/v1/tables')
    def tables():
        return jsonify(get_all_tables())


    @app.get('/api/v1/free-tables')
    def free_tables():
        raw_date = request.args.get('at')
        if raw_date is None:
            error = {'error': 'request argument "?at=yy-mm-dd hh:mm" is not specified'}
            return app.response_class(json.dumps(error), status=400)
        if not isinstance(raw_date, str):
            error = {'error': 'request argument "?at=yy-mm-dd hh:mm" must be a str.', 'at': raw_date}
            return app.response_class(json.dumps(error), status=400)
        try:
            date = datetime.fromisoformat(raw_date.strip("\""))
        except ValueError:
            error = {'error': 'the date in the "?at=yy-mm-dd hh:mm" argument is not a valid datetime.', 'at': raw_date}
            return app.response_class(json.dumps(error), status=400)
        return jsonify(get_free_tables(date))


    app.run()
