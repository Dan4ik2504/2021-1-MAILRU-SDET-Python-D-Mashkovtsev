import logging

from network.socket_client import SocketClient
from network.request_builder import RequestBuilder
from network.response_parser import response_parser
from furl import furl

import settings

logger = logging.getLogger(settings.HTTP_CLIENT_SETTINGS.LOGGER_NAME)


class HttpClient:
    def __init__(self, url=None):
        self.sock = SocketClient()
        self.url = url

    def get(self, url):
        response = self.request(RequestBuilder.METHODS.GET, url)
        return response

    def post(self, url, json=None):
        response = self.request(RequestBuilder.METHODS.POST, url, json)
        return response

    def put(self, url, json=None):
        response = self.request(RequestBuilder.METHODS.PUT, url, json)
        return response

    def delete(self, url):
        response = self.request(RequestBuilder.METHODS.DELETE, url)
        return response

    def request(self, method, url, json=None):
        logger.info(f'Request. Method: "{method}". URL: "{url}"')
        if logger.level == logging.DEBUG:
            logger.debug(f'Request JSON data: "{json}"')

        url_obj = furl(url)
        self.sock.connect(url_obj.host, url_obj.port)
        request = RequestBuilder(method=method, url=url, json=json)
        self.sock.send_data(request.get_string())
        
        response = self.sock.receive_data()
        self.sock.disconnect()
        response_obj = response_parser(response)

        logger.info(f'Response. URL: {url}. Status code: "{response_obj.status_code}"')
        if logger.level == logging.DEBUG:
            if response_obj.json:
                data_log_str = f'Response JSON data: "{response_obj.json}"'
            else:
                data_log_str = f'Data: "{response_obj.data}"'
            logger.debug(f'Headers: "{response_obj.headers}"\n{data_log_str}')
        return response_obj
