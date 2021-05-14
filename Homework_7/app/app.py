import json
import logging
import os
import requests
from flask import Flask, request, jsonify

import exceptions
import settings
from database.db_client import DBTable

app = Flask(__name__)
table_users = DBTable('first_name')

logger = logging.getLogger(settings.LOGGING.LOGGER_NAME)


@app.route('/add_user', methods=['POST'])
def create_user():
    first_name = json.loads(request.data).get('first_name')
    if first_name is None:
        return jsonify({
            "error": 'first name is missing',
            "message": f'User first name is missing'
        }), 400
    if len(table_users.select(first_name=first_name)) == 0:
        user = table_users.insert(first_name=first_name)
        return jsonify({"data": user}), 201
    else:
        return jsonify({
            "error": 'user exists',
            "message": f'User with first name "{first_name}" already exists.'
        }), 400


@app.route('/get_user/<first_name>', methods=['GET'])
def get_user_by_name(first_name):
    if user := table_users.select(first_name=first_name):
        user = user[0]
        stub_host = os.environ.get('STUB_HOST')
        stub_port = os.environ.get('STUB_PORT')

        age = None
        if stub_host and stub_port:
            try:
                resp = requests.get(f'http://{stub_host}:{stub_port}/get_age/{first_name}')
                if resp.status_code == 200:
                    age = resp.json()["data"]
            except requests.exceptions.ConnectionError as e:
                logger.warning(f'Unable to get age from external system:\n{e}')
        else:
            logger.warning(f'Unable to get age from external system. STUB_HOST: {stub_host}. STUB_PORT: {stub_port}')

        user['age'] = age

        mock_host = os.environ.get('MOCK_HOST')
        mock_port = os.environ.get('MOCK_PORT')

        last_name = None
        if mock_host and mock_port:
            try:
                resp = requests.get(f'http://{mock_host}:{mock_port}/get_last_name/{first_name}')
                if resp.status_code == 200:
                    last_name = resp.json()["data"]['last_name']

            except requests.exceptions.ConnectionError as e:
                logger.warning(f'Unable to get surname from external system:\n{e}')
        else:
            logger.warning(f'Unable to get surname from external system. MOCK_HOST: {mock_host}. MOCK_PORT: {mock_port}')

        user['last_name'] = last_name

        return jsonify({"data": user}), 200
    else:
        return jsonify({
                    "error": 'user not found',
                    "message": f'User with first name "{first_name}" not found'
                }), 404


if __name__ == '__main__':
    host = os.environ.get('APP_HOST', settings.APP_SETTINGS.HOST)
    port = os.environ.get('APP_PORT', settings.APP_SETTINGS.PORT)

    app.run(host, port)
