from json import JSONDecodeError
from urllib.parse import urljoin
import logging
import allure

import settings


class ApiClient:
    class Methods:
        GET = "GET"
        POST = "POST"

    class Exceptions:
        class InvalidResponse(Exception):
            pass

        class JsonUnserializable(Exception):
            pass

    def __init__(self, session):
        self.session = session
        self.logger = logging.getLogger(settings.Logging.LOGGER_NAME)
        self.base_url = settings.Url.BASE

    @allure.step("{method} request on {url}")
    def _request(self, method: str, url: str, headers=None, data=None, expected_status=200, jsonify=True,
                 allow_redirects=True):

        def log_pre(logger, method, url, headers, data, expected_status):
            logger.info(f'Performing {method} request:\n'
                        f'URL: {url}\n'
                        f'HEADERS: {headers}\n'
                        f'DATA: {data}\n\n'
                        f'expected status: {expected_status}\n\n')

        def log_post(logger, response):
            log_str = 'Got response:\n' \
                      'RESPONSE STATUS: {response.status_code}'

            if len(response.text) > settings.Logging.MAX_RESPONSE_LENGTH:
                if logger.level == logging.INFO:
                    logger.info(f'{log_str}\n'
                                f'RESPONSE CONTENT: COLLAPSED due to response size > {settings.Logging.MAX_RESPONSE_LENGTH}. '
                                f'Use DEBUG logging.\n\n')
                elif logger.level == logging.DEBUG:
                    logger.debug(f'{log_str}\n'
                                 f'RESPONSE CONTENT: {response.text}\n\n')
            else:
                logger.info(f'{log_str}\n'
                            f'RESPONSE CONTENT: {response.text}\n\n')
        
        log_pre(self.logger, method, url, headers, data, expected_status)
        response = self.session.request(method, url, headers=headers, data=data, allow_redirects=allow_redirects)
        log_post(self.logger, response)

        if int(response.status_code) != int(expected_status):
            raise self.Exceptions.InvalidResponse(f'Got {response.status_code} {response.reason} for URL "{url}"! '
                                                  f'Expected status_code: {expected_status}.')

        if jsonify:
            try:
                json_response = response.json()
                return json_response
            except JSONDecodeError:
                raise self.Exceptions.JsonUnserializable("Unable to decode response in json")
        return response

    def get(self, location, jsonify=True, allow_redirects=True):
        """GET request"""
        return self._request(self.Methods.GET, urljoin(self.base_url, location), jsonify=jsonify,
                             allow_redirects=allow_redirects)

    def post(self, location, data, jsonify=True, allow_redirects=True):
        """POST request"""
        return self._request(self.Methods.POST, urljoin(self.base_url, location), jsonify=jsonify,
                             allow_redirects=allow_redirects, data=data)

    @property
    def cookies_list(self):
        """Returns list of dicts with cookie information.
        Dict keys: name, value, domain, path, secure"""
        return [{'name': c.name, 'value': c.value, 'domain': c.domain, 'path': c.path, 'secure': c.secure}
                for c in self.session.cookies]

    def get_cookie(self, name):
        """Get cookie by name"""
        for cookie in self.cookies_list:
            if cookie["name"] == name:
                return cookie
        return None
