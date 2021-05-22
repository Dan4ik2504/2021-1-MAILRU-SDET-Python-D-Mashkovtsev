from flask import Flask, jsonify
from db_client import MysqlClient
import settings


app = Flask(__name__)
db_client = MysqlClient(db_name=settings.MOCK_SETTINGS.DB_NAME)


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
