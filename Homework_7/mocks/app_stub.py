import logging
import os
import random

from flask import Flask, jsonify

import settings
from utils.logging_utils import set_up_logger
from utils.flask_utils import json_response_error, json_response_data

app = Flask(__name__)

app_logger = logging.getLogger('werkzeug')
set_up_logger(app_logger, settings.STUB_SETTINGS.FLASK_LOG_FILE_PATH, log_format=settings.FLASK_SETTINGS.LOG_FORMAT)
set_up_logger(app.logger, settings.STUB_SETTINGS.LOG_FILE_PATH)


@app.route('/age/<name>', methods=['GET'])
def get_user_age_by_name(name):
    return json_response_data(random.randint(0, 100)), 200


if __name__ == '__main__':
    host = os.environ.get('STUB_HOST', settings.STUB_SETTINGS.HOST)
    port = os.environ.get('STUB_PORT', settings.STUB_SETTINGS.PORT)

    app.run(host, port)
