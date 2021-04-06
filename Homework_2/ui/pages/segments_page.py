import allure

from ui.pages.base_page_auth import BasePageAuth
from ui.locators import pages_locators

import settings


class NewSegment:
    URL = settings.Url.SEGMENT_CREATING

    def __init__(self, page):
        self.segments_page = page
        self.SEGMENT_TYPES = {
            "A&G in SN": self.segments_page.locators.SEGMENT_CREATING_FORM_AG_IN_SN,
        }
        self.name = None

    class TYPES:
        APPS = "A&G in SN"

    def _open_form(self):
        create_segment_btns = (self.segments_page.locators.CREATE_SEGMENT_BUTTON,
                               self.segments_page.locators.CREATE_SEGMENT_INSTRUCTION_LINK)
        for locator in create_segment_btns:
            if self.segments_page.check.is_visible(locator, raise_exception=False):
                self.segments_page.click(locator)
                return self
        raise self.segments_page.NewSegmentCreatingException(
            f"Failed to open form to create a new segment: {create_segment_btns[0][1]} "
            f"(type: {create_segment_btns[0][0]}) or {create_segment_btns[1][1]} (type: {create_segment_btns[1][0]})")

    def select_segment_type(self, segment_type):
        type_locator = self.SEGMENT_TYPES[segment_type]
        self.segments_page.click(type_locator)
        checkbox_locator = self.segments_page.locators.SEGMENT_CREATING_FORM_AG_IN_SN_CHECKBOX
        self.segments_page.click(checkbox_locator)

    def _submit_adding_segment(self):
        adding_submit_btn_locator = self.segments_page.locators.SEGMENT_CREATING_FORM_ADDING_SUBMIT_BUTTON
        elem = self.segments_page.find(adding_submit_btn_locator)
        if elem.get_attribute("disabled"):
            self.segments_page.NewSegmentSavingException(
                f"Adding segment submit button disabled: {adding_submit_btn_locator[1]} (type: {adding_submit_btn_locator[0]})")
        elem.click()

    def _set_segment_name(self, name):
        self.segments_page.fill_field(self.segments_page.locators.SEGMENT_CREATING_FORM_NAME_INPUT, name)

    def _save(self):
        self._submit_adding_segment()

        if self.name:
            self._set_segment_name(self.name)

        saving_submit_btn_locator = self.segments_page.locators.SEGMENT_CREATING_FORM_CREATING_SUBMIT_BUTTON
        elem = self.segments_page.find(saving_submit_btn_locator)
        if elem.get_attribute("disabled"):
            self.segments_page.NewSegmentSavingException(
                f"Saving segment submit button disabled: {saving_submit_btn_locator[1]} (type: {saving_submit_btn_locator[0]})")
        elem.click()

        self.segments_page.custom_wait(self.segments_page.check.is_page_opened, url=self.segments_page.URL)

    def __enter__(self):
        return self._open_form()

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        self._save()


class Segment:
    def __init__(self, table, id):
        self.table = table
        self.id = id

        name_locator = self.table.segments_page.locators.TABLE_CELL_NAME_BY_ID
        self.new_segm_name_locator = (name_locator[0], name_locator[1].format(item_id=self.id))
        name = self.table.segments_page.driver.find_element(*self.new_segm_name_locator).text
        self.name = name

        rm_btn_locator = self.table.segments_page.locators.TABLE_CELL_REMOVE_BUTTON_BY_ID
        self.REMOVE_BTN_LOCATOR = (rm_btn_locator[0], rm_btn_locator[1].format(item_id=id))

    def remove(self):
        self.table.segments_page.click(self.REMOVE_BTN_LOCATOR)
        confirm_remove_btn = self.table.segments_page.locators.SEGMENT_CONFIRM_REMOVE_BUTTON
        self.table.segments_page.click(confirm_remove_btn)
        self.table.segments_page.custom_wait(self.table.segments_page.check.is_not_visible,
                                             locator=confirm_remove_btn)
        self.table.segments_page.custom_wait(self.table.segments_page.check.is_not_visible,
                                             locator=self.new_segm_name_locator)

    def __eq__(self, other):
        other = str(other)
        if other.isdigit():
            return self.id == other
        return self.name == other

    def __repr__(self):
        return "Segment object. Id: {id}; Name: {name}".format(id=self.id, name=self.name)


class SegmentsTable:
    def __init__(self, segments_page):
        self.segments_page = segments_page

    def get_segments(self):
        return [Segment(self, n.text) for n in self.segments_page.find_elements(
            self.segments_page.locators.TABLE_CELL_ID)]


class SegmentsPage(BasePageAuth):
    URL = settings.Url.SEGMENTS
    locators = pages_locators.Segments

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.new_segment = NewSegment(self)
        self.segments_table = SegmentsTable(self)

    class NewSegmentCreatingException(Exception):
        pass

    class NewSegmentSavingException(Exception):
        pass

    def is_opened(self):
        spinner_locator = self.locators.PAGE_LOADING_SPINNER
        if self.check.is_not_exists(spinner_locator, raise_exception=False):
            return True
        raise self.check.PageNotOpenedException(f"Spinner exists: {spinner_locator[1]} (type: {spinner_locator[0]})")
