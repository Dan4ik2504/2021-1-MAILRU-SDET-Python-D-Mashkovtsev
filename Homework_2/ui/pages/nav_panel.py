import allure

from ui.pages.dashboard_page import DashboardPage
from ui.pages.segments_page import SegmentsPage
from ui.pages.base_page_auth import BasePageAuth


class NavPanel(BasePageAuth):

    @allure.step("Going to dashboard page")
    def go_to_dashboard(self):
        self.click(self.locators.NavPanel.DASHBOARD)
        dashboard_page = DashboardPage(driver=self.driver)
        dashboard_page.wait_until_load()
        self.logger.info("Dashboard page opened")
        return dashboard_page

    @allure.step("Going to segments page")
    def go_to_segments(self):
        self.click(self.locators.NavPanel.SEGMENTS)
        segments_page = SegmentsPage(driver=self.driver)
        segments_page.wait_until_load()
        self.logger.info("Segments page opened")
        return segments_page
