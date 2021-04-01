import allure

from ui.pages.base_page_auth import BasePageAuth

import settings


class DashboardPage(BasePageAuth):
    URL = settings.Url.DASHBOARD
