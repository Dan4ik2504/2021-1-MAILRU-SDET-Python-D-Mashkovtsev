import json as jsn

import exceptions


class Response:
    def __init__(self, protocol, status_code, reason_phrase, headers, data=None, json=None):
        self.protocol = protocol
        self.status_code = status_code
        self.reason_phrase = reason_phrase
        self.headers = headers
        self.data = data
        self.json = json


def response_header_parser(head_str):
    head_list = head_str.split('\r\n')
    head_list = [s.strip() for s in head_list]
    protocol, status_code, *reason_phrase = head_list.pop(0).split(' ')
    protocol = protocol.strip()
    status_code = status_code.strip()
    reason_phrase = ' '.join(reason_phrase).strip()

    if status_code.isdigit():
        status_code = int(status_code)
    else:
        raise exceptions.InvalidResponseError(f"Invalid response status_code:\n{status_code}")

    headers = {}
    for header_str in head_list:
        h_key, *h_value = header_str.split(':')
        h_key = h_key.strip()
        h_value = ':'.join(h_value).strip()
        headers[h_key] = h_value

    data = {
        'protocol': protocol,
        'status_code': status_code,
        'reason_phrase': reason_phrase,
        'headers': headers
    }
    return data


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

    head, *body = response_str.split('\r\n\r\n')
    body = '\r\n'.join(body)
    if len(head) == 0:
        raise exceptions.InvalidResponseError(f"Invalid response headers:\n{head}")

    data_dict = response_header_parser(head)
    if len(body) > 0 and 'Content-Type' in data_dict['headers']:
        response_data = response_body_parser(body, data_dict['headers']['Content-Type'])
        if data_dict['headers']['Content-Type'] == "application/json":
            data_dict['json'] = response_data
        else:
            data_dict['data'] = response_data

    response = Response(**data_dict)
    return response
