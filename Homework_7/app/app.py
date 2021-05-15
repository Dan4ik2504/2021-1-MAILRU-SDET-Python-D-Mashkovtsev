import json
import logging
import os
import requests
from flask import Flask, request, jsonify
from flask.logging import default_handler

import exceptions
import settings
from database.db_client import DBTable
from utils.json_utils import json_response_data, json_response_error
from utils.logging_utils import set_up_logger


app = Flask(__name__)

table_users = DBTable('first_name')

app_logger = logging.getLogger('werkzeug')
set_up_logger(app_logger, settings.APP_SETTINGS.FLASK_LOG_FILE_PATH, log_format=settings.FLASK_SETTINGS.LOG_FORMAT)
set_up_logger(app.logger, settings.APP_SETTINGS.LOG_FILE_PATH)


@app.route('/user', methods=['POST'])
def create_user():
    try:
        first_name = json.loads(request.data).get('first_name')
    except json.JSONDecodeError:
        return json_response_error('Invalid request',
                                   'Client sent a request that this server could not understand'), 400

    if first_name is None:
        return json_response_error('Invalid request', 'Request data is missing. Expected "first_name"'), 400

    if len(table_users.select(first_name=first_name)) == 0:
        user = table_users.insert(first_name=first_name)
        return json_response_data(user), 201
    else:
        return json_response_error('User exists', f'User with first name "{first_name}" already exists.'), 409


@app.route('/user/<first_name>', methods=['GET'])
def get_user_by_name(first_name):
    if user := table_users.select(first_name=first_name):
        user = user[0]
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
            app.logger.warning(f'Unable to get age from external system. STUB_HOST: {stub_host}. STUB_PORT: {stub_port}')

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
                app.logger.warning(f'Unable to get surname from external system:\n{e}')
        else:
            app.logger.warning(
                f'Unable to get surname from external system. MOCK_HOST: {mock_host}. MOCK_PORT: {mock_port}')

        user['last_name'] = last_name

        return json_response_data(user), 200
    else:
        return json_response_error('User not found', f'User with first name "{first_name}" not found'), 404


if __name__ == '__main__':
    host = os.environ.get('APP_HOST', settings.APP_SETTINGS.HOST)
    port = os.environ.get('APP_PORT', settings.APP_SETTINGS.PORT)

    app.run(host, port)
