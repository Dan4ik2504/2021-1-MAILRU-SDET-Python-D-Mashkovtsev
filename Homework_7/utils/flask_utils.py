import json
from functools import wraps

from flask import jsonify, request
from database.db_client import DBTable
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


def json_validator(json_data, required_fields: list = None, allowed_fields: list = None,
                   json_required_fields_can_be_empty: bool = False):
    if not isinstance(json_data, dict):
        raise exceptions.InvalidJSONException('JSON must be dict')

    json_fields = list(json_data.keys())
    if required_fields:
        required_fields_errors = []
        for req_field in required_fields:
            if req_field not in json_fields:
                required_fields_errors.append(req_field)
            else:
                if not json_required_fields_can_be_empty:
                    req_data = json_data[req_field]
                    if req_data is None or hasattr(req_data, '__len__') and len(req_data) == 0:
                        required_fields_errors.append(req_field)
                    else:
                        json_fields.remove(req_field)
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


def process_request_response_data(validate_json=False, json_required_fields_can_be_empty=False,
                                  **validate_json_kwargs):

    def inner_func(func):

        @wraps(func)
        def wrapper(**func_kwargs):
            for k, v in func_kwargs.items():
                if not validators.slug(v):
                    return json_response_error('Incorrect URL', f'"{k}" required'), 400

            if validate_json:
                try:
                    json_validator(request.json, json_required_fields_can_be_empty=json_required_fields_can_be_empty,
                                   **validate_json_kwargs)
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


def get_or_http_404(db_table: DBTable, exc_name='Not found', exc_msg='Entry not found', **kwargs):
    resp = db_table.select(**kwargs)
    if len(resp) > 0:
        return resp[0]
    else:
        raise exceptions.HTTPNotFoundError(exc_name, exc_msg)
