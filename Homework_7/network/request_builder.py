from furl import furl
import json as jsn


class RequestBuilder:
    class METHODS:
        GET = 'GET'
        POST = 'POST'
        PUT = 'PUT'
        DELETE = 'DELETE'

    def __init__(self, method: str, url: str, headers: dict = None, json=None, protocol='HTTP/1.1'):
        self.method = method.upper()
        self.url = furl(url)
        self.headers = headers or {}
        self.json = json
        self.data = None
        self.protocol = protocol

    def prepare(self):
        if self.method == self.METHODS.POST:
            if self.json:
                self.headers['Content-Type'] = 'application/json'
                self.data = jsn.dumps(self.json)

            self.headers['Content-Length'] = len(self.data)
            self.headers['Connection'] = 'close'

    def get_string(self):
        self.prepare()
        request_rows = [
            f'{self.method} {self.url.url} {self.protocol}',
            f'Host: {self.url.host}'
        ]

        for k, v in self.headers.items():
            request_rows.append(f'{k}: {v}')

        if self.data:
            request_rows.append("")
            request_rows.append(self.data)

        return '\r\n'.join(request_rows) + '\r\n\r\n'
