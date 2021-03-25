from selenium.webdriver.common.by import By


class MainPageNoAuth:
    LOGIN_BUTTON = (By.CSS_SELECTOR, "[class^='responseHead-module-button-']")
    LOGIN_CONFIRM_BUTTON = (By.CSS_SELECTOR, "[class^='authForm-module-button-']")
    AUTH_FORM = (By.CSS_SELECTOR, "[class^='authForm-module-wrap-']")
    EMAIL_FIELD = (By.NAME, "email")
    PASSWORD_FIELD = (By.NAME, "password")


class BasePageAuth:
    HEADER_USERNAME = (By.CSS_SELECTOR, "[class^='right-module-userNameWrap-']")
    HEADER_USER_MENU_BUTTON = (By.CSS_SELECTOR, "[class^='right-module-rightButton-']")
    HEADER_USER_MENU_LOGOUT_BUTTON = (By.XPATH, "//li/a[contains(@class, 'rightMenu-module-rightMenuLink') and contains(@href, '/logout')]")

    class NavPanel:
        _BASE_XPATH = "//div/ul[contains(@class, 'center-module-buttonsWrap-')]/li/a[contains(@class, 'center-module-button-') and contains(@href, '{}')]"
        DASHBOARD = (By.XPATH, _BASE_XPATH.format("/dashboard"))
        SEGMENTS = (By.XPATH, _BASE_XPATH.format("/segments"))
        BILLING = (By.XPATH, _BASE_XPATH.format("/billing"))
        STATISTICS = (By.XPATH, _BASE_XPATH.format("/statistics"))
        PRO = (By.XPATH, _BASE_XPATH.format("/pro"))
        PROFILE = (By.XPATH, _BASE_XPATH.format("/profile"))
        TOOLS = (By.XPATH, _BASE_XPATH.format("/tools"))
        HELP = (By.XPATH, _BASE_XPATH.format("/help/advertisers/ru"))

class ProfilePage(BasePageAuth):
    _BASE_XPATH = "//div[@data-class-name='Contacts']/ul[@class='profile__list']/li/div[contains(@class, '{}')]/div/div/input[@type='text']"
    NAME_FIELD = (By.XPATH, _BASE_XPATH.format("js-contacts-field-name"))
    PHONE_FIELD = (By.XPATH, _BASE_XPATH.format("js-contacts-field-phone"))
    EMAIL_FIELD = (By.XPATH, "//div[@data-class-name='Contacts']/ul[@class='profile__list']/li/div[@class='js-additional-emails']/div/div/div/div/input[@type='text']")
    CONFIRM_CHANGES_BUTTON = (By.XPATH, "//button[@data-class-name='Submit']")
    SUCCESS_VIEW = (By.XPATH, "//div[@data-class-name='SuccessView']")