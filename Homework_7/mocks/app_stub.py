import os
import random

from flask import Flask, jsonify

import settings

app = Flask(__name__)


@app.route('/get_age/<name>', methods=['GET'])
def get_user_age_by_name(name):
    return jsonify({"data": random.randint(0, 100)}), 200


if __name__ == '__main__':
    host = os.environ.get('STUB_HOST', settings.STUB_SETTINGS.HOST)
    port = os.environ.get('STUB_PORT', settings.STUB_SETTINGS.HOST)

    app.run(host, port)
