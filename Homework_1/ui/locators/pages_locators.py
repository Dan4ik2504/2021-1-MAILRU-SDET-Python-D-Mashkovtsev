from selenium.webdriver.common.by import By

import settings


class MainPageNoAuth:
    LOGIN_BUTTON = (By.CSS_SELECTOR, "[class^='responseHead-module-button-']")
    LOGIN_CONFIRM_BUTTON = (By.CSS_SELECTOR, "[class^='authForm-module-button-']")
    AUTH_FORM = (By.CSS_SELECTOR, "[class^='authForm-module-wrap-']")
    EMAIL_FIELD = (By.NAME, "email")
    PASSWORD_FIELD = (By.NAME, "password")


class BasePageAuth:
    HEADER_USERNAME = (By.CSS_SELECTOR, "[class^='right-module-userNameWrap-']")
    HEADER_USER_MENU = (By.CSS_SELECTOR, "[class^='rightMenu-module-rightMenu-'")
    HEADER_USER_MENU_BUTTON = (By.CSS_SELECTOR, "[class^='right-module-rightButton-']")
    HEADER_USER_MENU_LOGOUT_BUTTON = (By.XPATH, "//li/a[contains(@class, 'rightMenu-module-rightMenuLink') and \
    contains(@href, '/logout')]")
    INSTRUCTION_WRAPPER = (By.CSS_SELECTOR, "[class^='instruction-module-wrapper-']")

    class NavPanel:
        _BASE_XPATH = "//a[contains(@class, 'center-module-button-') and contains(@href, '{}')]"
        DASHBOARD = (By.XPATH, _BASE_XPATH.format("/" + settings.URL_PATHS["dashboard"]))
        SEGMENTS = (By.XPATH, _BASE_XPATH.format("/" + settings.URL_PATHS["segments"]))
        BILLING = (By.XPATH, _BASE_XPATH.format("/" + settings.URL_PATHS["billing"]))
        STATISTICS = (By.XPATH, _BASE_XPATH.format("/" + settings.URL_PATHS["statistics"]))
        PRO = (By.XPATH, _BASE_XPATH.format("/" + settings.URL_PATHS["pro"]))
        PROFILE = (By.XPATH, _BASE_XPATH.format("/" + settings.URL_PATHS["profile"]))
        TOOLS = (By.XPATH, _BASE_XPATH.format("/" + settings.URL_PATHS["tools"]))
        HELP = (By.XPATH, _BASE_XPATH.format("/" + settings.URL_PATHS["help"]))


class ProfilePage(BasePageAuth):
    _BASE_FORM_XPATH = "//div[contains(@class, '{}')]//input[@type='text']"
    NAME_FIELD = (By.XPATH, _BASE_FORM_XPATH.format("js-contacts-field-name"))
    PHONE_FIELD = (By.XPATH, _BASE_FORM_XPATH.format("js-contacts-field-phone"))
    EMAIL_FIELD = (By.XPATH, _BASE_FORM_XPATH.format("js-additional-emails"))
    CONFIRM_CHANGES_BUTTON = (By.XPATH, "//button[@data-class-name='Submit']")
    SUCCESS_VIEW = (By.XPATH, "//div[@data-class-name='SuccessView']")
