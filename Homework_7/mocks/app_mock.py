import threading

from flask import Flask, jsonify, request

import settings

from database.db_client import DBTable

app = Flask(__name__)

table_last_names = DBTable('first_name', 'last_name')


@app.route('/get_last_name/<first_name>', methods=['GET'])
def get_user_surname(first_name):
    if last_name := table_last_names.select(first_name=first_name):
        return jsonify({"data": last_name[0]}), 200
    else:
        return jsonify({
             "error": 'Entry does not exists',
             "message": f'Last name for user with first name "{first_name}" not found'
        }), 404


def run_mock():
    server = threading.Thread(target=app.run, kwargs={
        'host': settings.MOCK_SETTINGS.HOST,
        'port': settings.MOCK_SETTINGS.PORT
    })
    server.start()
    return server


def shutdown_mock():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()


@app.route('/shutdown')
def shutdown():
    shutdown_mock()
    return jsonify(f'OK, exiting'), 200
