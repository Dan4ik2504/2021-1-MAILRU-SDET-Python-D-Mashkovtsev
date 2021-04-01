from selenium.webdriver.common.by import By

import settings


class MainPageNoAuth:
    LOGIN_BUTTON = (By.CSS_SELECTOR, "[class^='responseHead-module-button-']")
    LOGIN_CONFIRM_BUTTON = (By.CSS_SELECTOR, "[class^='authForm-module-button-']")
    AUTH_FORM = (By.CSS_SELECTOR, "[class^='authForm-module-wrap-']")
    EMAIL_FIELD = (By.NAME, "email")
    PASSWORD_FIELD = (By.NAME, "password")
    FORM_ERROR = (By.XPATH, "//div[contains(@class, 'notify-module-error-')]")


class LoginPage(MainPageNoAuth):
    LOGIN_MSG_TITLE = (By.CSS_SELECTOR, "div[class='formMsg_title']")
    LOGIN_MSG_TEXT = (By.CSS_SELECTOR, "div[class='formMsg_text']")


class BasePageAuth:
    HEADER_USERNAME = (By.CSS_SELECTOR, "[class^='right-module-userNameWrap-']")
    HEADER_USER_MENU = (By.CSS_SELECTOR, "[class^='rightMenu-module-rightMenu-'")
    HEADER_USER_MENU_BUTTON = (By.CSS_SELECTOR, "[class^='right-module-rightButton-']")
    HEADER_USER_MENU_LOGOUT_BUTTON = (By.XPATH, "//li/a[contains(@class, 'rightMenu-module-rightMenuLink') and \
    contains(@href, '/logout')]")

    class NavPanel:
        _BASE_XPATH = "//a[contains(@class, 'center-module-button-') and contains(@href, '{}')]"
        DASHBOARD = (By.XPATH, _BASE_XPATH.format("/" + settings.Url._PATHS["dashboard"]))
        SEGMENTS = (By.XPATH, _BASE_XPATH.format("/" + settings.Url._PATHS["segments"]))
        BILLING = (By.XPATH, _BASE_XPATH.format("/" + settings.Url._PATHS["billing"]))
        STATISTICS = (By.XPATH, _BASE_XPATH.format("/" + settings.Url._PATHS["statistics"]))
        PRO = (By.XPATH, _BASE_XPATH.format("/" + settings.Url._PATHS["pro"]))
        PROFILE = (By.XPATH, _BASE_XPATH.format("/" + settings.Url._PATHS["profile"]))
        TOOLS = (By.XPATH, _BASE_XPATH.format("/" + settings.Url._PATHS["tools"]))
        HELP = (By.XPATH, _BASE_XPATH.format("/" + settings.Url._PATHS["help"]))