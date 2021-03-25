import pytest

from selenium.webdriver.support import expected_conditions as EC

from base_tests.base import BaseCaseNoAuth, BaseCaseAuth
from ui.locators import pages_locators

import settings


class TestLoginLogout(BaseCaseNoAuth):
    @pytest.mark.UI
    def test_login(self):
        self.main_page_no_auth.login()
        assert self.driver.current_url == settings.DASHBOARD_URL

    @pytest.mark.UI
    def test_logout(self):
        self.main_page_no_auth.login()
        assert self.base_page_auth.is_authorized(open_new_tab=False)
        self.base_page_auth.logout()
        assert self.driver.current_url == settings.BASE_URL


class TestUI(BaseCaseAuth):
    @pytest.mark.parametrize(
        ("new_text", "prev_text", "locator"),
        [
            ("Гвидо ван Россум", settings.USERNAME, pages_locators.ProfilePage.NAME_FIELD),
            ("+79999999999", settings.PHONE, pages_locators.ProfilePage.PHONE_FIELD),
            ("poiuytrewq@bombaya.com", settings.EMAIL, pages_locators.ProfilePage.EMAIL_FIELD),
        ]
    )
    @pytest.mark.UI
    def test_edit_contact_information(self, new_text, prev_text, locator):
        self.base_page_auth.click(self.base_page_auth.locators.NavPanel.PROFILE)
        self.base_page_auth.wait().until(EC.url_changes(settings.DASHBOARD_URL))
        assert settings.PROFILE_URL in self.driver.current_url

        self.profile_page.change_contacts_info_data(locator, new_text)
        self.driver.refresh()

        element_text = self.profile_page.get_input_value(locator)
        assert element_text == new_text

        # Возвращаем старое значение
        self.profile_page.change_contacts_info_data(locator, prev_text)

    @pytest.mark.parametrize(
        ("locator", "url"),
        [
            (pages_locators.BasePageAuth.NavPanel.STATISTICS, settings.STATISTICS_URL),
            (pages_locators.BasePageAuth.NavPanel.TOOLS, settings.TOOLS_URL),
        ]
    )
    @pytest.mark.UI
    def test_navpanel(self, locator, url):
        self.base_page_auth.click(locator)
        self.base_page_auth.wait().until(EC.url_changes(settings.DASHBOARD_URL))
        assert url in self.driver.current_url
