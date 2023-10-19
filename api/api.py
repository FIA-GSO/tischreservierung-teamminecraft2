import flask
from flask import request   # wird benötigt, um die HTTP-Parameter abzufragen
from flask import jsonify   # übersetzt python-dicts in json

from datetime import datetime
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True  # Zeigt Fehlerinformationen im Browser, statt nur einer generischen Error-Message

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_bool_arg(arg_value) -> None|bool:
    if isinstance(arg_value, str) and arg_value.lower() in ['true', '1']:
        return True
    return False

def get_datetime_arg(arg_value) -> None|datetime:
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
            query += ' WHERE tischnummer NOT IN('
            query += ' SELECT DISTINCT r.tischnummer'
            query += ' FROM reservierungen r'
            query += ' WHERE (Datetime(\'now\', \'localtime\') BETWEEN r.zeitpunkt AND Datetime(r.zeitpunkt, \'+60 minutes\')) and r.storniert != True)'
            #return jsonify(query)
            pass

        connection = sqlite3.connect('buchungssystem.sqlite')
        connection.row_factory = dict_factory
        cursor = connection.cursor()
        return jsonify(cursor.execute(query).fetchall())

app.run()