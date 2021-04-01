class NavPanel:
    def __init__(self, page):
        self.page = page

    def dashboard(self):
        if self.__class__.__name__ != "DashboardPage":
            from ui.pages.dashboard_page import DashboardPage
            self.page.click(self.page.locators.NavPanel.DASHBOARD)
            current_page = DashboardPage(driver=self.page.driver)
            current_page.wait_until_load()
            return current_page
        else:
            return self.page

    def segments(self):
        if self.__class__.__name__ != "SegmentsPage":
            from ui.pages.segments_page import SegmentsPage
            self.page.click(self.page.locators.NavPanel.SEGMENTS)
            current_page = SegmentsPage(driver=self.page.driver)
            current_page.wait_until_load()
            return current_page
        else:
            return self.page