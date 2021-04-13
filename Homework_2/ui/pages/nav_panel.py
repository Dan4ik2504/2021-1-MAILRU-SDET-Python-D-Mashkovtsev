import allure

from ui.pages.dashboard_page import DashboardPage
from ui.pages.segments_page import SegmentsPage
from ui.pages.base_page_auth import BasePageAuth


class NavPanel(BasePageAuth):
    """The object of the navbar displayed after authorization, with methods for navigating to the pages"""

    @allure.step("Going to dashboard page")
    def go_to_dashboard(self):
        """Redirects to a dashboard page and returns an object for that page"""
        self.logger.info("Opening dashboard page")
        self.click(self.locators.NavPanel.DASHBOARD)
        dashboard_page = DashboardPage(driver=self.driver)
        dashboard_page.custom_wait(dashboard_page.check.is_page_opened)
        self.logger.info("Dashboard page opened")
        return dashboard_page

    @allure.step("Going to segments page")
    def go_to_segments(self):
        """Redirects to a segments page and returns an object for that page"""
        self.logger.info("Opening segments page")
        self.click(self.locators.NavPanel.SEGMENTS)
        segments_page = SegmentsPage(driver=self.driver)
        segments_page.open_page()
        segments_page.custom_wait(segments_page.check.is_page_opened)
        self.logger.info("Segments page opened")
        return segments_page
