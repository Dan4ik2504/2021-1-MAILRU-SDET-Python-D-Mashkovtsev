import json
import logging
import os
import threading

from flask import Flask, request

import exceptions
import settings

from database.db_client import DBTable
from utils.logging_utils import set_up_logger
from utils.flask_utils import process_request_response_data

app = Flask(__name__)
os.environ['WERKZEUG_RUN_MAIN'] = 'true'
table_last_names = DBTable('first_name', 'last_name')


@app.route('/last_name/<first_name>', methods=['GET'])
@process_request_response_data()
def get_user_last_name(first_name):
    if last_name := table_last_names.select(first_name=first_name):
        return last_name[0], 200
    else:
        raise exceptions.HTTPNotFoundError('Entry does not exists',
                                           f'Last name for user with first name "{first_name}" not found')


@app.route('/last_name', methods=['POST'])
@process_request_response_data(validate_json=True, required_fields=['first_name', 'last_name'])
def set_user_last_name():
    first_name = request.json['first_name']
    last_name = request.json['last_name']

    if len(first_name) == 0 or len(last_name) == 0:
        raise exceptions.HTTPBadRequestError('Invalid JSON', 'First name and last name are required')

    if len(table_last_names.select(first_name=first_name, last_name=last_name)) == 0:
        user = table_last_names.insert(first_name=first_name, last_name=last_name)
        return user, 201
    else:
        raise exceptions.HTTPConflictError(
            'User exists', f'User with first name "{first_name}" and last name "{last_name}" already exists.')


@app.route('/last_name/<first_name>', methods=['PUT'])
@process_request_response_data(validate_json=True, required_fields=['last_name'])
def update_user_last_name(first_name):
    last_name = request.json['last_name']

    if len(last_name) == 0:
        raise exceptions.HTTPBadRequestError('Invalid JSON', 'Last name is required')

    users = table_last_names.select(first_name=first_name)
    if len(users) == 0:
        raise exceptions.HTTPNotFoundError(
            f'User not found', f'Last name for user with first name "{first_name}" not found')

    user = users[0]
    table_last_names.update(first_name=first_name, last_name=last_name, entry_id=user['entry_id'])
    user = table_last_names.select(entry_id=user['entry_id'])

    return user, 201


@app.route('/last_name/<first_name>', methods=['DELETE'])
@process_request_response_data()
def delete_user_last_name(first_name):
    users = table_last_names.select(first_name=first_name)
    if len(users) == 0:
        raise exceptions.HTTPNotFoundError(
            f'User not found', f'Last name for user with first name "{first_name}" not found')

    user = users[0]

    table_last_names.delete(entry_id=user['entry_id'])
    return 'OK', 200


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
    return f'OK, exiting', 200
