from datetime import datetime

import flask
from flask import jsonify  # übersetzt python-dicts in json
from flask import request  # wird benötigt, um die HTTP-Parameter abzufragen

from sql import get_all_tables, get_free_tables


if __name__ == '__main__':
    app = flask.Flask(__name__)
    app.config["DEBUG"] = True  # Zeigt Fehlerinformationen im Browser, statt nur einer generischen Error-Message

    @app.get('/api/v1/table')
    def home():
        raw_date = request.args.get('free-at')
        try:
            date = datetime.fromisoformat(raw_date)
            return jsonify(get_free_tables(date))
        except (TypeError, ValueError):
            return jsonify(get_all_tables())

    app.run()
