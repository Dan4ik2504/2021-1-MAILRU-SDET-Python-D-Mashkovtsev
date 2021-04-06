import time
from contextlib import contextmanager
import logging
import allure

from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

from utils.javascript_code import JsCode
import settings


class BasePage:
    """Базовый объект страницы"""
    URL = settings.Url.BASE
    logger = logging.getLogger(settings.Logging.LOGGER_NAME)

    def __init__(self, driver):
        self.driver = driver
        self.check = self._Check(self)

    class CustomWaitTimeoutException(Exception):
        pass

    def is_opened(self):
        """Additional check to see that page has been opened"""
        return True

    @property
    def action_chains(self):
        return ActionChains(self.driver)

    def open_page(self, url=None):
        """Открыть страницу в браузере"""
        url = url if url else self.URL
        allure.step(f"Page opening: {url}")
        if self.driver.current_url.split('?')[0].rstrip("/") != url:
            self.driver.get(url)
        self.custom_wait(self.check.is_page_opened)
        self.logger.info(f'Page opened: {url}')

    def wait(self, timeout=settings.Basic.DEFAULT_TIMEOUT):
        """Ожидание"""
        self.logger.info(f'Waiting')
        return WebDriverWait(self.driver, timeout)

    def scroll_to_element(self, element):
        """Скроллинг к элементу"""
        self.logger.info(f'Scrolling to {element.tag_name}')
        self.driver.execute_script(JsCode.scroll_into_view, element)

    def find(self, locator, timeout=settings.Basic.DEFAULT_TIMEOUT):
        """Поиск элемента"""
        self.logger.info(f'Searching {locator[1]} (type: {locator[0]})')
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def find_elements(self, locator, timeout=settings.Basic.DEFAULT_TIMEOUT):
        self.logger.info(f'Searching {locator[1]} (type: {locator[0]})')
        self.wait(timeout).until(EC.presence_of_element_located(locator))
        elements = self.driver.find_elements(*locator)
        return elements

    def click(self, locator, timeout=settings.Basic.DEFAULT_TIMEOUT):
        """Клик по элементу"""
        allure.step(f'Clicking on {locator[1]} (type: {locator[0]})')
        for i in range(settings.Basic.CLICK_RETRY):
            self.logger.info(
                f'Clicking on {locator[1]} (type: {locator[0]}). Try {i + 1} of {settings.Basic.CLICK_RETRY}...')
            try:
                self.custom_wait(self.check.is_page_opened, check_url=False)
                elem = self.find(locator, timeout=timeout)
                self.scroll_to_element(elem)
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

        element = self.wait().until(EC.visibility_of_element_located(locator))
        self.scroll_to_element(element)
        element.clear()
        element.send_keys(text)
        return element

    def fill_field_and_return_previous_text(self, locator, text: str):
        """Заполняет поле текстом и возвращает старый текст"""
        allure.step(f"Filling field {locator[1]} (type: {locator[0]}) with {text}")
        self.logger.info(f"Filling field {locator[1]} (type: {locator[0]}) with {text}")

        self.custom_wait(self.check.is_visible, locator)
        element = self.find(locator)
        self.scroll_to_element(element)
        prev_text = element.text
        element.clear()
        element.send_keys(text)
        return prev_text

    def get_input_value(self, locator):
        """Возвращает текст, записанный в поле input"""
        return self.find(locator).get_attribute("value")

    def custom_wait(self, method, *args, error=None, timeout=settings.Basic.DEFAULT_TIMEOUT,
                    interval=settings.Basic.DEFAULT_CHECKING_INTERVAL, check=True, **kwargs):
        log_msg = f"Waiting for {method.__name__}"
        allure.step(log_msg)
        self.logger.info(log_msg)

        if not error:
            error = self.check.exceptions.get(method.__name__, Exception)

        st = time.perf_counter()
        last_exception = None
        while time.perf_counter() - st < timeout:
            try:
                result = method(*args, **kwargs)
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

    class _Check:
        page = None
        exceptions: dict = None

        def __init__(self, page):
            self.page = page
            self.exceptions = {
                "is_visible": self.ElementNotVisibleException,
                "is_element_visible": self.ElementNotVisibleException,
                "is_element_not_visible": self.ElementVisibleException,
                "is_exists": self.ElementNotExistsException,
                "is_element_exists": self.ElementNotExistsException,
                "is_element_not_exists": self.ElementExistsException,
                "is_element_text_equal": self.ComparisonException,
                "is_element_text_not_equal": self.ComparisonException,
                "is_page_opened": self.PageNotOpenedException,

            }

        class ComparisonException(Exception):
            pass

        class ElementNotVisibleException(Exception):
            pass

        class ElementVisibleException(Exception):
            pass

        class ElementNotExistsException(Exception):
            pass

        class ElementExistsException(Exception):
            pass

        class PageNotOpenedException(Exception):
            pass

        def _is_element_visible(self, element):
            return self.page.driver.execute_script(JsCode.is_visible, element)

        def is_element_visible(self, element, raise_exception=True):
            if self._is_element_visible(element):
                return True

            if raise_exception:
                raise self.ElementNotVisibleException(
                    f'Element "{element.tag_name}" is not visible')
            else:
                return False

        def is_visible(self, locator, raise_exception=True):
            elem = self.page.find(locator)
            if self.is_element_visible(elem, raise_exception=False):
                return True

            if raise_exception:
                raise self.ElementNotVisibleException(
                    f'Element "{elem.tag_name}" found by "{locator[1]}" (type: {locator[0]}) is not visible')
            else:
                return False

        def is_element_not_visible(self, element, raise_exception=True):
            if not self._is_element_visible(element):
                return True

            if raise_exception:
                raise self.ElementVisibleException(
                    f'Element "{element.tag_name}" is visible')
            else:
                return False

        def is_not_visible(self, locator, raise_exception=True):
            try:
                elem = self.page.driver.find_element(*locator)
                if self.is_element_not_visible(elem, raise_exception=False):
                    return True
            except NoSuchElementException:
                return True

            if raise_exception:
                raise self.ElementVisibleException(
                    f"Element {elem.tag_name} found by {locator[1]} (type: {locator[0]}) is visible")
            else:
                return False

        def is_exists(self, locator, raise_exception=True):
            try:
                elem = self.page.driver.find_element(*locator)
                if elem:
                    return True
            except NoSuchElementException:
                pass

            if raise_exception:
                raise self.ElementNotExistsException(
                    f"Element {locator[1]} (type: {locator[0]}) is not found")
            else:
                return False

        def is_not_exists(self, locator, raise_exception=True):
            try:
                elem = self.page.driver.find_element(*locator)
                if elem:
                    if raise_exception:
                        raise self.ElementExistsException(
                            f"Element {elem.tag_name} found by {locator[1]} (type: {locator[0]}) is exists")
                    else:
                        return False
            except NoSuchElementException:
                pass
            return True

        def is_element_text_equal(self, elem, text, raise_exception=True):
            if elem.text == text:
                return True
            else:
                if raise_exception:
                    raise self.ComparisonException(f"{elem.text} != {text}")
                else:
                    return False

        def is_element_text_not_equal(self, elem, text, raise_exception=True):
            if elem.text != text:
                return True
            else:
                if raise_exception:
                    raise self.ComparisonException(f"elem.text is {text}")
                else:
                    return False

        def is_links_equal(self, url_1, url_2, raise_exception=True):
            urls = (url_1, url_2)
            new_urls = []
            for url in urls:
                url = url.split("?")[0]
                url = url.split("#")[0]
                url = url.rstrip("/")
                new_urls.append(url)
            url_1, url_2 = new_urls
            result = url_1 == url_2
            if result:
                return True
            else:
                if raise_exception:
                    raise self.ComparisonException(f"{url_1} != {url_2}")
                else:
                    return False

        def is_page_opened(self, url=None, check_url=True, raise_exception=True):
            if check_url:
                url = url if url else self.page.URL
                current_url = self.page.driver.current_url
                if not self.is_links_equal(current_url, url, raise_exception=False):
                    raise self.PageNotOpenedException(f"{current_url} != {url}")

            status = self.page.driver.execute_script(JsCode.document_ready_state)
            expected = "complete"
            if not status == expected:
                if raise_exception:
                    raise self.PageNotOpenedException(f"{status} != {expected}")
                else:
                    return False

            result = self.page.is_opened()
            if not result:
                raise self.PageNotOpenedException("Page is not opened")

            return True
