from selenium.webdriver.common.by import By

USERNAME_FIELD = (By.ID, 'username')
PASSWORD_FIELD = (By.ID, 'password')
CONFIRM_BUTTON = (By.ID, 'submit')
ERROR_TEXT = (By.ID, 'flash')
REGISTER_PAGE_LINK = (By.CSS_SELECTOR, "form[action$='/login'] a[href$='/reg']")
