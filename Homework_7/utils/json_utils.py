import json

from flask import jsonify


def json_response_data(data):
    return jsonify({
        'data': data
    })


def json_response_error(error_name, error_msg):
    return jsonify({
            "error": error_name,
            "message": error_msg
        })
