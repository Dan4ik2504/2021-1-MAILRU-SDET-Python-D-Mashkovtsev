import pytest

from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

import settings


class BasePage:
    URL = settings.BASE_URL

    def __init__(self, driver):
        self.driver = driver

    def open_page(self):
        """Открыть страницу в браузере"""
        self.driver.get(self.URL)

    def wait(self, timeout=settings.DEFAULT_TIMEOUT):
        """Ожидание"""
        return WebDriverWait(self.driver, timeout)

    def find(self, locator, timeout=settings.DEFAULT_TIMEOUT):
        """Поиск элемента"""
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def click(self, locator, timeout=settings.DEFAULT_TIMEOUT):
        """Клик по элементу"""
        for i in range(settings.CLICK_RETRY):
            try:
                element = self.wait(timeout).until(EC.element_to_be_clickable(locator))
            except TimeoutException as exc:
                if i == settings.CLICK_RETRY - 1:
                    raise exc
            else:
                element.click()
                return element

    def fill_field(self, locator, text: str):
        """Заполнить поле текстом"""
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

