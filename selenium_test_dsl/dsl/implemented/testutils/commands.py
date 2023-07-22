from ..utility.util import enumvalue
from enum import Enum


class Command(Enum):
    """
    Represents possible commands to be executed by the webdriver.
    """

    FIND_ELEMENT = enumvalue(reset=True)
    REFRESH_PAGE = enumvalue()
    TEXT_CLICK = enumvalue()
    TEXT_ASSERT_DISPLAYED = enumvalue()
    TEXT_ASSERT_CLICKABLE = enumvalue()
    TEXT_ASSERT_SELECTED = enumvalue()
    TEXT_ASSERT_ENABLED = enumvalue()
    CLEAR_INPUT = enumvalue()
    CLICK_ELEMENT = enumvalue()
    SCREENSHOT = enumvalue()
    SEND_KEYS_TO_ELEMENT = enumvalue()
    SLEEP = enumvalue()
    OPEN_PAGE = enumvalue()
    DROPDOWN_SELECT = enumvalue()
    FOR_EACH = enumvalue()
    EXECUTE_SCRIPT = enumvalue()
    SCROLL = enumvalue()
    TABLE_SELECT = enumvalue()

    ASSERT_DISPLAYED = enumvalue()
    ASSERT_CLICKABLE = enumvalue()
    ASSERT_ENABLED = enumvalue()
    ASSERT_EXISTS = enumvalue()
    ASSERT_SELECTED = enumvalue()
    ASSERT_PAGE_TITLE = enumvalue()
    ASSERT_TEXT_VALUE = enumvalue()
    ASSERT_COOKIE_EXISTS = enumvalue()
