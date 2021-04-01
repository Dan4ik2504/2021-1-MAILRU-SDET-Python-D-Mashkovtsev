from contextlib import contextmanager


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

    def __exit__(self, *args, **kwargs):
        self.close()
