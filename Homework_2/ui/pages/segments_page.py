import allure

from ui.pages.base_page_auth import BasePageAuth

import settings


class SegmentsPage(BasePageAuth):
    URL = settings.Url.SEGMENTS
