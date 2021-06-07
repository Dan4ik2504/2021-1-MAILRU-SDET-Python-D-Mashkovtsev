from selenium.webdriver.common.by import By

USERNAME_FIELD = (By.ID, 'username')
EMAIL_FIELD = (By.ID, 'email')
PASSWORD_FIELD = (By.ID, 'password')
REPEAT_PASSWORD_FIELD = (By.ID, 'confirm')
SDET_CHECKBOX = (By.ID, 'term')
CONFIRM_BUTTON = (By.ID, 'submit')
ERROR_TEXT = (By.ID, 'flash')
LOGIN_PAGE_LINK = (By.CSS_SELECTOR, "form[action$='/reg'] a[href$='/login']")
