import json as jsn
import re

import exceptions

first_line_regexp = r'^(?P<protocol>HTTP\/\d.\d) (?P<status_code>\d{3}) (?P<reason_phrase>.*?)$'
headers_regexp = r'^(?P<header_name>.*?): ?(?P<header_text>.*?)$'


class Response:
    def __init__(self, protocol, status_code, reason_phrase, headers, data=None, json=None):
        self.protocol = protocol
        self.status_code = status_code
        self.reason_phrase = reason_phrase
        self.headers = headers
        self.data = data
        self.json = json


def response_status_line_parser(status_line):
    result = re.search(first_line_regexp, status_line)
    if result:
        data = {
            'protocol': result['protocol'],
            'status_code': int(result['status_code']),
            'reason_phrase': result['reason_phrase']
        }
        return data
    else:
        raise exceptions.InvalidResponseError(f"Invalid response status line:\n{status_line}")


def response_headers_parser(headers_list):
    headers_list = [s.strip() for s in headers_list]

    headers = {}
    for header_str in headers_list:
        result = re.search(headers_regexp, header_str)
        if result:
            headers[result['header_name']] = result['header_text']
        else:
            raise exceptions.InvalidResponseError(f"Invalid response header:\n{header_str}")

    return headers


def response_body_parser(body_str, content_type):
    body_str = body_str.strip()
    if content_type == "application/json":
        try:
            body_json = jsn.loads(body_str)
        except jsn.JSONDecodeError:
            raise exceptions.InvalidResponseError(f"Invalid response body. Expected JSON. Received:\n{body_str}")
        return body_json
    else:
        return body_str


def response_parser(response_str):
    if len(response_str) == 0:
        raise exceptions.InvalidResponseError(f"Invalid response:\n{response_str}")

    delimiter = '\r\n\r\n'
    head, *body = response_str.split(delimiter)
    if len(body) > 1:
        raise exceptions.InvalidResponseError(f"Invalid response body:\n{delimiter.join(body)}")

    if len(head) == 0:
        raise exceptions.InvalidResponseError(f"Invalid response head:\n{head}")

    status_line, *headers = head.split('\r\n')

    data = response_status_line_parser(status_line)

    data['headers'] = response_headers_parser(headers)

    if len(body) > 0 and 'Content-Type' in data['headers']:
        response_data = response_body_parser(body[0], data['headers']['Content-Type'])
        if data['headers']['Content-Type'] == "application/json":
            data['json'] = response_data
        else:
            data['data'] = response_data

    response = Response(**data)
    return response
