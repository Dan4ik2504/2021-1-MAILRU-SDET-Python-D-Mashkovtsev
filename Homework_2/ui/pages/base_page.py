from contextlib import contextmanager
import logging
import allure

from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

from utils.decorators import wait

import settings


class BasePage:
    """Базовый объект страницы"""
    URL = settings.Url.BASE

    def __init__(self, driver):
        self.driver = driver

    class PageNotLoadedException(Exception):
        pass

    @property
    def action_chains(self):
        return ActionChains(self.driver)

    def open_page(self, url=None):
        """Открыть страницу в браузере"""
        URL = url if url else self.URL
        self.driver.get(URL)
        wait(self.is_opened, url=URL)
        self.wait().until(self.is_page_loaded)

    def is_opened(self, url=None, timeout=settings.Basic.DEFAULT_TIMEOUT,
                  checking_interval=settings.Basic.DEFAULT_CHECKING_INTERVAL):
        """Проверка на то, открыта ли страница"""

        URL = url if url else self.URL

        def _check_url(url):
            if self.driver.current_url != url:
                raise self.PageNotLoadedException(
                    f'{self.URL} did not opened in {settings.Basic.DEFAULT_TIMEOUT} for {self.__class__.__name__}.\n'
                    f'Current url: {self.driver.current_url}.')
            return True

        wait(_check_url, error=self.PageNotLoadedException, check=True, timeout=timeout,
             interval=checking_interval, url=URL)


    @staticmethod
    def is_page_loaded(driver):
        """Возвращает True, если страница загружена"""
        return driver.execute_script("return document.readyState") == "complete"

    def wait(self, timeout=settings.Basic.DEFAULT_TIMEOUT):
        """Ожидание"""
        return WebDriverWait(self.driver, timeout)

    def scroll_to(self, element):
        """Скроллинг к элементу"""
        self.driver.execute_script('arguments[0].scrollIntoView(true);', element)

    def find(self, locator, timeout=settings.Basic.DEFAULT_TIMEOUT):
        """Поиск элемента"""
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    @allure.step('Clicking "{locator}"')
    def click(self, locator, timeout=settings.Basic.DEFAULT_TIMEOUT):
        """Клик по элементу"""
        for i in range(settings.Basic.CLICK_RETRY):
            try:
                self.wait(timeout).until(self.is_page_loaded)
                elem = self.find(locator, timeout=timeout)
                self.scroll_to(elem)
                elem = self.wait(timeout).until(EC.element_to_be_clickable(locator))
                elem.click()
                return
            except (TimeoutException, StaleElementReferenceException) as exc:
                if i == settings.Basic.CLICK_RETRY - 1:
                    raise exc

    def fill_field(self, locator, text: str):
        """Заполняет поле текстом"""
        element = self.find(locator)
        element.clear()
        element.send_keys(text)
        return element

    def fill_field_and_return_previous_text(self, locator, text: str):
        """Заполняет поле текстом и возвращает старый текст"""
        element = self.find(locator)
        prev_text = element.text
        element.clear()
        element.send_keys(text)
        return prev_text

    def get_input_value(self, locator):
        """Возвращает текст, записанный в поле input"""
        return self.find(locator).get_attribute("value")
