import sqlite3
from datetime import datetime
from typing import Optional

import flask
from flask import jsonify  # übersetzt python-dicts in json
from flask import request  # wird benötigt, um die HTTP-Parameter abzufragen

app = flask.Flask(__name__)
app.config["DEBUG"] = True  # Zeigt Fehlerinformationen im Browser, statt nur einer generischen Error-Message


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_bool_arg(arg_value) -> Optional[bool]:
    if isinstance(arg_value, str) and arg_value.lower() in ['true', '1']:
        return True
    return False


def get_datetime_arg(arg_value) -> Optional[datetime]:
    try:
        return datetime.fromisoformat(arg_value)
    except (TypeError, ValueError):
        return None


@app.route('/api/v1/table', methods=['GET'])
def home():
    if request.method == 'GET':
        query = 'SELECT * FROM tische t'
        if get_datetime_arg(request.args.get('free-at')) != None:
            # only return tables that are free until at least 1 hour from the given datetime
            # extend query to only match qualifying tables
            pass

        connection = sqlite3.connect('buchungssystem.sqlite')
        connection.row_factory = dict_factory
        cursor = connection.cursor()
        return jsonify(cursor.execute(query).fetchall())


app.run()
