import json

from flask import jsonify
import exceptions


def json_response_data(data):
    return jsonify({
        'data': data
    })


def json_response_error(error_name, error_msg):
    return jsonify({
            "error": error_name,
            "message": error_msg
        })


def validate_json(json_str, required_fields: list = None, allowed_fields: list = None):
    try:
        json_data = json.loads(json_str)
    except json.JSONDecodeError:
        raise exceptions.InvalidJSONException('Invalid JSON data')

    if not isinstance(json_data, dict):
        raise exceptions.InvalidJSONException('JSON must be dict')

    json_fields = list(json_data.keys())
    if required_fields:
        required_fields_errors = []
        for req_field in required_fields:
            if req_field not in json_fields:
                required_fields_errors.append(req_field)
            else:
                json_fields.remove(req_field)
    else:
        required_fields_errors = None

    if not allowed_fields:
        allowed_fields = []
    allowed_fields_errors = []
    for json_field in json_fields:
        if json_field not in allowed_fields:
            allowed_fields_errors.append(json_field)

    if required_fields_errors or allowed_fields_errors:
        error_msg = ""
        if required_fields_errors:
            error_msg += f'Fields required: {", ".join(required_fields_errors)}. '
        if allowed_fields_errors:
            error_msg += f'Fields not allowed: {", ".join(allowed_fields_errors)}'
        raise exceptions.InvalidJSONException(error_msg)
    else:
        return json_data
