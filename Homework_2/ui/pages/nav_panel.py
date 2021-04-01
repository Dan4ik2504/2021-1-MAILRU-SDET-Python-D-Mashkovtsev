import allure

class NavPanel:
    def __init__(self, page):
        self.page = page

    @allure.step("Going to dashboard page")
    def dashboard(self):
        if self.__class__.__name__ != "DashboardPage":
            from ui.pages.dashboard_page import DashboardPage
            self.page.click(self.page.locators.NavPanel.DASHBOARD)
            current_page = DashboardPage(driver=self.page.driver)
            current_page.wait_until_load()
            self.page.logger.info("Dashboard page opened")
            return current_page
        else:
            return self.page

    @allure.step("Going to segments page")
    def segments(self):
        if self.__class__.__name__ != "SegmentsPage":
            from ui.pages.segments_page import SegmentsPage
            self.page.click(self.page.locators.NavPanel.SEGMENTS)
            current_page = SegmentsPage(driver=self.page.driver)
            current_page.wait_until_load()
            self.page.logger.info("Segments page opened")
            return current_page
        else:
            return self.page