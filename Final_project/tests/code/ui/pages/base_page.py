import inspect
import time
import logging
from contextlib import contextmanager
from functools import wraps

import allure

from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException, \
    JavascriptException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver

from utils.javascript_code import JsCode
import settings
import exceptions


class BasePage:
    """Base page object"""
    URL = ''
    logger = logging.getLogger(settings.TESTS.LOGGER_NAME)

    def __init__(self, driver):
        self.driver: WebDriver = driver
        self.check = self._Check(self)
        self.wait_until = self._WaitUntil(self)
        self.URL = settings.APP_SETTINGS.URL + self.URL

    def is_opened(self):
        """Additional check to see that page has been opened"""
        return True

    @property
    def action_chains(self):
        """ActionChains"""
        return ActionChains(self.driver)

    def wait(self, timeout=settings.UI.DEFAULT_TIMEOUT):
        """WebDriverWait"""
        return WebDriverWait(self.driver, timeout)

    def open_page(self, url=None):
        """Open the page"""
        url = url if url else self.URL
        log_msg = f"Page opening: {url}"
        with allure.step(log_msg):
            self.logger.info(log_msg)

            log_msg = f'URL checking'
            with allure.step(log_msg):
                self.logger.info(log_msg)
                if not self.check.is_links_equal(self.driver.current_url, url, raise_exception=False):
                    log_msg = f'Opening URL: "{url}". Previous URL: "{self.driver.current_url}"'
                    with allure.step(log_msg):
                        self.logger.info(log_msg)
                        self.driver.get(url)

            log_msg = 'Checking page load'
            with allure.step(log_msg):
                self.logger.info(log_msg)
                self.custom_wait(self.check.is_page_opened)
                self.logger.info(f'Page opened: "{url}"')

    def scroll_to_element(self, element):
        """Scrolling to the element found by locator"""
        log_msg = f'Scrolling to "{element.tag_name}"'
        with allure.step(log_msg):
            self.logger.info(log_msg)
            self.driver.execute_script(JsCode.scroll_into_view, element)

    def find(self, locator, timeout=settings.UI.DEFAULT_TIMEOUT):
        """Finding item by locator"""
        log_msg = f'Searching of the element by locator: "{locator[1]}" (type: {locator[0]})'
        with allure.step(log_msg):
            self.logger.info(log_msg)
            try:
                log_msg = f'Waiting for the presence of the element'
                with allure.step(log_msg):
                    self.logger.info(log_msg)
                    element = self.wait(timeout).until(EC.presence_of_element_located(locator))
                self.logger.info(f'Element have been found: "{element.tag_name}"')
                return element
            except TimeoutException:
                raise exceptions.FindingException(f'Element not found by locator: "{locator[1]}" (type: {locator[0]})')

    def fast_find(self, locator):
        """Finding item by locator without waiting"""
        log_msg = f'Fast searching of the element by locator: "{locator[1]}" (type: {locator[0]})'
        with allure.step(log_msg):
            self.logger.info(log_msg)
            try:
                element = self.driver.find_element(*locator)
                self.logger.info(f'Element have been found: "{element.tag_name}"')
                return element
            except (NoSuchElementException, StaleElementReferenceException):
                raise exceptions.FindingException(f'Element not found by locator: "{locator[1]}" (type: {locator[0]})')

    def find_elements(self, locator):
        """Finding an items by locator"""
        log_msg = f'Searching elements by locator: "{locator[1]}" (type: {locator[0]})'
        with allure.step(log_msg):
            self.logger.info(log_msg)
            elements = self.driver.find_elements(*locator)

            elements_names = []
            for e in elements:
                try:
                    elements_names.append(e.tag_name)
                except StaleElementReferenceException:
                    pass

            if len(elements) > 0:
                self.logger.info(f'{len(elements)} element(s) have been found')
                self.logger.debug(f'Element(s) have been found: "{", ".join(elements_names)}"')
            else:
                self.logger.info(f'No items found')
            return elements

    def click(self, locator, timeout=settings.UI.DEFAULT_TIMEOUT):
        """Click on an element found by locator"""
        log_msg = f'Clicking on "{locator[1]}" (type: {locator[0]})'
        with allure.step(log_msg):
            for i in range(settings.UI.CLICK_RETRY):
                log_msg = f'Clicking on "{locator[1]}" (type: {locator[0]}). ' \
                          f'Try {i + 1} of {settings.UI.CLICK_RETRY}...'
                with allure.step(log_msg):
                    self.logger.info(log_msg)
                    try:
                        log_msg = f'Waiting for page opening and loading'
                        with allure.step(log_msg):
                            self.logger.info(log_msg)
                            self.custom_wait(self.check.is_page_opened, check_url=False)

                        log_msg = f'Searching of the element found by locator "{locator[1]}" (type: {locator[0]})'
                        with allure.step(log_msg):
                            self.logger.info(log_msg)
                            elem = self.find(locator, timeout=timeout)

                        log_msg = f'Scrolling to the element found by locator "{locator[1]}" (type: {locator[0]})'
                        with allure.step(log_msg):
                            self.logger.info(log_msg)
                            self.scroll_to_element(elem)

                        log_msg = f'Waiting for element found by locator ' \
                                  f'"{locator[1]}" (type: {locator[0]}) to be clickable'
                        with allure.step(log_msg):
                            self.logger.info(log_msg)
                            elem = self.wait(timeout).until(EC.element_to_be_clickable(locator))

                        log_msg = f'Clicking on "{elem.tag_name}" found by "{locator[1]}" (type: {locator[0]})'
                        with allure.step(log_msg):
                            self.logger.info(log_msg)
                            elem.click()
                        return
                    except (TimeoutException, StaleElementReferenceException, exceptions.FindingException) as exc:
                        if i == settings.UI.CLICK_RETRY - 1:
                            raise exc
                        self.logger.debug(f'Error thrown: {exc}. Trying click again')

    def _fill_field(self, locator, text):
        log_msg = f'Waiting for page opening and loading'
        with allure.step(log_msg):
            self.logger.info(log_msg)
            self.custom_wait(self.check.is_page_opened, check_url=False)

        log_msg = f'Waiting for element found by locator ' \
                  f'"{locator[1]}" (type: {locator[0]}) visibility to be located'
        with allure.step(log_msg):
            self.logger.info(log_msg)
            element = self.wait().until(EC.visibility_of_element_located(locator))

        log_msg = f'Scrolling to the element found by locator "{locator[1]}" (type: {locator[0]})'
        with allure.step(log_msg):
            self.logger.info(log_msg)
            self.scroll_to_element(element)

        log_msg = f'Waiting for element found by locator "{locator[1]}" (type: {locator[0]}) to be visible'
        with allure.step(log_msg):
            self.logger.info(log_msg)
            self.custom_wait(self.check.is_visible, locator)

        log_msg = f'Filling element found by locator "{locator[1]}" (type: {locator[0]}) with "{text}"'
        with allure.step(log_msg):
            self.logger.info(log_msg)
            prev_text = element.text
            element.clear()
            element.send_keys(text)

        self.logger.info(f'Field "{element.tag_name}" filled')
        return element, prev_text

    def fill_field(self, locator, text):
        """Fills field found by locator with the given text"""
        log_msg = f'Filling field found by locator "{locator[1]}" (type: {locator[0]}) with "{text}"'
        with allure.step(log_msg):
            self.logger.info(log_msg)
            element, _ = self._fill_field(locator, text)
            return element

    def fill_field_and_return_previous_text(self, locator, text: str):
        """Fills field found by locator with the given text and returns the previously text"""
        log_msg = f'Filling field found by locator "{locator[1]}" (type: {locator[0]}) with "{text}" ' \
                  f'and returning the previous text'
        with allure.step(log_msg):
            self.logger.info(log_msg)
            _, prev_text = self._fill_field(locator, text)
            return prev_text

    def get_input_value(self, locator):
        """Returns the text of the input field found by locator"""
        log_msg = f'Getting the value of the input field: "{locator[1]}" (type: {locator[0]})'
        with allure.step(log_msg):
            self.logger.info(log_msg)

            log_msg = f'Searching of the input field by locator "{locator[1]}" (type: {locator[0]})'
            with allure.step(log_msg):
                self.logger.info(log_msg)
                element = self.find(locator)

            log_msg = f'Getting value from input field found by locator "{locator[1]}" (type: {locator[0]})'
            with allure.step(log_msg):
                self.logger.info(log_msg)
                result = element.get_attribute("value")

            self.logger.info(f'Received the value of the input field: "{locator[1]}" (type: {locator[0]})')
            self.logger.debug(f'Value of the input field: {result}')
            return result

    def custom_wait(self, method, *args, error=Exception, timeout=settings.UI.DEFAULT_TIMEOUT,
                    interval=settings.UI.DEFAULT_CHECKING_INTERVAL, check=True, **kwargs):
        """A custom function to wait for the passed function to succeed"""
        log_msg = f'Waiting for successfully method "{method.__name__}" execution'
        with allure.step(log_msg):
            self.logger.info(log_msg)

            st = time.perf_counter()
            last_exception = None
            i = 0
            while time.perf_counter() - st < timeout:
                try:
                    i += 1
                    log_msg = f'Method execution: "{method.__name__}". Try: {i}'
                    with allure.step(log_msg):
                        self.logger.debug(log_msg)
                        result = method(*args, **kwargs)
                        if check:
                            if result:
                                self.logger.debug(f'Method "{method.__name__}" execution result: "{result}"')
                                return result
                            last_exception = f'Method "{method.__name__}" returned "{result}"'
                        else:
                            self.logger.debug(f'Method "{method.__name__}" execution result: "{result}"')
                            return result
                except error as e:
                    last_exception = e
                time.sleep(interval)

            raise exceptions.CustomWaitTimeoutException(
                f'Method {method.__name__} timeout in {timeout}sec with exception: "{last_exception}"')

    def get_page_loaded_time(self):
        """Returns the time when the page was loaded"""
        return self.driver.execute_script(JsCode.dom_complete_time) / 1000

    @contextmanager
    def is_page_reloaded__context_manager(self):
        """Checks that the page has been reloaded.
        Compares page loaded time before and after block 'with'"""
        start_time = self.get_page_loaded_time()
        yield
        end_time = self.get_page_loaded_time()
        if start_time == end_time:
            raise exceptions.CheckingException("Page has not been reloaded")

    @contextmanager
    def is_page_not_reloaded__context_manager(self):
        """Checks that the page has not been reloaded.
        Compares page loaded time before and after block 'with'"""
        start_time = self.get_page_loaded_time()
        yield
        end_time = self.get_page_loaded_time()
        if start_time != end_time:
            raise exceptions.CheckingException("Page has been reloaded")

    class _Check:
        _page = None

        def __init__(self, page):
            self._page = page

        def _raise_exception_wrapper(self, exc, exc_msg, raise_exception, result=False):
            self._page.logger.debug(f'Raised exception "{exc.__name__}" with message: "{exc_msg}"')
            if raise_exception:
                raise exc(exc_msg)
            else:
                return result

        def _is_element_visible(self, element):
            try:
                result = self._page.driver.execute_script(JsCode.is_visible, element)
                self._page.logger.debug(f'Element "{element.tag_name}" visibility status: "{result}"')
                return result
            except (JavascriptException, StaleElementReferenceException):
                self._page.logger.debug(f'Element is not visible or stale')
                return False

        def is_element_visible(self, element, raise_exception=False):
            """Checking that an element is visible"""
            self._page.logger.debug(f'Checking that element is visible')
            if self._is_element_visible(element):
                return True

            exc_msg = f'Element is not visible'
            return self._raise_exception_wrapper(exceptions.ElementNotVisibleException, exc_msg, raise_exception)

        def is_visible(self, locator, raise_exception=False):
            """Checking that an element found by locator is visible"""
            self._page.logger.debug(f'Checking that element found by locator '
                                    f'"{locator[1]}" (type: {locator[0]}) is visible')

            elem = self._page.find(locator)
            if self.is_element_visible(elem, raise_exception=False):
                self._page.logger.debug(
                    f'Element found by locator "{locator[1]}" (type: {locator[0]}) is visible')
                return True
            else:
                self._page.logger.debug(
                    f'Element found by locator "{locator[1]}" (type: {locator[0]}) is not visible')

                exc_msg = f'Element found by locator "{locator[1]}" (type: {locator[0]}) is not visible'
                return self._raise_exception_wrapper(exceptions.ElementNotVisibleException, exc_msg, raise_exception)

        def is_element_not_visible(self, element, raise_exception=False):
            """Checking that an element is not visible"""
            self._page.logger.debug(f'Checking that element is not visible')

            if not self._is_element_visible(element):
                return True

            exc_msg = f'Element is visible'
            return self._raise_exception_wrapper(exceptions.ElementVisibleException, exc_msg, raise_exception)

        def is_not_visible(self, locator, raise_exception=False):
            """Checking that an element found by locator is not visible"""
            self._page.logger.debug(
                f'Checking that element found by locator "{locator[1]}" (type: {locator[0]}) is not visible')
            try:
                elem = self._page.fast_find(locator)
            except exceptions.FindingException:
                self._page.logger.debug(f'Element is not founded by locator "{locator[1]}" (type: {locator[0]})')
                return True

            if self.is_element_not_visible(elem, raise_exception=raise_exception):
                self._page.logger.debug(
                    f'Element found by locator "{locator[1]}" (type: {locator[0]}) is not visible')
                return True
            else:
                self._page.logger.debug(
                    f'Element found by locator "{locator[1]}" (type: {locator[0]}) is visible')

            exc_msg = f'Element found by "{locator[1]}" (type: {locator[0]}) is visible'
            return self._raise_exception_wrapper(exceptions.ElementVisibleException, exc_msg, raise_exception)

        def is_exists(self, locator, raise_exception=False):
            """Checking that an element found by locator exists"""
            self._page.logger.debug(f'Checking that element found by locator '
                                    f'"{locator[1]}" (type: {locator[0]}) does not exists')
            try:
                elem = self._page.driver.find_element(*locator)
                if elem:
                    self._page.logger.debug(
                        f'Element found by locator "{locator[1]}" (type: {locator[0]}) exists')
                    return True
            except NoSuchElementException:
                pass

            exc_msg = f'Element "{locator[1]}" (type: {locator[0]}) is not found'
            return self._raise_exception_wrapper(exceptions.ElementNotExistsException, exc_msg, raise_exception)

        def is_not_exists(self, locator, raise_exception=False):
            """Checking that an element found by locator does not exist"""
            self._page.logger.debug(f'Checking that element found by locator '
                                    f'"{locator[1]}" (type: {locator[0]}) exists')
            try:
                elem = self._page.driver.find_element(*locator)
                if elem:
                    exc_msg = f'Element "{elem.tag_name}" found by {locator[1]} (type: {locator[0]}) exists'
                    return self._raise_exception_wrapper(exceptions.ElementExistsException, exc_msg, raise_exception)
            except (NoSuchElementException, StaleElementReferenceException):
                pass
            self._page.logger.debug(
                f'Element found by {locator[1]} (type: {locator[0]}) does not exists')
            return True

        def is_element_text_equal(self, elem, text, raise_exception=False):
            """Checking that the text of an element is equal to the given text"""
            self._page.logger.debug(
                f'Checking that element "{elem.tag_name}" text "{elem.text}" == given text "{text}"')
            if elem.text == text:
                self._page.logger.debug(f'Element text "{elem.text}" == given text "{text}"')
                return True
            else:
                exc_msg = f'Element text "{elem.text}" != given text "{text}"'
                return self._raise_exception_wrapper(exceptions.ComparisonException, exc_msg, raise_exception)

        def is_element_text_not_equal(self, elem, text, raise_exception=False):
            """Checking that the text of an element is not equal to the given text"""
            self._page.logger.debug(
                f'Checking that element "{elem.tag_name}" text "{elem.text}" != given text "{text}"')
            if elem.text != text:
                self._page.logger.debug(f'Element text "{elem.text}" != given text "{text}"')
                return True
            else:
                exc_msg = f'Element text "{elem.text}" == given text "{text}"'
                return self._raise_exception_wrapper(exceptions.ComparisonException, exc_msg, raise_exception)

        def is_links_equal(self, url_1, url_2, raise_exception=False):
            """Url comparison without arguments"""
            self._page.logger.debug(f'Checking that URLs equal: "{url_1}" == "{url_2}"')
            urls = (url_1, url_2)
            new_urls = []
            for url in urls:
                url = url.split("?")[0]
                url = url.split("#")[0]
                url = url.rstrip("/")
                new_urls.append(url)
            new_url_1, new_url_2 = new_urls
            result = new_url_1 == new_url_2
            if result:
                self._page.logger.debug(f'URLs "{url_1}" == URL "{url_2}"')
                return True
            else:
                exc_msg = f'URL "{url_1}" != URL "{url_2}"'
                return self._raise_exception_wrapper(exceptions.ComparisonException, exc_msg, raise_exception)

        def is_page_url_match_driver_url(self, raise_exception=False):
            """Checking that the current url matches the url of the page"""
            url_1 = self._page.driver.current_url
            url_2 = self._page.URL
            self._page.logger.debug(
                f'Checking that current URL "{url_1}" == {self._page.__class__.__name__} page URL {url_2}')
            result = self.is_links_equal(url_1, url_2, raise_exception=False)
            if result:
                return True

            exc_msg = f'Current url "{url_1}" does not match page object url "{url_2}"'
            return self._raise_exception_wrapper(exceptions.PageUrlDoesNotMatchDriverUrl, exc_msg, raise_exception)

        def is_page_opened(self, url=None, check_url=True, raise_exception=False):
            """Checking that the page has been opened and fully loaded"""
            self._page.logger.debug('Checking that the page has been opened and fully loaded')

            if check_url:
                url = url if url else self._page.URL
                current_url = self._page.driver.current_url
                if not self.is_links_equal(current_url, url, raise_exception=False):
                    exc_msg = f'Current URL "{current_url}" != page URL "{url}"'
                    return self._raise_exception_wrapper(exceptions.PageNotOpenedException, exc_msg, raise_exception)
                else:
                    self._page.logger.debug(f'Current URL "{current_url}" == page URL "{url}"')

            status = self._page.driver.execute_script(JsCode.document_ready_state)
            expected = "complete"
            if not status == expected:
                exc_msg = f'Current page loading status "{status}" != expected status "{expected}"'
                return self._raise_exception_wrapper(exceptions.PageNotOpenedException, exc_msg, raise_exception)
            else:
                self._page.logger.debug(f'Current page loading status "{status}" == expected status "{expected}"')

            result = self._page.is_opened()
            if not result:
                exc_msg = "Page is not opened"
                return self._raise_exception_wrapper(exceptions.PageNotOpenedException, exc_msg, raise_exception)

            self._page.logger.debug(f'Page (URL: {self._page.driver.current_url}) has been opened and fully loaded')
            return True

    class _WaitUntil(_Check):
        _error = exceptions.CheckingException

        def __init__(self, page):
            super().__init__(page)
            methods = inspect.getmembers(self)
            methods = [a for a in methods if inspect.ismethod(a[1]) and not a[0].startswith('_')]

            for k, v in methods:
                setattr(self, k, self.wait_decorator(self._wait)(v))

        def _wait(self, method, *args, timeout=settings.UI.DEFAULT_TIMEOUT,
                  interval=settings.UI.DEFAULT_CHECKING_INTERVAL, check=True, **kwargs):
            return self._page.custom_wait(method, *args, timeout=timeout, interval=interval, check=check,
                                          error=self._error, **kwargs)

        @staticmethod
        def wait_decorator(waiter):
            def inner(func):
                @wraps(func)
                def wrapper(*args, **kwargs):
                    kwargs['raise_exception'] = False
                    return waiter(func, *args, **kwargs)

                return wrapper

            return inner
