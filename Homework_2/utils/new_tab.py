import logging
import allure

import settings

logger = logging.getLogger(settings.Logging.LOGGER_NAME)


class NewTab:

    def __init__(self, driver):
        self.driver = driver
        self.original_tab = self.driver.current_window_handle

    def open(self):
        allure.step("Opening new tab")
        self.driver.execute_script("window.open('');")
        self.new_tab = self.driver.window_handles[-1]
        self.driver.switch_to.window(self.new_tab)
        logger.info(f"New tab opened")
        return self.new_tab

    def close(self):
        allure.step("Closing new tab")
        self.driver.close()
        self.driver.switch_to.window(self.original_tab)
        logger.info(f"New tab closed")

    def __enter__(self):
        return self.open()

    def __exit__(self, *args, **kwargs):
        self.close()
