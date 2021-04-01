import time
from contextlib import contextmanager
import logging
import allure

from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

import settings


class BasePage:
    """Базовый объект страницы"""
    URL = settings.Url.BASE
    logger = logging.getLogger(settings.Logging.LOGGER_NAME)

    def __init__(self, driver):
        self.driver = driver
        self.open_page()

    class PageIsNotOpenedException(Exception):
        pass

    class PageIsNotLoadedException(Exception):
        pass

    class ComparisonException(Exception):
        pass

    class CustomWaitTimeoutException(Exception):
        pass

    @property
    def action_chains(self):
        return ActionChains(self.driver)

    def open_page(self, url=None):
        """Открыть страницу в браузере"""
        URL = url if url else self.URL
        allure.step(f"Page opening: {URL}")
        if self.driver.current_url.split('?')[0].rstrip("/") != URL:
            self.driver.get(URL)
        self.wait_until_load(url=URL)
        self.logger.info(f'Page opened: {URL}')

    def is_opened(self, url=None):
        URL = url if url else self.URL
        URL = URL.rstrip("/")
        current_url = self.driver.current_url.split('?')[0].rstrip("/")
        if current_url == URL:
            return True
        raise self.PageIsNotOpenedException(f"{current_url} != {URL}")

    def wait_until_open(self, url=None):
        """Ожидание открытия страницы"""
        result = self.custom_wait(self.is_opened, error=self.PageIsNotOpenedException, check=True, url=url)
        if result:
            self.logger.info(f'Page opened')

    def is_loaded(self):
        status = self.driver.execute_script("return document.readyState")
        expected = "complete"
        if status == expected:
            return True
        raise self.PageIsNotLoadedException(f"{status} != {expected}")

    def wait_until_load(self, url=None):
        """Ожидание открытия (если передан URL) и загрузки страницы"""
        if url:
            self.wait_until_open(url=url)
        result = self.custom_wait(self.is_loaded, check=True, error=self.PageIsNotLoadedException)
        if result:
            self.logger.info(f'Page loaded')
        return result

    def is_elem_text_not_equal(self, elem, text):
        if elem.text != text:
            return True
        else:
            raise self.ComparisonException(f"elem.text is {text}")

    def wait_until_elem_text_changes(self, elem, text):
        """Ждать пока текст элемента изменится"""
        self.logger.info(f'Waiting until {elem.tag_name} text is changes from {text}')
        return self.custom_wait(self.is_elem_text_not_equal, check=True, timeout=2, error=self.ComparisonException,
                                elem=elem, text=text)

    def is_elem_text_equal(self, elem, text):
        if elem.text == text:
            return True
        else:
            raise self.ComparisonException(f"{elem.text} != {text}")

    def wait_until_elem_text_is_equal(self, elem, text):
        """Ждать пока текст элемента не станет равен"""
        self.logger.info(f'Waiting until {elem.tag_name} text is equal {text}')
        return self.custom_wait(self.is_elem_text_equal, check=True, timeout=2, error=self.ComparisonException,
                                text=text, elem=elem,)

    def wait(self, timeout=settings.Basic.DEFAULT_TIMEOUT):
        """Ожидание"""
        self.logger.info(f'Waiting')
        return WebDriverWait(self.driver, timeout)

    def scroll_to(self, element):
        """Скроллинг к элементу"""
        self.logger.info(f'Scrolling to {element.tag_name}')
        self.driver.execute_script('arguments[0].scrollIntoView(true);', element)

    def find(self, locator, timeout=settings.Basic.DEFAULT_TIMEOUT):
        """Поиск элемента"""
        self.logger.info(f'Finding {locator[1]} (type: {locator[0]})')
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def click(self, locator, timeout=settings.Basic.DEFAULT_TIMEOUT):
        """Клик по элементу"""
        allure.step(f'Clicking on {locator[1]} (type: {locator[0]})')
        for i in range(settings.Basic.CLICK_RETRY):
            self.logger.info(f'Clicking on {locator[1]} (type: {locator[0]}). Try {i + 1} of {settings.Basic.CLICK_RETRY}...')
            try:
                self.wait_until_load()
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
        allure.step(f"Filling field {locator[1]} (type: {locator[0]}) with {text}")
        self.logger.info(f"Filling field {locator[1]} (type: {locator[0]}) with {text}")
        element = self.find(locator)
        element.clear()
        element.send_keys(text)
        return element

    def fill_field_and_return_previous_text(self, locator, text: str):
        """Заполняет поле текстом и возвращает старый текст"""
        self.logger.info(f"Filling field {locator[1]} (type: {locator[0]}) with {text}")
        element = self.find(locator)
        prev_text = element.text
        element.clear()
        element.send_keys(text)
        return prev_text

    def get_input_value(self, locator):
        """Возвращает текст, записанный в поле input"""
        return self.find(locator).get_attribute("value")

    def custom_wait(self, method, error=Exception, timeout=settings.Basic.DEFAULT_TIMEOUT,
             interval=settings.Basic.DEFAULT_CHECKING_INTERVAL, check=False, **kwargs):
        self.logger.info(f"Waiting for {method.__name__}")
        st = time.time()
        last_exception = None
        while time.time() - st < timeout:
            try:
                result = method(**kwargs)
                if check:
                    if result:
                        return result
                    last_exception = f'Method {method.__name__} returned {result}'
                else:
                    return result
            except error as e:
                last_exception = e
            time.sleep(interval)

        raise self.CustomWaitTimeoutException(
            f'Method {method.__name__} timeout in {timeout}sec with exception: "{last_exception}"')
