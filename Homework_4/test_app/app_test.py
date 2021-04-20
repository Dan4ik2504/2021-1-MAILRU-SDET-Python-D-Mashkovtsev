import allure
import pytest

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
            cards = self.assistant_page.get_visible_fact_cards()
            assert len(cards) == 1
            card = cards[0]

            assert card.title == "Россия"
            assert card.text.startswith("Росси́я, другое официальное название - Росси́йская Федера́ция, - "
                                        "государство в Восточной Европе и Северной Азии. ")

        with allure.step("Clicking on suggest"):
            suggest_text = "численность населения россии"
            suggest_locator = self.assistant_page.locators.SUGGEST_TEXT_ITEM_WITH_TEXT_BASE
            suggest_locator = (suggest_locator[0], suggest_locator[1].format(text=suggest_text))
            suggest_elem = self.assistant_page.swipe_to_element(
                locator=suggest_locator, direction=self.assistant_page.SwipeTo.LEFT,
                swipe_over_element_locator=self.assistant_page.locators.SUGGEST_LIST, swipe_length=0.3)
            assert suggest_elem.text == suggest_text
            suggest_elem.click()

            self.assistant_page.custom_wait(self.assistant_page.check.is_new_element_located,
                                            locator=self.assistant_page.locators.DIALOG_FACT_CARD,
                                            elements_count=1)

        with allure.step("Checking that the card exists"):
            cards = self.assistant_page.get_visible_fact_cards()
            assert len(cards) == 2

            card = cards[-1]

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
        item_locator = self.assistant_page.locators.DIALOG_ITEM
        items_number = len(self.assistant_page.find_elements(item_locator))
        self.assistant_page.send_text_to_assistant(expression)
        self.assistant_page.custom_wait(self.assistant_page.check.is_new_element_located,
                                        locator=item_locator, elements_count=items_number)
        items_list = self.assistant_page.get_visible_dialog_items_text()
        item = items_list[-1]
        assert item == answer
