import dataclasses

import allure
from selenium.common.exceptions import NoSuchElementException

import exceptions
from app.pages.base_page import BasePage
from app.pages.settings_page import SettingsPage
from app.locators.assistant_page import AssistantPageLocators


@dataclasses.dataclass
class DialogFactCard:
    title: str
    text: str


class AssistantPage(BasePage):
    locators = AssistantPageLocators
    
    def is_opened(self):
        return self.check.is_visible(self.locators.TOOLBAR, raise_exception=False)

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
                text = element.find_element(*self.locators.DIALOG_FACT_CARD_TEXT).text
            except NoSuchElementException:
                continue
            else:
                card_obj = DialogFactCard(title=title, text=text)
                cards_objects.append(card_obj)
        self.logger.info(f'Got {len(cards_objects)} fact cards')
        self.logger.debug(f'Fact cards: '
                          f'{"; ".join(["{}: {}".format(card.title, card.text[:100]) for card in cards_objects])}')
        return cards_objects
    
    @allure.step("Getting visible suggestions")
    def get_visible_suggestions_elements(self):
        elements = self.find_elements(self.locators.SUGGEST_TEXT_ITEM)
        self.logger.info(f'Got {len(elements)} suggestions')
        self.logger.debug(f'Suggestions: {"; ".join([str(elem.text) for elem in elements if elem.text is not None])}')
        return elements

    @allure.step("Getting visible dialog items")
    def get_visible_dialog_items_text(self):
        elements = self.find_elements(self.locators.DIALOG_ITEM)
        items_text = []
        for element in elements:
            items_text.append(element.text)
        self.logger.info(f'Got {len(items_text)} items')
        self.logger.debug(f'Items: {"; ".join(items_text)}')
        return items_text

    @allure.step("Settings page opening")
    def go_to_settings_page(self):
        """Opens settings page and returns settings page object"""
        buttons_locators = (self.locators.OPEN_SETTINGS_BUTTON, self.locators.OPEN_ASSISTANT_MENU_BUTTON)
        element = None
        for locator in buttons_locators:
            try:
                element = self.fast_find(locator)
            except exceptions.ElementNotFound:
                pass
        if element is not None:
            element.click()
        else:
            raise exceptions.ElementNotFound(
                f'Neither "{buttons_locators[0][1]}" (type: {buttons_locators[0][0]}) '
                f'nor "{buttons_locators[1][1]}" (type: {buttons_locators[1][0]}) elements were found')
        settings_page = SettingsPage(self.driver)
        settings_page.custom_wait(settings_page.is_opened)
        self.logger.info("Settings page is open")
        return settings_page

    @allure.step('Clicking on suggest with text "{suggest_text}"')
    def click_on_suggest(self, suggest_text):
        """Clicking on suggest with given text. If necessary, a swipe will be made to element to be clicked"""
        suggest_locator = self.locators.SUGGEST_TEXT_ITEM_WITH_TEXT__BASE
        suggest_locator = (suggest_locator[0], suggest_locator[1].format(text=suggest_text))
        self.logger.info(f'Swiping and clicking on suggest found by locator "{suggest_locator[1]}" (type: {suggest_locator[0]})')
        suggest_elem = self.swipe_to_element(
            locator=suggest_locator, direction=self.SwipeTo.LEFT,
            swipe_over_element_locator=self.locators.SUGGEST_LIST, swipe_length=0.3)
        suggest_elem.click()
        self.logger.info(f'The element with text "{suggest_text}" has been clicked')

