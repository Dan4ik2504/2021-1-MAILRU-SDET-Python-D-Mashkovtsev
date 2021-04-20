import dataclasses
import logging
import time

import allure
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from appium.webdriver.common.touch_action import TouchAction

from app.locators.base_page import BasePageLocators
import settings
import exceptions
from appium.webdriver.webdriver import WebDriver


@dataclasses.dataclass
class Coordinates:
    x_center: int
    y_center: int
    x_left: int
    x_right: int
    y_top: int
    y_bottom: int


class BasePage:
    locators = BasePageLocators()
    logger = logging.getLogger(settings.Logging.LOGGER_NAME)

    class SwipeTo:
        TOP = "top"
        BOTTOM = "bottom"
        LEFT = "left"
        RIGHT = "right"

    def __init__(self, driver):
        self.driver: WebDriver = driver
        self.screen_coordinates = self.get_screen_coordinates()
        self.check = self._Check(self)

    def get_screen_coordinates(self, indent: float = settings.Basic.DEFAULT_INDENT_PERCENT):
        """
        Returns an instance of the Coordinates class with screen coordinates

        :param indent: Offset from the borders of the screen as a percentage of the width (in the case of X) and
        height (in the case of Y) of the screen
        """

        dimension = self.driver.get_window_size()

        x_center = int(dimension['width'] / 2)
        y_center = int(dimension['height'] / 2)
        y_top = int(dimension['height'] * indent)
        y_bottom = int(dimension['height'] * (1 - indent))
        x_left = int(dimension['width'] * indent)
        x_right = int(dimension['width'] * (1 - indent))

        coordinates = Coordinates(x_center=x_center, y_center=y_center, y_top=y_top, y_bottom=y_bottom, x_left=x_left,
                                  x_right=x_right)
        self.logger.debug(f'Screen coordinates: {str(dataclasses.asdict(coordinates))}')

        return coordinates

    def wait(self, timeout=settings.Basic.DEFAULT_TIMEOUT):
        """WebDriverWait"""
        return WebDriverWait(self.driver, timeout=timeout)

    @property
    def touch_action(self):
        """TouchAction"""
        return TouchAction(self.driver)

    def hide_keyboard(self):
        """Hiding the system keyboard"""
        self.driver.hide_keyboard()

    def find(self, locator, timeout=settings.Basic.DEFAULT_TIMEOUT):
        """Finding element by locator"""
        log_msg = f'Searching of the element by locator: "{locator[1]}" (type: {locator[0]})'
        with allure.step(log_msg):
            self.logger.info(log_msg)
            try:
                element = self.wait(timeout).until(EC.presence_of_element_located(locator))
                self.logger.info(f'Element have been found')
                return element
            except TimeoutException:
                raise exceptions.ElementNotFound(f'Element not found by locator: "{locator[1]}" (type: {locator[0]})')

    def fast_find(self, locator):
        """Finding element by locator without waiting"""
        log_msg = f'Fast searching of the element by locator: "{locator[1]}" (type: {locator[0]})'
        with allure.step(log_msg):
            self.logger.info(log_msg)
            try:
                element = self.driver.find_element(*locator)
                self.logger.info(f'Element have been found')
                return element
            except (NoSuchElementException, StaleElementReferenceException):
                raise exceptions.ElementNotFound(f'Element not found by locator: "{locator[1]}" (type: {locator[0]})')

    def find_elements(self, locator):
        """Finding an elements by locator"""
        log_msg = f'Searching elements by locator: "{locator[1]}" (type: {locator[0]})'
        with allure.step(log_msg):
            self.logger.info(log_msg)
            elements = self.driver.find_elements(*locator)

            if len(elements) > 0:
                self.logger.info(f'{len(elements)} element(s) have been found')
            else:
                self.logger.info(f'No elements found')
            return elements

    @allure.step('Fill field "{locator}" by text "{text}"')
    def fill_field(self, locator, text):
        """Filling a field with text"""
        self.logger.info(f'Fill field "{locator[1]}" (type: {locator[0]}) by "{text}"')
        element = self.wait().until(EC.visibility_of_element_located(locator))
        self.custom_wait(self.check.is_visible, locator)
        element.clear()
        element.send_keys(text)

    def swipe(self, x_start, y_start, x_end, y_end, swipetime=settings.Basic.DEFAULT_SWIPE_TIME_MS):
        """
        Swipe to the given coordinates

        :param x_start: Swipe start coordinate
        :param y_start: Swipe start coordinate
        :param x_end: Swipe end coordinate
        :param y_end: Swipe end coordinate
        :param swipetime: Swipe time
        """
        self.touch_action. \
            press(x=x_start, y=y_start). \
            wait(ms=swipetime). \
            move_to(x=x_end, y=y_end). \
            release(). \
            perform()

    @allure.step("Swipe top")
    def swipe_top(self, x_center=None, y_top=None, y_bottom=None, swipetime=settings.Basic.DEFAULT_SWIPE_TIME_MS,
                  swipe_length=1):
        """
        Swipe to the top at the specified coordinates.
        By default, uses window coordinates

        :param y_bottom: Bottom coordinate of the swipe. Specified if swipe direction is 'top' or 'bottom'
        :param y_top: Top coordinate of the swipe. Specified if swipe direction is 'top' or 'bottom'
        :param x_center: X-axis coordinate of the swipe. Specified if swipe direction is 'top' or 'bottom'
        :param swipe_length: Swipe length as a percentage of the original swipe length (max = 1)
        :param swipetime: Swipe time
        """
        self.logger.info("Swipe top")
        x = x_center if x_center else self.screen_coordinates.x_center
        y_start = y_bottom if y_bottom else self.screen_coordinates.y_bottom
        y_end = y_top if y_top else self.screen_coordinates.y_top
        y_end = int(y_start - ((y_start - y_end) * swipe_length))
        self.swipe(x_start=x, x_end=x, y_start=y_start, y_end=y_end, swipetime=swipetime)

    @allure.step("Swipe bottom")
    def swipe_bottom(self, x_center=None, y_top=None, y_bottom=None, swipetime=settings.Basic.DEFAULT_SWIPE_TIME_MS,
                     swipe_length=1):
        """
        Swipe to the bottom at the specified coordinates.
        By default, uses window coordinates

        :param y_bottom: Bottom coordinate of the swipe. Specified if swipe direction is 'top' or 'bottom'
        :param y_top: Top coordinate of the swipe. Specified if swipe direction is 'top' or 'bottom'
        :param x_center: X-axis coordinate of the swipe. Specified if swipe direction is 'top' or 'bottom'
        :param swipe_length: Swipe length as a percentage of the original swipe length (max = 1)
        :param swipetime: Swipe time
        """
        self.logger.info("Swipe bottom")
        x = x_center if x_center else self.screen_coordinates.x_center
        y_start = y_top if y_top else self.screen_coordinates.y_top
        y_end = y_bottom if y_bottom else self.screen_coordinates.y_bottom
        y_end = int(y_start + ((y_end - y_start) * swipe_length))
        self.swipe(x_start=x, x_end=x, y_start=y_start, y_end=y_end, swipetime=swipetime)

    @allure.step("Swipe left")
    def swipe_left(self, y_center=None, x_left=None, x_right=None, swipetime=settings.Basic.DEFAULT_SWIPE_TIME_MS,
                   swipe_length=1):
        """
        Swipe to the left at the specified coordinates.
        By default, uses window coordinates

        :param y_center: Y-axis coordinate of the swipe. Specified if swipe direction is 'left' or 'right'
        :param x_right: Right coordinate of the swipe. Specified if swipe direction is 'left' or 'right'
        :param x_left: Left coordinate of the swipe. Specified if swipe direction is 'left' or 'right'
        :param swipe_length: Swipe length as a percentage of the original swipe length (max = 1)
        :param swipetime: Swipe time
        """
        self.logger.info("Swipe left")
        y = y_center if y_center else self.screen_coordinates.y_center
        x_start = x_right if x_right else self.screen_coordinates.x_right
        x_end = x_left if x_left else self.screen_coordinates.x_left
        x_end = int(x_start - ((x_start - x_end) * swipe_length))
        self.swipe(x_start=x_start, x_end=x_end, y_start=y, y_end=y, swipetime=swipetime)

    @allure.step("Swipe right")
    def swipe_right(self, y_center=None, x_left=None, x_right=None, swipetime=settings.Basic.DEFAULT_SWIPE_TIME_MS,
                    swipe_length=1):
        """
        Swipe to the right at the specified coordinates.
        By default, uses window coordinates

        :param y_center: Y-axis coordinate of the swipe. Specified if swipe direction is 'left' or 'right'
        :param x_right: Right coordinate of the swipe. Specified if swipe direction is 'left' or 'right'
        :param x_left: Left coordinate of the swipe. Specified if swipe direction is 'left' or 'right'
        :param swipe_length: Swipe length as a percentage of the original swipe length (max = 1)
        :param swipetime: Swipe time
        """
        self.logger.info("Swipe right")
        y = y_center if y_center else self.screen_coordinates.y_center
        x_start = x_left if x_left else self.screen_coordinates.x_left
        x_end = x_right if x_right else self.screen_coordinates.x_right
        x_end = int(x_start + ((x_end - x_start) * swipe_length))
        self.swipe(x_start=x_start, x_end=x_end, y_start=y, y_end=y, swipetime=swipetime)

    @allure.step("Swipe {direction}")
    def swipe_in_direction(self, direction: str, x_left=None, x_right=None, y_center=None, x_center=None,
                           y_top=None, y_bottom=None, swipetime=settings.Basic.DEFAULT_SWIPE_TIME_MS, swipe_length=1):
        """
        Swipe to the specified direction

        :param y_bottom: Bottom coordinate of the swipe. Specified if swipe direction is 'top' or 'bottom'
        :param y_top: Top coordinate of the swipe. Specified if swipe direction is 'top' or 'bottom'
        :param x_center: X-axis coordinate of the swipe. Specified if swipe direction is 'top' or 'bottom'
        :param y_center: Y-axis coordinate of the swipe. Specified if swipe direction is 'left' or 'right'
        :param x_right: Right coordinate of the swipe. Specified if swipe direction is 'left' or 'right'
        :param x_left: Left coordinate of the swipe. Specified if swipe direction is 'left' or 'right'
        :param direction: left, right, top, bottom
        :param swipe_length: Swipe length as a percentage of the original swipe length (max = 1)
        :param swipetime: Swipe time
        """
        self.logger.info(f"Swipe {direction}")
        if direction == self.SwipeTo.LEFT:
            self.swipe_left(y_center=y_center, x_left=x_left, x_right=x_right, swipetime=swipetime,
                            swipe_length=swipe_length)
        elif direction == self.SwipeTo.RIGHT:
            self.swipe_right(y_center=y_center, x_left=x_left, x_right=x_right, swipetime=swipetime,
                             swipe_length=swipe_length)
        elif direction == self.SwipeTo.TOP:
            self.swipe_top(x_center=x_center, y_top=y_top, y_bottom=y_bottom, swipetime=swipetime,
                           swipe_length=swipe_length)
        elif direction == self.SwipeTo.BOTTOM:
            self.swipe_bottom(x_center=x_center, y_top=y_top, y_bottom=y_bottom, swipetime=swipetime,
                              swipe_length=swipe_length)
        else:
            raise exceptions.IncorrectSwipeDirection(f'Incorrect swipe direction: {direction}')

    @allure.step("Swipe {direction} to {locator}")
    def swipe_to_element(self, locator, direction=SwipeTo.TOP, max_swipes=settings.Basic.MAX_SWIPES,
                         swipetime=settings.Basic.DEFAULT_SWIPE_TIME_MS, swipe_over_element_locator=None,
                         swipe_length=1):
        """
        Swiping until element is visible.

        :param swipe_length: Swipe length as a percentage of the original swipe length (max = 1)
        :param swipetime: Swipe time
        :param max_swipes: Max number of swipes
        :param direction: Scrolling direction
        :param locator: Locator of the element
        :param swipe_over_element_locator: If specified, swiping occurs on the element found by the given locator
        """
        self.logger.info(f'Swipe {direction} to "{locator[1]}" (type: {locator[0]})')
        already_swiped = 0
        elements = self.driver.find_elements(*locator)
        while len(elements) == 0:
            if already_swiped > max_swipes:
                raise TimeoutException(f"Error with {locator}, please check function")
            if swipe_over_element_locator:
                self.swipe_over_element(swipe_over_element_locator, direction=direction, swipetime=swipetime,
                                        swipe_length=swipe_length)
            else:
                self.swipe_in_direction(direction, swipetime=swipetime, swipe_length=swipe_length)
            already_swiped += 1
            elements = self.driver.find_elements(*locator)
        return elements[0]

    @staticmethod
    def get_element_coords(element):
        """Returns the coordinates of the element"""
        x_left = int(element.location['x'])
        x_right = int(x_left + element.rect['width'])
        x_center = (x_left + x_right) // 2
        x_indent = element.rect['width'] // 10
        x_left += x_indent
        x_right -= x_indent

        y_top = int(element.location['y'])
        y_bottom = int(y_top + element.rect['height'])
        y_center = (y_top + y_bottom) // 2
        y_indent = element.rect['height'] // 10
        y_top += y_indent
        y_bottom -= y_indent
        coordinates = Coordinates(x_left=x_left, x_right=x_right, x_center=x_center,
                                  y_top=y_top, y_bottom=y_bottom, y_center=y_center)
        return coordinates

    @allure.step("Swipe {direction} over {locator}")
    def swipe_over_element(self, locator, direction=SwipeTo.TOP, swipetime=settings.Basic.DEFAULT_SWIPE_TIME_MS,
                           swipe_length=1):
        """Swipe over element"""
        self.logger.info(f'Swipe {direction} over "{locator[1]}" (type: {locator[0]})')
        element = self.find(locator)
        coords = self.get_element_coords(element)
        self.swipe_in_direction(direction, **dataclasses.asdict(coords), swipetime=swipetime, swipe_length=swipe_length)

    def click(self, locator, timeout=settings.Basic.DEFAULT_TIMEOUT):
        """Click on an element found by locator"""
        log_msg = f'Clicking on "{locator[1]}" (type: {locator[0]})'
        with allure.step(log_msg):
            for i in range(settings.Basic.CLICK_RETRY):
                log_msg = f'Clicking. Try {i + 1} of {settings.Basic.CLICK_RETRY}...'
                with allure.step(log_msg):
                    self.logger.info(log_msg)
                    try:
                        log_msg = f'Searching of the element'
                        with allure.step(log_msg):
                            self.logger.info(log_msg)
                            elem = self.find(locator, timeout=timeout)

                        log_msg = f'Clicking on element'
                        with allure.step(log_msg):
                            self.logger.info(log_msg)
                            elem.click()
                        return
                    except (TimeoutException, StaleElementReferenceException, exceptions.ElementNotFound) as exc:
                        if i == settings.Basic.CLICK_RETRY - 1:
                            raise exc
                        self.logger.debug(f'Error thrown: {exc}. Trying click again')

    @allure.step("Waiting")
    def custom_wait(self, method, *args, error=exceptions.CheckException, timeout=settings.Basic.DEFAULT_TIMEOUT,
                    interval=settings.Basic.DEFAULT_CHECKING_INTERVAL, check=True, **kwargs):
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

            raise exceptions.WaitException(
                f'Method {method.__name__} timeout in {timeout}sec with exception: "{last_exception}"')

    class _Check:
        def __init__(self, page):
            self.page = page

        def _raise_exception_wrapper(self, exc=exceptions.CheckException, exc_msg=None, raise_exception=True,
                                     result=False):
            self.page.logger.debug(f'Raised exception "{exc.__name__}" with message: "{exc_msg}"')
            if raise_exception:
                raise exc(exc_msg)
            else:
                return result

        @staticmethod
        def _is_element_visible(element):
            try:
                return element.is_displayed()
            except StaleElementReferenceException:
                return False

        def is_element_visible(self, element, raise_exception=True):
            """Checking that an element is visible"""
            if self._is_element_visible(element):
                return True
            return self._raise_exception_wrapper(exc_msg=f'Element is not visible', raise_exception=raise_exception)

        def is_visible(self, locator, raise_exception=True):
            """Checking that an element found by locator is visible"""
            try:
                element = self.page.fast_find(locator)
                if self.is_element_visible(element, raise_exception=raise_exception):
                    return True
            except exceptions.ElementNotFound:
                pass
            return self._raise_exception_wrapper(
                exc_msg=f'Element "{locator[0]}" (type: {locator[1]}) is not visible',
                raise_exception=raise_exception)

        def is_element_not_visible(self, element, raise_exception=True):
            """Checking that an element is not visible"""
            if not self._is_element_visible(element):
                return True
            return self._raise_exception_wrapper(exc_msg=f'Element is visible', raise_exception=raise_exception)

        def is_not_visible(self, locator, raise_exception=True):
            """Checking that an element found by locator is not visible"""
            try:
                element = self.page.fast_find(locator)
            except exceptions.ElementNotFound:
                return True
            if self.is_element_not_visible(element, raise_exception=raise_exception):
                return True
            return self._raise_exception_wrapper(
                exc_msg=f'Element "{locator[0]}" (type: {locator[1]}) is visible',
                raise_exception=raise_exception)

        def is_new_element_located(self, locator, elements_count, raise_exception=True):
            """Checking that the number of existing elements is greater than the given one"""
            elements = self.page.find_elements(locator)
            if len(elements) > elements_count:
                return True
            return self._raise_exception_wrapper(
                exc_msg=f'New elements "{locator[0]}" (type: {locator[1]}) is not located. '
                        f'{len(elements)} elements exists',
                raise_exception=raise_exception)
