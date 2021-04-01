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


class Dashboard(BasePageAuth):
    PAGE_LOADING_SPINNER = (By.XPATH, "//*[contains(@class, 'spinner')]")
    CREATE_CAMPAIGN_BUTTON = (By.XPATH,
                              "//div[contains(@class, 'button-module-textWrapper-') and text() = 'Создать кампанию']")
    CAMPAIGN_NAME = (By.XPATH, "//div[@data-entity-type='campaign' and contains(@class, "
                               "'nameCell-module-campaignNameCell-')]/a[contains(@class, "
                               "'nameCell-module-campaignNameLink')]")



class NewCampaign(BasePageAuth):
    BUTTON_GOAL_TRAFFIC = (By.CSS_SELECTOR, "div[class*='_traffic']")
    INPUT_URL = (By.CSS_SELECTOR, "input[class*='mainUrl-module-searchInput-Su-Rad']")
    INPUT_CAMPAIGN_NAME = (By.XPATH, "//div[contains(@class, 'input_campaign-name')]//input")
    PAGE_LOADING_SPINNER = (By.CSS_SELECTOR, "[class*='spinner']")
    _SETTING_WRAPPER_BASE_XPATH = "//li[@data-setting-name='{data}']"
    _SETTING_WRAPPER_BUTTON = _SETTING_WRAPPER_BASE_XPATH + "//div[contains(@data-scroll-name, 'setting-')]"
    _SEX_CHECKBOX_XPATH = _SETTING_WRAPPER_BASE_XPATH + "//input[@type='checkbox' and @value='{value}']"
    SEX_WRAPPER_BUTTON = (By.XPATH, _SETTING_WRAPPER_BASE_XPATH.format(data='sex'))
    SEX_CHECKBOX_MALE = (By.XPATH, _SEX_CHECKBOX_XPATH.format(data='sex', value="male"))
    SEX_CHECKBOX_FEMALE = (By.XPATH, _SEX_CHECKBOX_XPATH.format(data='sex', value="female"))
    DATE_WRAPPER_BUTTON = (By.XPATH, _SETTING_WRAPPER_BUTTON.format(data="date"))
    DATE_FROM_INPUT = (By.XPATH, _SETTING_WRAPPER_BASE_XPATH.format(data='date') +
                       "//div[contains(@class, 'date-setting__date-from')]/input")
    DATE_TO_INPUT = (By.XPATH, _SETTING_WRAPPER_BASE_XPATH.format(data='date') +
                     "//div[contains(@class, 'date-setting__date-to')]/input")
    BUDGET_WRAPPER_BUTTON = (By.XPATH, _SETTING_WRAPPER_BUTTON.format(data='budget_setting'))
    BUDGET_PER_DAY_INPUT = (By.XPATH, _SETTING_WRAPPER_BASE_XPATH.format(data='budget_setting') +
                            "//input[@data-test='budget-per_day']")
    BUDGET_TOTAL_INPUT = (By.XPATH, _SETTING_WRAPPER_BASE_XPATH.format(data='budget_setting') +
                          "//input[@data-test='budget-total']")
    _BANNER_FORMAT_ITEM_BUTTON_XPATH = "//div[contains(@class, 'bannerFormats-module-formatsWrap-')]/div/div[" \
                                       "contains(@class, 'banner-format-item')][span[" \
                                       "@class='banner-format-item__title' and text()='{banner_format}']]"
    MULTIFORMAT_BANNER_FORMAT_ITEM_BUTTON = (By.XPATH,
                                             _BANNER_FORMAT_ITEM_BUTTON_XPATH.format(banner_format='Мультиформат'))
    BANNER_IMAGE_INPUT = (By.XPATH, "//div[contains(@class, 'upload-module-wrapper')]/input[@type='file' and "
                                    "@data-test='image_1080x607']")
    BANNER_SMALL_IMAGE_INPUT = (By.XPATH, "//div[contains(@class, 'upload-module-wrapper')]/input[@type='file' and "
                                    "@data-test='image_600x600']")
    BANNER_ICON_INPUT = (By.XPATH, "//div[contains(@class, 'upload-module-wrapper')]/input[@type='file' and "
                                    "@data-test='icon_256x256']")
    BANNER_IMAGE_SAVING_SUBMIT_BUTTON = (
        By.XPATH, "//input[contains(@class, 'image-cropper__save') and @type='submit']")
    _BANNER_EDITOR_BASE_XPATH = "//div[contains(@class, 'bannerEditor-module-editorForm-')]"
    BANNER_TITLE_INPUT = (By.XPATH, _BANNER_EDITOR_BASE_XPATH + "//input[contains(@data-name, 'title_')]")
    BANNER_TEXT_INPUT = (By.XPATH, _BANNER_EDITOR_BASE_XPATH + "//textarea[contains(@data-name, 'text_')]")
    BANNER_ABOUT_COMPANY_INPUT = (By.XPATH, _BANNER_EDITOR_BASE_XPATH +
                                  "//textarea[contains(@data-name, 'about_company_')]")
    BANNER_NAME_INPUT = (By.XPATH, _BANNER_EDITOR_BASE_XPATH + "//input[contains(@data-name, 'banner-name')]")
    BANNER_SAVE_INPUT = (By.XPATH, "//div[contains(@class, 'bannerEditor-module-bottomControlsWrap-')]//div[contains(" \
                                   "@class, 'button-module-textWrapper-')]")
    SUBMIT_BUTTON = (By.XPATH, "//div[contains(@class, 'footer__button')]//button[@data-class-name='Submit']")
