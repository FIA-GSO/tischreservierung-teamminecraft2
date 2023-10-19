import flask
from flask import request   # wird benötigt, um die HTTP-Parameter abzufragen
from flask import jsonify   # übersetzt python-dicts in json
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True  # Zeigt Fehlerinformationen im Browser, statt nur einer generischen Error-Message

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def eval_bool_arg(arg_value) -> None|bool:
    if isinstance(arg_value, str) and arg_value.lower() in ['true', '1']:
        return True
    return False

@app.route('/api/v1/table', methods=['GET'])
def home():
    if request.method == 'GET':
        query = 'SELECT * FROM tische t'
        if eval_bool_arg(request.args.get('free-tables')) == True:
            # extend query to only match free tables
            pass

        connection = sqlite3.connect('buchungssystem.sqlite')
        connection.row_factory = dict_factory
        cursor = connection.cursor()
        return jsonify(cursor.execute(query).fetchall())

app.run()