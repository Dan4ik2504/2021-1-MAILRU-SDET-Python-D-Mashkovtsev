import json
from functools import wraps

from flask import jsonify, request
import exceptions
import validators


def json_response_data(data):
    return jsonify({
        'data': data
    })


def json_response_error(error_name, error_msg):
    return jsonify({
            "error": error_name,
            "message": error_msg
        })


def json_validator(json_data, required_fields: list = None, allowed_fields: list = None):
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


def process_request_response_data(validate_json=False, **validate_json_kwargs):

    def inner_func(func):

        @wraps(func)
        def wrapper(**func_kwargs):
            for k, v in func_kwargs.items():
                if not validators.slug(v):
                    return json_response_error('Incorrect URL', f'"{k}" required'), 400

            if validate_json:
                try:
                    json_validator(request.json, **validate_json_kwargs)
                except exceptions.InvalidJSONException as exc:
                    return json_response_error('Invalid JSON', str(exc)), 400

            try:
                response = list(func(**func_kwargs))
            except (exceptions.HTTPClientError, exceptions.InvalidJSONException) as exc:
                return json_response_error(exc.err_name, exc.err_msg), exc.status_code
            else:
                response[0] = json_response_data(response[0])
                return tuple(response)

        return wrapper

    return inner_func
