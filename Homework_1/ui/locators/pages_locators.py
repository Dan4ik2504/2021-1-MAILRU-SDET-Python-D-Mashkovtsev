from selenium.webdriver.common.by import By


class MainPage:
    LOGIN_BUTTON = (By.CSS_SELECTOR, "[class^='responseHead-module-button-']")
    LOGIN_CONFIRM_BUTTON = (By.CSS_SELECTOR, "[class^='authForm-module-button-']")
    AUTH_FORM = (By.CSS_SELECTOR, "[class^='authForm-module-wrap-']")
    EMAIL_FIELD = (By.NAME, "email")
    PASSWORD_FIELD = (By.NAME, "password")


class Dashboard:
    HEADER_USERNAME = (By.CSS_SELECTOR, "[class^='right-module-userNameWrap-']")
    HEDAER_USER_MENU_BUTTON = (By.CSS_SELECTOR, "[class^='right-module-rightButton-']")
    HEAD_USER_MENU_LOGOUT_BUTTON = (By.XPATH, "//li/a[contains(@class, 'rightMenu-module-rightMenuLink') and contains(@href, '/logout')]")