from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC

import settings


class BasePage:
    """Базовый объект страницы"""
    URL = settings.BASE_URL

    def __init__(self, driver):
        self.driver = driver

    def open_page(self, url=None):
        """Открыть страницу в браузере"""
        self.driver.get(url if url else self.URL)

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
                self.wait(timeout).until(self.is_page_loaded)
                return self.wait(timeout).until(EC.element_to_be_clickable(locator)).click()
            except (TimeoutException, StaleElementReferenceException) as exc:
                if i == settings.CLICK_RETRY - 1:
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
        """Возвращает значение, записанное в поле input"""
        return self.find(locator).get_attribute("value")

    def checking_in_new_tab(self, check_func, *args, **kwargs):
        """Запускает функцию внутри новой вкладки"""
        with self.NewTab(self.driver):
            return check_func(self, *args, **kwargs)

    def checking_in_new_tab_wrapper(self, check_func, open_new_tab=True, *args, **kwargs):
        """Решает, открывать ли новую вкладку, в зависимости от флага open_new_tab"""
        if open_new_tab:
            return self.checking_in_new_tab(check_func=check_func, open_new_tab=open_new_tab, *args, **kwargs)
        else:
            return check_func(self, open_new_tab=open_new_tab, *args, **kwargs)

    @staticmethod
    def is_page_loaded(driver):
        """Возвращает True, если страница загружена"""
        return driver.execute_script("return document.readyState") == "complete"

    class NewTab:
        """Новая вкладка"""
        def __init__(self, driver):
            self.driver = driver
            self.original_tab = self.driver.current_window_handle

        def open(self):
            """Открыть вкладку"""
            self.driver.execute_script("window.open('');")
            self.new_tab = self.driver.window_handles[-1]
            self.driver.switch_to.window(self.new_tab)
            return self.new_tab

        def close(self):
            """Закрыть вкладку"""
            self.driver.close()
            self.driver.switch_to.window(self.original_tab)

        def __enter__(self):
            return self.open()

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.close()
