import logging
import os
import requests
from flask import Flask, request

import exceptions
import settings
from database.db_client import DBTable
from utils.flask_utils import process_request_response_data, get_or_http_404, add_rest_api_error_handlers
from utils.logging_utils import set_up_logger

app = Flask(__name__)
add_rest_api_error_handlers(app)

table_users = DBTable('app_users', ['first_name'])

app_logger = logging.getLogger('werkzeug')
set_up_logger(app_logger, settings.APP_SETTINGS.FLASK_LOG_FILE_PATH, log_format=settings.FLASK_SETTINGS.LOG_FORMAT)
set_up_logger(app.logger, settings.APP_SETTINGS.LOG_FILE_PATH)


@app.route('/user', methods=['POST'])
@process_request_response_data(validate_json=True, required_fields=['first_name'])
def create_user():
    first_name = request.json['first_name']

    if not table_users.exists(first_name=first_name):
        user = table_users.insert(first_name=first_name)
        return user, 201
    else:
        raise exceptions.HTTPConflictError(
            'User exists', f'User with first name "{first_name}" already exists.')


@app.route('/user/<first_name>', methods=['GET'])
@process_request_response_data()
def get_user_by_name(first_name):
    user = get_or_http_404(table_users, first_name=first_name,
                           exc_name='User not found',
                           exc_msg=f'User with first name "{first_name}" not found')
    stub_host = os.environ.get('STUB_HOST')
    stub_port = os.environ.get('STUB_PORT')

    age = None
    if stub_host and stub_port:
        try:
            resp = requests.get(f'http://{stub_host}:{stub_port}/age/{first_name}')
            if resp.status_code == 200:
                age = resp.json()["data"]
        except requests.exceptions.ConnectionError as e:
            app.logger.warning(f'Unable to get age from external system:\n{e}')
    else:
        app.logger.warning(f'Unable to get age from external system: URL not specified')

    user['age'] = age

    mock_host = os.environ.get('MOCK_HOST')
    mock_port = os.environ.get('MOCK_PORT')

    last_name = None
    if mock_host and mock_port:
        try:
            resp = requests.get(f'http://{mock_host}:{mock_port}/last_name/{first_name}')
            if resp.status_code == 200:
                last_name = resp.json()["data"]['last_name']

        except requests.exceptions.ConnectionError as e:
            app.logger.warning(f'Unable to get last name from external system:\n{e}')
    else:
        app.logger.warning(f'Unable to last name age from external system: URL not specified')

    user['last_name'] = last_name

    return user, 200


if __name__ == '__main__':
    host = os.environ.get('APP_HOST', settings.APP_SETTINGS.HOST)
    port = os.environ.get('APP_PORT', settings.APP_SETTINGS.PORT)

    app.run(host, port)
