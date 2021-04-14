from json import JSONDecodeError
import logging
import allure
import requests

import settings
from api import settings_api


class ApiClient:
    class Methods:
        GET = "GET"
        POST = "POST"
        DELETE = "DELETE"

    class Exceptions:
        class InvalidResponse(Exception):
            pass

        class JsonUnserializable(Exception):
            pass

        class CsrfCookie(Exception):
            pass

    def __init__(self, session):
        self.session: requests.Session = session
        self.logger = logging.getLogger(settings.Logging.LOGGER_NAME)
        self.base_url = settings.Url.BASE

    def _set_headers(self, headers):
        """Adds the required headers"""
        if not isinstance(headers, dict):
            headers = {}
        if headers.get("Referer", None) is None:
            headers["Referer"] = settings.Url.BASE

        csrftoken = self.get_csrf_token(check=False)
        if csrftoken is not None:
            headers["X-CSRFToken"] = csrftoken["value"]

        return headers

    @allure.step("{method} request on {url}")
    def _request(self, method: str, url: str, params=None, data=None, headers=None, cookies=None, files=None,
                 allow_redirects=True, expected_status=200, jsonify=True, json=None):
        """Executes a request with a given method and prepared headers"""

        def log_pre(logger, url, params, data, headers, cookies, files, allow_redirects, json, jsonify):
            logger.info(f'Performing {method} request:\n'
                        f'URL: {url}\n'
                        f'Is redirects allowed: {allow_redirects}\n'
                        f'Is convert response to json: {jsonify}\n'
                        f'expected status: {expected_status}')

            if logger.level == logging.DEBUG:
                logger.debug(f'Performing {method} request:\n'
                             f'HEADERS: {headers}\n'
                             f'PARAMS: {params}\n'
                             f'DATA: {data}\n'
                             f'COOKIES: {cookies}\n'
                             f'FILES: {files}\n'
                             f'JSON: {json}')

        def log_post(logger, response):
            log_str = 'Got response:\n' \
                      f'RESPONSE STATUS: {response.status_code}'

            if len(response.text) > settings.Logging.MAX_RESPONSE_LENGTH:
                if logger.level == logging.INFO:
                    logger.info(f'{log_str}\n'
                                f'RESPONSE CONTENT: COLLAPSED due to response size > '
                                f'{settings.Logging.MAX_RESPONSE_LENGTH}. '
                                f'Use DEBUG logging.\n')
                elif logger.level == logging.DEBUG:
                    logger.debug(f'{log_str}\n'
                                 f'RESPONSE CONTENT: {response.text}')
            else:
                logger.info(f'{log_str}\n'
                            f'RESPONSE CONTENT: {response.text}')

        headers = self._set_headers(headers)

        log_pre(self.logger, url, params=params, data=data, headers=headers,
                cookies=cookies, files=files, allow_redirects=allow_redirects, json=json, jsonify=jsonify)
        response = self.session.request(method, url, params=params, data=data, headers=self._set_headers(headers),
                                        cookies=cookies, files=files, allow_redirects=allow_redirects, json=json)
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

    def get_request(self, url, params=None, data=None, headers=None, cookies=None, files=None,
                    allow_redirects=True, expected_status=200, jsonify=True, json=None):
        """GET request"""
        return self._request(self.Methods.GET, url, params=params, data=data, headers=headers, cookies=cookies,
                             files=files, allow_redirects=allow_redirects, expected_status=expected_status,
                             jsonify=jsonify, json=json)

    def post_request(self, url, params=None, data=None, headers=None, cookies=None, files=None,
                     allow_redirects=True, expected_status=200, jsonify=True, json=None):
        """POST request"""
        return self._request(self.Methods.POST, url, params=params, data=data, headers=headers, cookies=cookies,
                             files=files, allow_redirects=allow_redirects, expected_status=expected_status,
                             jsonify=jsonify, json=json)

    def delete_request(self, url, params=None, data=None, headers=None, cookies=None, files=None,
                       allow_redirects=True, expected_status=200, jsonify=True, json=None):
        """DELETE request"""
        return self._request(self.Methods.DELETE, url, params=params, data=data, headers=headers, cookies=cookies,
                             files=files, allow_redirects=allow_redirects, expected_status=expected_status,
                             jsonify=jsonify, json=json)

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

    def get_csrf_token(self, check=True):
        """Get csrf cookie"""
        self.session.get(settings.Url.CSRF)
        csrf = self.get_cookie(settings_api.CookieNames.CSRF)
        if check:
            if csrf is None:
                raise self.Exceptions.CsrfCookie("CSRF token not received")
        return csrf
