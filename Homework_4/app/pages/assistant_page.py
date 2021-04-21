import dataclasses

import allure
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

import exceptions
from app.pages.base_page import BasePage
from app.pages.settings_page import SettingsPage
from app.locators.assistant_page import AssistantPageLocators


class AssistantPage(BasePage):
    locators = AssistantPageLocators

    class MESSAGE_SENDER:
        USER = "User"
        ASSISTANT = "Assistant"

    class DialogItems:
        @dataclasses.dataclass
        class DialogMessage:
            sender: str
            text: str

        @dataclasses.dataclass
        class DialogFactCard:
            sender: str
            title: str
            text: str

        @dataclasses.dataclass
        class DialogPlayer:
            sender: str
            track_name: str

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

    @allure.step("Getting visible suggestions")
    def get_visible_suggestions_elements(self):
        elements = self.find_elements(self.locators.SUGGEST_TEXT_ITEM)
        self.logger.info(f'Got {len(elements)} suggestions')
        self.logger.debug(f'Suggestions: {"; ".join([str(elem.text) for elem in elements if elem.text is not None])}')
        return elements

    @allure.step("Getting visible simple dialog items")
    def get_visible_simple_dialog_items_text(self):
        elements = self.find_elements(self.locators.DIALOG_ITEM)
        items_text = []
        for element in elements:
            items_text.append(element.text)
        self.logger.info(f'Got {len(items_text)} items')
        self.logger.debug(f'Items: {"; ".join(items_text)}')
        return items_text

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
                card_obj = self.DialogItems.DialogFactCard(title=title, text=text)
                cards_objects.append(card_obj)
        self.logger.info(f'Got {len(cards_objects)} fact cards')
        self.logger.debug(f'Fact cards: '
                          f'{"; ".join(["{}: {}".format(card.title, card.text[:100]) for card in cards_objects])}')
        return cards_objects

    def get_visible_dialog_elements(self):
        """Returns list of visible dialog elements"""
        return self.find_elements(self.locators.DIALOG_ITEMS)

    @allure.step("Getting visible dialog items objects")
    def get_visible_dialog_objects(self):
        """Returns list of visible dialog items as instances of
        DialogMessage, DialogFactCard and DialogPlayer classes."""
        self.logger.info("Getting visible dialog items objects")
        text_element_class = self.locators.DIALOG_ITEM_TEXT_VIEW_CLASS_BASE
        text_element_id = self.locators.DIALOG_ITEM[1]
        fact_element_class = self.locators.DIALOG_ITEM_LINEAR_LAYOUT_CLASS_BASE
        fact_element_id = self.locators.DIALOG_FACT_CARD[1]
        frame_layout_element_class = self.locators.DIALOG_ITEM_FRAME_LAYOUT_CLASS_BASE
        view_group_element_class = self.locators.DIALOG_ITEM_VIEW_GROUP_CLASS_BASE

        dialog_elements = self.get_visible_dialog_elements()

        self.logger.info(f'Got {len(dialog_elements)} dialog elements')

        dialog_objects = []
        for element in dialog_elements:
            try:
                elem_class = element.get_attribute('class')

                # If the element is a simple text element sent by the assistant
                if elem_class == text_element_class and element.get_attribute('resource-id') == text_element_id:
                    elem_text = self.get_element_text_or_none(element)
                    message_obj = self.DialogItems.DialogMessage(text=elem_text, sender=self.MESSAGE_SENDER.ASSISTANT)
                    dialog_objects.append(message_obj)
                    self.logger.debug(f'Dialog text item object created. '
                                      f'Text: "{elem_text}". Sender: "{self.MESSAGE_SENDER.ASSISTANT}"')

                elif elem_class == frame_layout_element_class:
                    elem_child = element.find_element(*self.locators.ELEMENT_FIRST_CHILD)
                    elem_child_class = elem_child.get_attribute('class')

                    # If the element is a simple text element sent by the user
                    if elem_child_class == text_element_class \
                            and elem_child.get_attribute('resource-id') == text_element_id:
                        elem_text = self.get_element_text_or_none(elem_child)
                        message_obj = self.DialogItems.DialogMessage(text=elem_text, sender=self.MESSAGE_SENDER.USER)
                        dialog_objects.append(message_obj)
                        self.logger.debug(f'Dialog text item object created. '
                                          f'Text: "{elem_text}". Sender: "{self.MESSAGE_SENDER.USER}"')

                    # If the element is a fact element sent by assistant
                    elif elem_child_class == fact_element_class \
                            and elem_child.get_attribute('resource-id') == fact_element_id:
                        title = self.get_element_text_or_none(
                            elem_child.find_element(*self.locators.DIALOG_FACT_CARD_TITLE))
                        text = self.get_element_text_or_none(
                            elem_child.find_element(*self.locators.DIALOG_FACT_CARD_TEXT))

                        fact_obj = self.DialogItems.DialogFactCard(title=title, text=text,
                                                                   sender=self.MESSAGE_SENDER.ASSISTANT)
                        dialog_objects.append(fact_obj)
                        self.logger.debug(f'Dialog fact item object created. '
                                          f'Title: "{title}". Text: "{text}". '
                                          f'Sender: "{self.MESSAGE_SENDER.ASSISTANT}"')

                    # If the element is a player element sent by the assistant
                    elif elem_child_class == view_group_element_class:
                        player_track_name = self.get_element_text_or_none(
                            elem_child.find_element(*self.locators.PLAYER_TRACK_NAME))

                        player_obj = self.DialogItems.DialogPlayer(track_name=player_track_name,
                                                                   sender=self.MESSAGE_SENDER.ASSISTANT)
                        dialog_objects.append(player_obj)
                        self.logger.debug(f'Dialog player item object created. '
                                          f'Track name: "{player_track_name}". '
                                          f'Sender: "{self.MESSAGE_SENDER.ASSISTANT}"')

            except (StaleElementReferenceException, NoSuchElementException):
                continue

        self.logger.info(f'Created {len(dialog_objects)} dialog item objects')

        return dialog_objects

    def get_visible_dialog_elements_count(self):
        """Returns the number of visible elements"""
        return len(self.get_visible_dialog_elements())

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
        self.logger.info(
            f'Swiping and clicking on suggest found by locator "{suggest_locator[1]}" (type: {suggest_locator[0]})')
        suggest_elem = self.swipe_to_element(
            locator=suggest_locator, direction=self.SwipeTo.LEFT,
            swipe_over_element_locator=self.locators.SUGGEST_LIST, swipe_length=0.3)
        suggest_elem.click()
        self.logger.info(f'The element with text "{suggest_text}" has been clicked')
