import re

import allure
import pytest

import settings
from test_app.base import BaseCase


class TestAssistant(BaseCase):
    @allure.title("Get country information")
    @pytest.mark.AndroidUI
    def test_get_country_info(self):
        with allure.step("Sending text to assistant"):
            self.assistant_page.send_text_to_assistant("Russia")

            self.assistant_page.custom_wait(self.assistant_page.check.is_visible,
                                            locator=self.assistant_page.locators.DIALOG_FACT_CARD)

        with allure.step("Checking that the card exists"):
            dialog_objects = self.assistant_page.get_visible_dialog_objects()
            assert len(dialog_objects) > 2

            card = dialog_objects[-2]

            assert card.title == "Россия"
            assert card.text.startswith("Росси́я, другое официальное название - Росси́йская Федера́ция, - "
                                        "государство в Восточной Европе и Северной Азии. ")

        with allure.step("Clicking on suggest"):
            suggest_text = "численность населения россии"
            self.assistant_page.click_on_suggest(suggest_text)

            self.assistant_page.custom_wait(self.assistant_page.check.is_new_element_located,
                                            locator=self.assistant_page.locators.DIALOG_FACT_CARD,
                                            elements_count=1)

        with allure.step("Checking that the card exists"):
            dialog_objects = self.assistant_page.get_visible_dialog_objects()
            assert len(dialog_objects) > 2

            card = dialog_objects[-2]

            assert card.title == "146 млн."
            assert card.text == "Россия"

    @allure.title("Test calculator")
    @pytest.mark.AndroidUI
    @pytest.mark.parametrize(
        ("expression", "answer"),
        (
                ("2 + 2", "4"),
                ("623 * 32", "19936")
        )
    )
    def test_calculator(self, expression, answer):
        items_number = self.assistant_page.get_visible_dialog_elements_count()
        self.assistant_page.send_text_to_assistant(expression)
        self.assistant_page.custom_wait(self.assistant_page.check.is_new_element_located,
                                        locator=self.assistant_page.locators.DIALOG_ITEM,
                                        elements_count=items_number)
        items_list = self.assistant_page.get_visible_dialog_objects()
        request_obj = items_list[-2]
        response_obj = items_list[-1]
        assert request_obj.text == expression
        assert response_obj.text == answer


class TestSettings(BaseCase):
    @allure.title("News source change test")
    @pytest.mark.AndroidUI
    def test_check_source(self):
        with allure.step("Opening news sources page"):
            settings_page = self.assistant_page.go_to_settings_page()

            news_sources = settings_page.go_to_news_sources_setup_page()

        with allure.step("Selecting a news source"):
            news_sources.select_source(news_sources.SOURCES.VESTI_FM)
            checked_source = news_sources.get_checked_source()
            assert checked_source == news_sources.SOURCES.VESTI_FM

        with allure.step("Opening assistant page"):
            self.driver.back()
            self.driver.back()
            self.assistant_page.custom_wait(self.assistant_page.is_opened)

        with allure.step("Checking news source"):
            self.assistant_page.send_text_to_assistant("News")
            player_elem = self.assistant_page.find(self.assistant_page.locators.PLAYER_TRACK_NAME)
            assert player_elem.text == "Вести ФМ"

    @allure.title("About app page test")
    @pytest.mark.AndroidUI
    def test_about_app(self):
        with allure.step("Opening about app page"):
            settings_page = self.assistant_page.go_to_settings_page()
            about_app_page = settings_page.go_to_about_app_page()

        with allure.step("Comparison of application versions"):
            app_version_on_page = about_app_page.get_app_version()
            app_version_in_file_name = re.findall(r"^\w+?_v(?P<version>[\d\.]+?)\.apk$", settings.App.NAME)[0]
            assert app_version_on_page == app_version_in_file_name

        with allure.step("Checking for the presence of a trademark"):
            assert re.match(r"^Mail\.ru Group © \d{4}–\d{4}\. Все права защищены\.$",
                            about_app_page.get_about_copyright_text())
