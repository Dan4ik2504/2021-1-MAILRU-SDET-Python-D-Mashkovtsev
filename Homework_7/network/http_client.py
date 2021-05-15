import json as jsn

from network.socket_client import SocketClient
from network.request_builder import RequestBuilder
from network.response_parser import response_parser
from furl import furl


class HttpClient:
    def __init__(self):
        self.sock = SocketClient()

    def get(self, url):
        response = self.request(RequestBuilder.METHODS.GET, url)
        return response

    def post(self, url, json=None):
        response = self.request(RequestBuilder.METHODS.POST, url, json)
        return response

    def request(self, method, url, json=None):
        url_obj = furl(url)
        self.sock.connect(url_obj.host, url_obj.port)
        request = RequestBuilder(method=method, url=url, json=json)
        self.sock.send_data(request.get_string())
        response = self.sock.receive_data()
        self.sock.disconnect()
        response_obj = response_parser(response)
        return response_obj
