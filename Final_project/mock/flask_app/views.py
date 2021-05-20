import logging
from flask import Flask, jsonify
import sys

sys.path.insert(0, '/settings')

from db_client import MysqlClient
import settings


def configure_logger(logger):
    logger.setLevel(settings.GLOBAL_LOGGING.LEVEL)

    file_handler = logging.FileHandler(settings.MOCK_SETTINGS.LOGGING.LOG_FILE_PATH, 'w')
    file_handler.setLevel(settings.GLOBAL_LOGGING.LEVEL)
    logger.addHandler(file_handler)


app = Flask(__name__)
db_client = MysqlClient()

app_logger = logging.getLogger('werkzeug')
configure_logger(app_logger)


@app.route('/vk_id/<username>', methods=['GET'])
def get_vk_id(username):
    resp = db_client.get_vk_id(username=username)
    if resp:
        return jsonify({'vk_id': resp.vk_id}), 200
    else:
        return "{}", 404


@app.errorhandler(404)
def not_found_rest_api(e):
    return '{}', 404


if __name__ == '__main__':
    db_client.recreate_db()
    app.run(host=settings.MOCK_SETTINGS.HOST, port=settings.MOCK_SETTINGS.PORT)
