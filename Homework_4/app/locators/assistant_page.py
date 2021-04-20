from app.locators.base_page import BasePageLocators
from appium.webdriver.common.mobileby import MobileBy as By


class AssistantPageLocators(BasePageLocators):
    OPEN_KEYBOARD_BUTTON = (By.ID, "ru.mail.search.electroscope:id/keyboard")
    OPEN_ASSISTANT_MENU_BUTTON = (By.ID, "ru.mail.search.electroscope:id/assistant_menu_bottom")
    INPUT_TEXT_FIELD = (By.ID, "ru.mail.search.electroscope:id/input_text")
    SEND_TEXT_BUTTON = (By.ID, "ru.mail.search.electroscope:id/text_input_action")
    DIALOG_ITEM = (By.ID, "ru.mail.search.electroscope:id/dialog_item")
    DIALOG_FACT_CARD = (By.ID, "ru.mail.search.electroscope:id/item_dialog_fact_card_content_block")
    DIALOG_FACT_CARD_TITLE = (By.ID, "ru.mail.search.electroscope:id/item_dialog_fact_card_title")
    DIALOG_FACT_CARD_TEXT = (By.ID, "ru.mail.search.electroscope:id/item_dialog_fact_card_content_text")
    SUGGEST_LIST = (By.ID, "ru.mail.search.electroscope:id/suggests_list")
    SUGGEST_TEXT_ITEM = (By.ID, "ru.mail.search.electroscope:id/item_suggest_text")
    SUGGEST_TEXT_ITEM_WITH_TEXT_BASE = \
        (By.XPATH, "//*[@resource-id='ru.mail.search.electroscope:id/item_suggest_text' and @text='{text}']")
