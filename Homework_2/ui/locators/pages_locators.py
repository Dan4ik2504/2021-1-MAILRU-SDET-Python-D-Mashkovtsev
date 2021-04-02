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


class Segments(BasePageAuth):
    CREATE_SEGMENT_INSTRUCTION_LINK = (By.CSS_SELECTOR, "a[href*='/segments/segments_list/new/']")
    CREATE_SEGMENT_BUTTON = \
        (By.XPATH, "//div[contains(@class, 'segments-list__tbl-settings-wrap')]//button[@data-class-name='Submit']")
    PAGE_LOADING_SPINNER = (By.CSS_SELECTOR, "[class*='spinner']:not([style*='display: none;'])")
    SEGMENT_CREATING_FORM_ACTIVE_SEGMENTS = \
        (By.XPATH, "//div[contains(@class, 'adding-segments-item') and not(contains(@class, "
                   "'adding-segments-item_empty')) and not(text()='Список сегментов')]")
    SEGMENT_CREATING_FORM_AG_IN_SN = \
        (By.XPATH, "//div[contains(@class, 'adding-segments-item') and text()='Приложения и игры в соцсетях']")
    SEGMENT_CREATING_FORM_AG_IN_SN_CHECKBOX = \
        (By.XPATH, "//div[contains(@class, 'adding-segments-source__header') and (//following-sibling::div["
                   "@class='adding-segments-source__text-wrap']"
                   "//span[text()='Игравшие и платившие в платформе'])]//input[@type='checkbox']")
    SEGMENT_CREATING_FORM_ADDING_SUBMIT_BUTTON = \
        (By.XPATH, "//div[contains(@class, 'adding-segments-modal__btn-wrap')]//button[@data-class-name='Submit']")
    SEGMENT_CREATING_FORM_CREATING_SUBMIT_BUTTON = \
        (By.XPATH, "//div[contains(@class, 'create-segment-form__btn-wrap')]/button[@data-class-name='Submit']")
    SEGMENT_CREATING_FORM_NAME_INPUT = \
        (By.XPATH, "//div[contains(@class, 'input_create-segment-form')]//input[@type='text']")
    _TABLE_XPATH = "//div[contains(@class, 'main-module-Table-')]"
    _TABLE_CELL_BASE_XPATH = \
        _TABLE_XPATH + "//div[contains(@class, 'main-module-Cell-') and contains(@data-test, '{cell_name}')]"
    TABLE_CELL_ID = (By.XPATH, _TABLE_CELL_BASE_XPATH.format(cell_name="id") + "//span")
    TABLE_CELL_NAME = (By.XPATH, _TABLE_CELL_BASE_XPATH.format(cell_name="name") +
                       "/div[contains(@class, 'cells-module-nameCell')]/a")
    TABLE_CELL_REMOVE_BUTTON = (By.XPATH, _TABLE_CELL_BASE_XPATH.format(cell_name="remove") +
                       "/span[contains(@class, 'cells-module-removeCell')]")
    TABLE_CELL_NAME_BY_ID = (By.XPATH, _TABLE_CELL_BASE_XPATH.format(cell_name="name-{item_id}") +
                       "/div[contains(@class, 'cells-module-nameCell')]/a")
    TABLE_CELL_REMOVE_BUTTON_BY_ID = (By.XPATH, _TABLE_CELL_BASE_XPATH.format(cell_name="remove-{item_id}") +
                       "/span[contains(@class, 'cells-module-removeCell')]")
    SEGMENT_CONFIRM_REMOVE_BUTTON = (By.XPATH, "//button[contains(@class, 'button_confirm-remove')]")