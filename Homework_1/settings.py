# System settings
DRIVER_PATH = "/opt/WebDriver/bin/chromedriver"

# Basic settings
DEFAULT_TIMEOUT = 10
CLICK_RETRY = 3

# URLs
BASE_URL = "https://target.my.com/"
URL_PATHS = {
    "dashboard": "dashboard",
    "segments": "segments",
    "billing": "billing",
    "statistics": "statistics",
    "pro": "pro",
    "profile": "profile",
    "tools": "tools",
    "help": "help/advertisers/ru",
}
DASHBOARD_URL = BASE_URL + URL_PATHS["dashboard"]
SEGMENTS_URL = BASE_URL + URL_PATHS["segments"]
BILLING_URL = BASE_URL + URL_PATHS["billing"]
STATISTICS_URL = BASE_URL + URL_PATHS["statistics"]
PRO_URL = BASE_URL + URL_PATHS["pro"]
PROFILE_URL = BASE_URL + URL_PATHS["profile"]
TOOLS_URL = BASE_URL + URL_PATHS["tools"]
HELP_URL = BASE_URL + URL_PATHS["help"]

# User data
LOGIN = "tebivan222@bombaya.com"
PASSWORD = "Qwerty123456"
USERNAME = "Тестов Тест Тестович"
PHONE = "+70000000000"
EMAIL = "qwertyuiop@bombaya.com"
