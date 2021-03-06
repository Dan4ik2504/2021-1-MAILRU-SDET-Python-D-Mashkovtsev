import allure

from ui.pages.base_page_auth import BasePageAuth
from ui.locators import pages_locators

import settings


class NewSegment:
    """Object of the form for creating a new segment"""
    URL = settings.Url.SEGMENT_CREATING

    def __init__(self, page):
        self.segments_page = page
        self.SEGMENT_TYPES = {
            "A&G in SN": self.segments_page.locators.SEGMENT_CREATING_FORM_AG_IN_SN,
        }
        self.name = None

    class TYPES:
        APPS = "A&G in SN"

    @allure.step("Opening the form for creating a new segment")
    def _open_form(self):
        create_segment_btns = (self.segments_page.locators.CREATE_SEGMENT_BUTTON,
                               self.segments_page.locators.CREATE_SEGMENT_INSTRUCTION_LINK)

        for locator in create_segment_btns:
            try:
                elem = self.segments_page.fast_find(locator)
            except self.segments_page.FastFindingException:
                pass
            else:
                if self.segments_page.check.is_element_visible(elem, raise_exception=False):
                    self.segments_page.click(locator)
                    self.segments_page.logger.info('Form for creating a new segment opened')
                    return self

        raise self.segments_page.NewSegmentCreatingException(
            f"Failed to open form to create a new segment: {create_segment_btns[0][1]} "
            f"(type: {create_segment_btns[0][0]}) or {create_segment_btns[1][1]} (type: {create_segment_btns[1][0]})")

    @allure.step('Segment type and source selecting')
    def select_segment_type(self, segment_type):
        log_msg = f'Segment type selecting: {segment_type}'
        with allure.step(log_msg):
            self.segments_page.logger.info('Segment type selecting')
            type_locator = self.SEGMENT_TYPES[segment_type]
            self.segments_page.logger.debug(
                f'Segment type button locator: "{type_locator[0]}" (type: {type_locator[1]})')
            self.segments_page.click(type_locator)
            self.segments_page.logger.info(f'Segment type selected: {segment_type}')

        log_msg = 'Segment source selecting'
        with allure.step(log_msg):
            self.segments_page.logger.info(log_msg)
            checkbox_locator = self.segments_page.locators.SEGMENT_CREATING_FORM_AG_IN_SN_CHECKBOX
            self.segments_page.logger.debug(
                f'Segment source checkbox locator: "{checkbox_locator[0]}" (type: {checkbox_locator[1]})')
            self.segments_page.click(checkbox_locator)
            self.segments_page.logger.info(f'Segment source selected')

    @allure.step('Segment addition confirmation')
    def _submit_adding_segment(self):
        self.segments_page.logger.info('Segment addition confirmation')
        adding_submit_btn_locator = self.segments_page.locators.SEGMENT_CREATING_FORM_ADDING_SUBMIT_BUTTON
        elem = self.segments_page.find(adding_submit_btn_locator)
        self.segments_page.logger.debug(f'Segment addition confirmation button located: "{elem.tag_name}"')
        if elem.get_attribute("disabled"):
            self.segments_page.NewSegmentSavingException(
                f"Adding segment submit button disabled: {adding_submit_btn_locator[1]} "
                f"(type: {adding_submit_btn_locator[0]})")
        
        elem.click()
        self.segments_page.logger.info('Segment addition confirmed')

    @allure.step('Setting segment name: "{name}"')
    def _set_segment_name(self, name):
        self.segments_page.fill_field(self.segments_page.locators.SEGMENT_CREATING_FORM_NAME_INPUT, name)

    @allure.step("New segment saving")
    def _save(self):
        self._submit_adding_segment()

        if self.name:
            self._set_segment_name(self.name)

        log_msg = 'Clicking on segment saving button'
        with allure.step(log_msg):
            self.segments_page.logger.info(log_msg)
            saving_submit_btn_locator = self.segments_page.locators.SEGMENT_CREATING_FORM_CREATING_SUBMIT_BUTTON
            elem = self.segments_page.find(saving_submit_btn_locator)
            if elem.get_attribute("disabled"):
                self.segments_page.NewSegmentSavingException(
                    f"Saving segment submit button disabled: {saving_submit_btn_locator[1]} "
                    f"(type: {saving_submit_btn_locator[0]})")
            elem.click()

        with allure.step('Opening segments page'):
            self.segments_page.custom_wait(self.segments_page.check.is_page_opened, url=self.segments_page.URL)

    def __enter__(self):
        return self._open_form()

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return False
        self._save()


class Segment:
    """Segment object generated by segments table object"""
    def __init__(self, table, segment_id):
        self.table = table
        self.segment_id = segment_id

        name_locator = self.table.segments_page.locators.Table.TABLE_CELL_NAME_BY_ID
        self.new_segm_name_locator = (name_locator[0], name_locator[1].format(item_id=self.segment_id))
        self.name = self.table.segments_page.find(self.new_segm_name_locator).text

        rm_btn_locator = self.table.segments_page.locators.Table.TABLE_CELL_REMOVE_BUTTON_BY_ID
        self.remove_btn_locator = (rm_btn_locator[0], rm_btn_locator[1].format(item_id=self.segment_id))
    
    @allure.step('Segment removing')
    def remove(self):
        log_msg = 'Clicking on the segment remove button'
        with allure.step(log_msg):
            self.table.segments_page.logger.info(log_msg)
            self.table.segments_page.click(self.remove_btn_locator)
            confirm_remove_btn = self.table.segments_page.locators.Table.TABLE_CELL_SEGMENT_CONFIRM_REMOVE_BUTTON
            self.table.segments_page.click(confirm_remove_btn)
            self.table.segments_page.logger.info('Segment remove button clicked')

        log_msg = 'Waiting for segment deletion'
        with allure.step(log_msg):
            self.table.segments_page.logger.info(log_msg)
            self.table.segments_page.custom_wait(self.table.segments_page.check.is_not_visible,
                                                 locator=confirm_remove_btn)
            self.table.segments_page.custom_wait(self.table.segments_page.check.is_not_visible,
                                                 locator=self.new_segm_name_locator)
            self.table.segments_page.logger.info('Segment removed')

    def __eq__(self, other):
        other = str(other)
        self.table.segments_page.logger.debug(
            f'Comparison of the name "{self.name}" or ID "{self.segment_id}" of the segment '
            f'with the given string: "{other}"')
        if other.isdigit():
            return self.segment_id == other
        return self.name == other

    def __str__(self):
        return f'{self.segment_id}-{self.name}'

    def __repr__(self):
        return "Segment object. Id: {id}. Name: {name}.".format(id=self.segment_id, name=self.name)


class SegmentsTable:
    """Object of the table displayed on the segments page"""
    def __init__(self, segments_page):
        self.segments_page = segments_page
    
    @allure.step("Searching for segments in the table")
    def get_segments(self):
        self.segments_page.logger.info('Searching for segments in the table')
        segments = [Segment(self, n.text) for n in self.segments_page.find_elements(
            self.segments_page.locators.Table.TABLE_CELL_ID)]
        self.segments_page.logger.info(f'Found {len(segments)} segments')
        self.segments_page.logger.debug(f'Found {len(segments)} segments: {"; ".join([str(s) for s in segments])}')
        return segments
        

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

    @allure.step('Checking that the segment page is open')
    def is_opened(self):
        self.logger.info('Checking that the segment page is open')
        spinner_locator = self.locators.PAGE_LOADING_SPINNER
        if self.check.is_not_exists(spinner_locator, raise_exception=False):
            self.logger.info(f'Segments page loaded')
            return True
        raise self.check.PageNotOpenedException(f"Spinner exists: {spinner_locator[1]} (type: {spinner_locator[0]})")
