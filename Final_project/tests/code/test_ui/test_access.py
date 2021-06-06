from urllib.parse import urljoin
import pytest

import settings
import tests_data
from test_ui.base import BaseUICase


class TestAccessToPagesWithoutLogin(BaseUICase):
    authorize = False
    auto_open_page = False

    def test_no_login__access_login_page(self):
        """
        Тест доступа к странице авторизации по пути "/login" без авторизации

        Шаги:
        1. Запрос страницы авторизации

        ОР: Открылась страница авторизации
        """

        self.login_page.open_page()
        assert self.login_page.check.is_page_url_match_driver_url()

    def test_no_login__access_login_page_2(self):
        """
        Тест доступа к странице авторизации по пути "/" без авторизации

        Шаги:
        1. Запрос страницы авторизации

        ОР: Открылась страница авторизации
        """

        self.login_page.open_page(url=settings.APP_SETTINGS.URL)
        assert self.login_page.current_url.path == '/'

    def test_no_login__access_register_page(self):
        """
        Тест доступа к странице регистрации без авторизации

        Шаги:
        1. Запрос страницы регистрации

        ОР: Открылась страница регистрации
        """

        self.register_page.open_page()
        assert self.register_page.check.is_page_url_match_driver_url()

    def test_no_login__access_main_page(self):
        """
        Тест доступа к главной странице без авторизации

        Шаги:
        1. Запрос главной страницы

        ОР: Произошел редирект на страницу авторизации
        """

        self.main_page.open_page(check_page_is_open=False)
        self.login_page.wait_until.is_page_opened()
        assert self.login_page.current_url.args['next'] == settings.APP_SETTINGS.URLS.MAIN
        assert self.login_page.get_error_text() == tests_data.LoginPage.ErrorMsgs.NOT_AUTHORIZED


class TestAccessToPageWithLogin(BaseUICase):
    authorize = True
    auto_open_page = False

    def test_login__access_login_page(self):
        """
        Тест доступа к странице авторизации по пути "/login" без авторизации

        Шаги:
        1. Запрос страницы авторизации

        ОР: Произошел редирект на главную страницу
        """

        self.login_page.open_page(check_page_is_open=False)
        self.main_page.wait_until.is_page_opened()
        assert self.main_page.check.is_page_url_match_driver_url()

    def test_login__access_login_page_2(self):
        """
        Тест доступа к странице авторизации по пути "/" без авторизации

        Шаги:
        1. Запрос страницы авторизации

        ОР: Произошел редирект на главную страницу
        """

        self.login_page.open_page(url=settings.APP_SETTINGS.URL, check_page_is_open=False)
        self.main_page.wait_until.is_page_opened()
        assert self.main_page.check.is_page_url_match_driver_url()

    def test_login__access_register_page(self):
        """
        Тест доступа к странице регистрации без авторизации

        Шаги:
        1. Запрос страницы регистрации

        ОР: Произошел редирект на главную страницу
        """

        self.register_page.open_page(check_page_is_open=False)
        self.main_page.wait_until.is_page_opened()
        assert self.main_page.check.is_page_url_match_driver_url()

    def test_login__access_main_page(self):
        """
        Тест доступа к странице авторизации по пути "/login" без авторизации

        Шаги:
        1. Запрос главной страницы

        ОР: Открылась главная страница
        """

        self.main_page.open_page()
        assert self.main_page.check.is_page_url_match_driver_url()


class TestCheckResourcesAvailability(BaseUICase):
    auto_open_page = False
    authorize = False
    seleniumwire_pages = True

    @pytest.mark.parametrize(
        ("path", "authorize_required"),
        (
                ('', False),
                (settings.APP_SETTINGS.URLS.LOGIN, False),
                (settings.APP_SETTINGS.URLS.REGISTRATION, False),
                (settings.APP_SETTINGS.URLS.MAIN, True),
        )
    )
    def test__resources_availability(self, path, authorize_required):
        """
        Тест доступности ресурсов на странице

        Шаги:
        1. Открыть страницу

        ОР: Все внешние ресурсы загрузились
        """

        if settings.EXTERNAL_SETTINGS.WITH_SELENOID:
            pytest.skip("Can't intercept requests when using the selenoid")

        url = urljoin(settings.APP_SETTINGS.URL, path)

        if authorize_required:
            self.do_login()

        self.base_page.open_page(url, check_page_is_open=False)
        self.base_page.wait_until.is_page_opened(url=url)
        print("Requests:", self.base_page.driver.requests)
        invalid_requests = [r for r in self.base_page.driver.requests
                            if r.response
                            and (
                                    str(r.response.status_code).startswith('4')
                                    or str(r.response.status_code).startswith('5')
                            )]

        assert len(invalid_requests) == 0, \
            f"Resources unavailable:\n" + \
            '\n'.join([f"Status code: {r.response.status_code}. URL: {r.url}" for r in invalid_requests])
