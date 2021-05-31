from datetime import datetime
from urllib.parse import urljoin

import pytest
import string

import settings
from test_ui.base import BaseUICase
import tests_data
from ui.locators import main_page_locators as mp_locators


class BaseMainPageTestCase(BaseUICase):
    authorize = True
    test_data = tests_data.MainPage


class TestMainPageHeaderUserInfo(BaseMainPageTestCase):

    # Methods

    def create_and_check_vk_id(self):
        vk_id = self.vkapi_builder.generate_vk_id(self.current_user.username)
        self.check_vk_id(vk_id)

    def set_and_check_vk_id(self, vk_id):
        self.vkapi_db.set_vk_id(self.current_user.username, vk_id)
        self.check_vk_id(vk_id)

    def check_vk_id(self, vk_id):
        self.main_page.refresh()
        assert self.main_page.get_vk_id() == self.test_data.VK_ID_TEMPLATE.format(vk_id)

    def check_vk_id_nonexistence(self):
        self.main_page.refresh()
        assert self.main_page.get_vk_id() == ''

    # Tests

    def test_main_page__header__username(self):
        """
        Проверка отображения корректного имени пользователя

        Шаги:
        1. Открыть страницу

        ОР: Отображается имя текущего пользователя
        """
        assert self.main_page.get_username() == self.test_data.USERNAME_TEMPLATE.format(self.current_user.username)

    def test_main_page__header__vk_id__positive(self):
        """
        Позитивный тест работы с VK API

        Шаги:
        1. Создание VK ID
        2. Перезагрузка страницы

        ОР: Отображается правильный VK ID
        """

        self.create_and_check_vk_id()

    def test_main_page__header__vk_id__check_nonexistence(self):
        """
        Тест на отсутствие VK ID, если не внесен в БД

        Шаги:
        1. Открыть главную страницу

        ОР: VK ID не отображается
        """

        assert self.main_page.get_vk_id() == ''

    def test_main_page__header__vk_id__rewrite(self):
        """
        Тест на отображение правильного VK ШD при его перезаписи в БД

        Шаги:
        1. Создание VK ID
        2. Перезагрузка страницы
        3. Перезапись VK ID
        4. Перезагрузка страницы

        ОР: После перезаписи отображается новый VK ID
        """

        self.create_and_check_vk_id()
        vk_id = self.fake.id
        self.set_and_check_vk_id(vk_id)

    def test_main_page__header__vk_id__delete(self):
        """
        Тест отображение VK ID при его удалении из БД

        Шаги:
        1. Создание VK ID
        2. Перезагрузка страницы
        3. Удаление VK ID из БД
        4. Перезагрузка страницы

        ОР: VK ID не отображается после его удаления из БД
        """

        self.create_and_check_vk_id()
        self.vkapi_db.delete_vk_id(self.current_user.username)
        self.check_vk_id_nonexistence()

    def test_main_page__header__vk_id__letters_and_punctuation(self):
        """
        Тест отображения VK ID, состоящего из букв и знаков

        Шаги:
        1. Создание VK ID
        2. Перезагрузка страницы

        ОР: В поле VK ID отображается строка, записанная в БД
        """

        vk_id = string.digits + string.ascii_letters + string.punctuation
        self.set_and_check_vk_id(vk_id)

    @pytest.mark.xfail
    def test_main_page__header__vk_id__empty(self):
        """
        Тест отображения VK ID, состоящего из пробела

        Шаги:
        1. Создание VK ID
        2. Перезагрузка страницы

        ОР: VK ID не отображается, так как VK API передал пустую строку
        """

        self.vkapi_db.set_vk_id(self.current_user.username, ' ')
        self.check_vk_id_nonexistence()

    def test_main_page__header__vk_id__null(self):
        """
        Тест отображения VK ID, состоящего из None

        Шаги:
        1. Создание VK ID
        2. Перезагрузка страницы

        ОР: VK ID не отображается, так как VK API передал None
        """

        self.vkapi_db.set_vk_id(self.current_user.username, None)
        self.check_vk_id_nonexistence()

    def test_main_page__header__logout(self):
        """
        Тест логаута

        Шаги:
        1. Залогиниться
        2. Нажать на кнопку "Logout"
        3. Подождать открытия страницы авторизации
        4. Перейти на главную страницу

        ОР: Успешный логаут. Сессионная кука отсутствует. Главная страница недоступна без повторной авторизации.
        В БД: спущен флаг активности пользователя; время логина не изменилось после логаута
        """

        assert self.login_page.check.is_session_cookie_exists()

        logout_time = datetime.utcnow()
        login_time = self.myapp_db.get_user(username=self.current_user.username, password=self.current_user.password,
                                      email=self.current_user.email).start_active_time

        self.main_page.click(self.main_page.locators.LOGOUT_BUTTON)
        self.login_page.wait_until.is_page_opened()

        assert not self.login_page.check.is_session_cookie_exists()

        self.main_page.open_page(check_page_is_open=False)
        self.login_page.wait_until.is_page_opened()

        user = self.myapp_db.get_user(username=self.current_user.username, password=self.current_user.password,
                                      email=self.current_user.email)
        assert user.access == 1
        assert user.active == 0
        assert user.start_active_time == login_time
        assert user.start_active_time <= logout_time


class TestMainPageHeader(BaseMainPageTestCase):

    @pytest.mark.parametrize(
        ("locator", "path"),
        (
                (mp_locators.HEADER_LOGO, settings.APP_SETTINGS.URLS.MAIN),
                (mp_locators.HEADER_HOME_BTN, settings.APP_SETTINGS.URLS.MAIN),
        )
    )
    def test_main_page__header__navbar_links(self, locator, path):
        """
        Тест ссылок на навигационной панели

        Шаги:
        1. Кликнуть на ссылку

        ОР: В этой же вкладке открылась нужная страница
        """
        url = urljoin(settings.APP_SETTINGS.URL, path)
        with self.main_page.is_new_tab_open(url=url, new_tabs_count=0):
            self.main_page.click(locator)
        assert self.main_page.check.is_page_url_match_driver_url()

    @pytest.mark.parametrize(
        ("dropdown_locator", "dropdown_item_locator"),
        (
                (mp_locators.HEADER_PYTHON_BTN, mp_locators.HEADER_PYTHON_HISTORY_LINK),
                (mp_locators.HEADER_LINUX_BTN, mp_locators.HEADER_LINUX_DOWNLOAD_CENTOS_LINK),
                (mp_locators.HEADER_NETWORK_BTN, mp_locators.HEADER_NETWORK_TCPDUMP_EXAMPLES)
        )
    )
    @pytest.mark.xfail
    def test_main_page__header__dropdown_opens_on_click(self, dropdown_locator, dropdown_item_locator):
        """
        Тест открытия выпадающих списков на навигационной панели по клику

        Шаги:
        1. Кликнуть на кнопку выпадающего списка

        ОР: Открылся выпадающий список. Не было перехода на другую страницу
        """

        assert not self.main_page.check.is_visible(dropdown_item_locator)
        with self.main_page.is_page_not_reloaded__context_manager():
            self.main_page.click(dropdown_locator)
            self.main_page.wait_until.is_page_opened(check_url=False)
            assert self.main_page.check.is_page_url_match_driver_url()
        assert self.main_page.check.is_visible(dropdown_item_locator)

    @pytest.mark.parametrize(
        ("dropdown_locator", "dropdown_item_locator"),
        (
                (mp_locators.HEADER_PYTHON_BTN, mp_locators.HEADER_PYTHON_HISTORY_LINK),
                (mp_locators.HEADER_LINUX_BTN, mp_locators.HEADER_LINUX_DOWNLOAD_CENTOS_LINK),
                (mp_locators.HEADER_NETWORK_BTN, mp_locators.HEADER_NETWORK_TCPDUMP_EXAMPLES)
        )
    )
    def test_main_page__header__dropdown_opens_on_hold(self, dropdown_locator, dropdown_item_locator):
        """
        Тест открытия выпадающих списков на навигационной панели по удержанию курсора

        Шаги:
        1. Навести курсор на кнопку выпадающего списка

        ОР: Открылся выпадающий список. Не было перехода на другую страницу
        """

        assert not self.main_page.check.is_visible(dropdown_item_locator)
        with self.main_page.is_page_not_reloaded__context_manager():
            self.main_page.action_chains.move_to_element(self.main_page.find(dropdown_locator)).perform()
            self.main_page.wait_until.is_page_opened(check_url=False)
            assert self.main_page.check.is_page_url_match_driver_url()
        assert self.main_page.check.is_visible(dropdown_item_locator)

    @pytest.mark.parametrize(
        ("locator", "url"),
        (
                (mp_locators.HEADER_PYTHON_HISTORY_LINK, settings.EXTERNAL_URLS.PYTHON_HISTORY),
                (mp_locators.HEADER_PYTHON_FLASK_LINK, settings.EXTERNAL_URLS.FLASK),
                (mp_locators.HEADER_LINUX_DOWNLOAD_CENTOS_LINK, settings.EXTERNAL_URLS.CENTOS_7),
                (mp_locators.HEADER_NETWORK_WIRESHARK_NEWS_LINK, settings.EXTERNAL_URLS.WIRESHARK_NEWS),
                (mp_locators.HEADER_NETWORK_WIRESHARK_DOWNLOAD_LINK, settings.EXTERNAL_URLS.WIRESHARK_DOWNLOAD),
                (mp_locators.HEADER_NETWORK_TCPDUMP_EXAMPLES, settings.EXTERNAL_URLS.TCPDUMP_EXAMPLES)
        )
    )
    @pytest.mark.xfail
    def test_main_page__header__navbar_dropdown_links(self, locator, url):
        """
        Тест внешних ссылок в выпадающих списках на навигационной панели

        Шаги:
        1. Открыть выпадающий список
        2. Кликнуть на ссылку

        ОР: В новой вкладке открылась нужная страница
        """

        with self.main_page.is_new_tab_open(url=url):
            self.main_page.click_on_navbar_dropdown_item(locator)


class TestMainPageBody(BaseMainPageTestCase):
    def test_main_page__body__buttons_count(self):
        """
        Проверка наличия элементов на странице

        Шаги:
        1. Открыть страницу

        ОР: Все элементы присутствуют
        """

        buttons_expected = [e['title'] for e in self.test_data.BODY_BUTTONS]
        elements = self.main_page.find_elements(self.main_page.locators.BODY_BUTTONS_LIST)
        assert len(elements) == len(buttons_expected)
        elems_text = [e.text for e in elements]
        assert sorted(elems_text) == sorted(buttons_expected)

    @pytest.mark.parametrize(
        ("button_title", "button_link"),
        ((e['title'], e['link']) for e in tests_data.MainPage.BODY_BUTTONS)
    )
    def test_main_page__body__buttons_links(self, button_title, button_link):
        """
        Тест перехода по ссылке

        Шаги:
        1. Кликнуть на кнопку

        ОР: В новой вкладке открылась нужная страница
        """

        locator = self.main_page.locators.BODY_BUTTON_BASE_XPATH
        locator = (locator[0], locator[1].format(button_title))
        with self.main_page.is_new_tab_open(url=button_link):
            self.main_page.click(locator)


class TestMainPageFooter(BaseMainPageTestCase):
    def test_main_page__footer__powered_by(self):
        """
        Тест наличия надписи "powered by" в футере

        Шаги:
        1. Открыть страницу

        ОР: Надпись присутствует
        """

        text = self.main_page.get_elem_text(self.main_page.locators.POWERED_BY_TEXT)
        assert text == self.test_data.POWERED_BY

    def test_main_page__footer__random_fact_about_python(self):
        """
        Тест наличия мотивационного факта о Python в футере

        Шаги:
        1. Открыть страницу

        ОР: Случайный факт присутствует
        """

        text = self.main_page.get_elem_text(self.main_page.locators.RANDOM_FACT_TEXT)
        assert text
