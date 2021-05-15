import json
import logging
import os
import threading

from flask import Flask, jsonify, request

import settings

from database.db_client import DBTable
from utils.logging_utils import set_up_logger
from utils.json_utils import json_response_error, json_response_data

app = Flask(__name__)
os.environ['WERKZEUG_RUN_MAIN'] = 'true'
table_last_names = DBTable('first_name', 'last_name')


@app.route('/last_name/<first_name>', methods=['GET'])
def get_user_last_name(first_name):
    if last_name := table_last_names.select(first_name=first_name):
        return json_response_data(last_name[0]), 200
    else:
        return json_response_error('Entry does not exists',
                                   f'Last name for user with first name "{first_name}" not found'), 404


@app.route('/last_name', methods=['POST'])
def set_user_last_name():
    try:
        data = json.loads(request.data)
    except json.JSONDecodeError:
        return json_response_error('Invalid request',
                                   'Client sent a request that this server could not understand'), 400

    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if not first_name or not last_name:
        return json_response_error(
            'Invalid request', 'Request data is missing. Expected "first_name" and "last_name"'), 400

    if len(table_last_names.select(first_name=first_name, last_name=last_name)) == 0:
        user = table_last_names.insert(first_name=first_name, last_name=last_name)
        return json_response_data(user), 201
    else:
        return json_response_error(
            'User exists', f'User with first name "{first_name}" and last name "{last_name}" already exists.'), 409


@app.route('/last_name/<first_name>', methods=['PUT'])
def update_user_last_name(first_name):
    try:
        data = json.loads(request.data)
    except json.JSONDecodeError:
        return json_response_error('Invalid request',
                                   'Client sent a request that this server could not understand'), 400
    last_name = data.get('last_name')

    if not last_name:
        return json_response_error(
            'Invalid request', 'Request data is missing. Expected "last_name"'), 400

    users = table_last_names.select(first_name=first_name)
    if len(users) == 0:
        return json_response_error(
            f'User not found', f'Last name for user with first name "{first_name}" not found'), 404

    user = users[0]
    table_last_names.update(first_name=first_name, last_name=last_name, entry_id=user['id'])
    user = table_last_names.select(entry_id=user['id'])

    return json_response_data(user), 201


@app.route('/last_name/<first_name>', methods=['DELETE'])
def delete_user_last_name(first_name):
    users = table_last_names.select(first_name=first_name)
    if len(users) == 0:
        return json_response_error(
            f'User not found', f'Last name for user with first name "{first_name}" not found'), 404

    user = users[0]

    table_last_names.delete(entry_id=user['entry_id'])
    return json_response_data('OK'), 201


def run_mock():
    server = threading.Thread(target=_run_mock_in_thread, kwargs={
        'host': settings.MOCK_SETTINGS.HOST,
        'port': settings.MOCK_SETTINGS.PORT,
        'app': app
    })
    server.start()
    return server


def _run_mock_in_thread(*args, **kwargs):
    if 'app' in kwargs:
        current_app = kwargs.pop('app')
    else:
        current_app = app

    app_logger = logging.getLogger('werkzeug')
    set_up_logger(app_logger, settings.MOCK_SETTINGS.FLASK_LOG_FILE_PATH, log_format=settings.FLASK_SETTINGS.LOG_FORMAT)
    set_up_logger(current_app.logger, settings.MOCK_SETTINGS.LOG_FILE_PATH)

    current_app.run(*args, **kwargs)


def shutdown_mock():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()


@app.route('/shutdown')
def shutdown():
    shutdown_mock()
    return json_response_data(f'OK, exiting'), 200
