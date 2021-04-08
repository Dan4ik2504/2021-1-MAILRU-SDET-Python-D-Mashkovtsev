import requests
import logging
import allure

import settings


class ApiClient:

    def __init__(self):
        self.session = requests.Session()
        self.logger = logging.getLogger(settings.Logging.LOGGER_NAME)

    @allure.step('Login via API: "{user}"')
    def post_login(self, user=settings.User.LOGIN, password=settings.User.PASSWORD):
        self.logger.info(f'Login via API: "{user}"')

        location = 'https://auth-ac.my.com/auth'
        self.logger.debug(f'Login URL: "{location}"')

        headers = {
            'Referer': 'https://target.my.com/',
        }
        self.logger.debug(f'Login POST request headers: "{"; ".join([f"{k}: {v}" for k, v in headers.items()])}"')

        data = {
            'email': user,
            'password': password,
            'continue': 'https://target.my.com/auth/mycom?state=target_login%3D1%26ignore_opener%3D1#email',
            'failure': 'https://account.my.com/login/'
        }
        self.logger.debug(f'Login POST request data: "{"; ".join([f"{k}: {v}" for k, v in data.items()])}"')

        log_msg = "POST request"
        self.logger.info(log_msg)
        with allure.step(log_msg):
            self.session.post(location, headers=headers, data=data)

    @property
    def cookies_list(self):
        return [{'name': c.name, 'value': c.value, 'domain': c.domain, 'path': c.path, 'secure': c.secure}
                for c in self.session.cookies]
