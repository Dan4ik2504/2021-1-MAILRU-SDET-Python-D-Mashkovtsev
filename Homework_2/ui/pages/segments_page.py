import allure

from ui.pages.base_page_auth import BasePageAuth
from ui.locators import pages_locators

import settings


class NewSegment:
    def __init__(self, page):
        self.page = page
        self.SEGMENT_TYPES = {
            "A&G in SN": self.page.locators.SEGMENT_CREATING_FORM_AG_IN_SN,
        }
        self.name = None

    class TYPES:
        APPS = "A&G in SN"

    def _open_form(self):
        create_segment_btns = (self.page.locators.CREATE_SEGMENT_BUTTON,
                               self.page.locators.CREATE_SEGMENT_INSTRUCTION_LINK)
        for locator in create_segment_btns:
            if self.page.is_element_exists(locator):
                self.page.click(locator)
                return self
        raise self.page.NewSegmentCreatingException(
            f"Failed to open form to create a new segment: {create_segment_btns[0][1]} "
            f"(type: {create_segment_btns[0][0]}) or {create_segment_btns[1][1]} (type: {create_segment_btns[1][0]})")

    def select_segment_type(self, segment_type):
        type_locator = self.SEGMENT_TYPES[segment_type]
        self.page.click(type_locator)
        checkbox_locator = self.page.locators.SEGMENT_CREATING_FORM_AG_IN_SN_CHECKBOX
        self.page.click(checkbox_locator)

    def _submit_adding_segment(self):
        adding_submit_btn_locator = self.page.locators.SEGMENT_CREATING_FORM_ADDING_SUBMIT_BUTTON
        elem = self.page.find(adding_submit_btn_locator)
        if elem.get_attribute("disabled"):
            self.page.NewSegmentSavingException(
                f"Adding segment submit button disabled: {adding_submit_btn_locator[1]} (type: {adding_submit_btn_locator[0]})")
        elem.click()

    def _set_segment_name(self, name):
        self.page.fill_field(self.page.locators.SEGMENT_CREATING_FORM_NAME_INPUT, name)

    def _save(self):
        self._submit_adding_segment()

        if self.name:
            self._set_segment_name(self.name)

        saving_submit_btn_locator = self.page.locators.SEGMENT_CREATING_FORM_CREATING_SUBMIT_BUTTON
        elem = self.page.find(saving_submit_btn_locator)
        if elem.get_attribute("disabled"):
            self.page.NewSegmentSavingException(
                f"Saving segment submit button disabled: {saving_submit_btn_locator[1]} (type: {saving_submit_btn_locator[0]})")
        elem.click()

        self.page.wait_until_load(url=self.page.URL)

    def __enter__(self):
        return self._open_form()

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        self._save()


class SegmentsPage(BasePageAuth):
    URL = settings.Url.SEGMENTS
    locators = pages_locators.Segments

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.new_segment = NewSegment(self)

    class NewSegmentCreatingException(Exception):
        pass

    class NewSegmentSavingException(Exception):
        pass

    def is_loaded(self):
        spinner_locator = self.locators.PAGE_LOADING_SPINNER
        if super().is_loaded():
            if not self.is_element_exists(spinner_locator):
                return True
        raise self.PageIsNotLoadedException(f"Spinner exists: {spinner_locator[1]} (type: {spinner_locator[0]})")

    def get_all_segments(self):
        segments = [n.text for n in self.driver.find_elements(*self.locators.TABLE_SEGMENT_NAME)]
        return segments
