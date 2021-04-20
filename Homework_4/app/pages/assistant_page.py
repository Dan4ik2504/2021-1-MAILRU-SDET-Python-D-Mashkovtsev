import dataclasses

import allure
from selenium.common.exceptions import NoSuchElementException

from app.pages.base_page import BasePage
from app.locators.assistant_page import AssistantPageLocators


@dataclasses.dataclass
class DialogFactCard:
    title: str
    text: str


class AssistantPage(BasePage):
    locators = AssistantPageLocators

    @allure.step("Opening the keyboard")
    def open_keyboard(self):
        self.click(self.locators.OPEN_KEYBOARD_BUTTON)
        self.logger.info("Keyboard is open")

    @allure.step("Opening the assistant menu")
    def open_assistant_menu(self):
        self.click(self.locators.OPEN_ASSISTANT_MENU_BUTTON)
        self.logger.info("Assistant menu is open")

    @allure.step("Sending text to an assistant")
    def send_text_to_assistant(self, text):
        if self.check.is_not_visible(self.locators.INPUT_TEXT_FIELD, raise_exception=False):
            self.open_keyboard()

        self.fill_field(self.locators.INPUT_TEXT_FIELD, text)
        self.click(self.locators.SEND_TEXT_BUTTON)
        self.hide_keyboard()
        self.logger.info("Text sent to assistant")

    @allure.step("Getting visible fact cards")
    def get_visible_fact_cards(self):
        elements = self.find_elements(self.locators.DIALOG_FACT_CARD)
        cards_objects = []
        for element in elements:
            try:
                title = element.find_element(*self.locators.DIALOG_FACT_CARD_TITLE).text
            except NoSuchElementException:
                title = None
                
            try:
                text = element.find_element(*self.locators.DIALOG_FACT_CARD_TEXT).text
            except NoSuchElementException:
                text = None

            card_obj = DialogFactCard(title=title, text=text)
            cards_objects.append(card_obj)
        self.logger.info(f'Got {len(cards_objects)} fact cards')
        self.logger.debug(f'Fact cards: '
                          f'{"; ".join(["{}: {}".format(card.title, card.text[:100]) for card in cards_objects])}')
        return cards_objects
    
    @allure.step("Getting visible suggest text")
    def get_visible_suggest_text(self):
        elements = self.find_elements(self.locators.SUGGEST_TEXT_ITEM)
        self.logger.info(f'Got {len(elements)} suggestions')
        self.logger.debug(f'Suggestions: {"; ".join([str(elem.text) for elem in elements if elem.text is not None])}')
        return elements
