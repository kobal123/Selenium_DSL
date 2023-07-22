from selenium.webdriver.ie.webdriver import WebDriver

from .commands import Command
import time
from enum import Enum
from io import StringIO
from selenium.common.exceptions import UnexpectedTagNameException, InvalidSelectorException, ScreenshotException, \
    JavascriptException
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from colorama import init, Fore
from selenium.webdriver.support.expected_conditions import *
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from dsl.implemented.testutils.argument import Argument
from .TestResult import TestResult
from .testcase import TestCase
from ..utility.util import color
from .custom_expected_conditions import stripped_text_to_be_present_in_element
from .custom_expected_conditions import stripped_text_to_be_present_in_value
from .custom_expected_conditions import table_cell_clickable
from .custom_expected_conditions import text_to_be_clickable
from .custom_expected_conditions import text_to_be_displayed
from .custom_expected_conditions import text_to_be_selected
from selenium.webdriver.common.by import By


class TestExecutor:
    """
    Class to execute the commands of a testcase.
    The execution depends on the implementation of this class.
    """

    def __init__(self, browser):
        self.ctx_pos = None
        self.browser = browser
        self.__testcase = None
        self.__OPS: dict = {
            Command.ASSERT_CLICKABLE: self._execute_ASSERT_CLICKABLE,
            Command.ASSERT_ENABLED: self._execute_ASSERT_ENABLED,
            Command.ASSERT_DISPLAYED: self._execute_ASSERT_VISIBLE,
            Command.ASSERT_EXISTS: self._execute_EXISTS,
            Command.ASSERT_SELECTED: self._execute_ASSERT_SELECTED,
            Command.ASSERT_TEXT_VALUE: self._execute_ASSERT_TEXT_VALUE,
            Command.ASSERT_PAGE_TITLE: self._execute_ASSERT_PAGE_TITLE,
            Command.SLEEP: self._execute_WAIT,
            Command.SEND_KEYS_TO_ELEMENT: self._execute_SEND_KEYS,
            Command.SCREENSHOT: self._execute_SCREENSHOT,
            Command.DROPDOWN_SELECT: self._execute_DROPDOWN_SELECT,
            Command.CLICK_ELEMENT: self._execute_CLICK_ELEMENT,
            Command.FIND_ELEMENT: self._execute_FIND_ELEMENT,
            Command.OPEN_PAGE: self._execute_OPEN_PAGE,
            Command.EXECUTE_SCRIPT: self._execute_EXECUTE_SCRIPT,
            Command.TABLE_SELECT: self._execute_TABLE_CLICK,
            Command.CLEAR_INPUT: self._execute_CLEAR_INPUT,
            Command.TEXT_ASSERT_DISPLAYED: self._execute_TEXT_ASSERT_DISPLAYED,
            Command.TEXT_CLICK: self._execute_TEXT_CLICK,
            Command.REFRESH_PAGE: self._execute_REFRESH_PAGE
        }


    def _execute_REFRESH_PAGE(self,arg: Argument):
        try:
            self.browser.refresh()
        except WebDriverException:
            self.fail_test_with_cause("""
            Error refreshing the page.
            """)


    def _execute_CLEAR_INPUT(self, arg: Argument):
        self.browser.find_element(by=arg.selector, value=arg.element_name).clear()

    def set_testcase(self, testcase: TestCase):
        self.__testcase = testcase

    def _execute_TABLE_CLICK(self, arg: Argument):
        cell = WebDriverWait(self.browser, 15).until(table_cell_clickable(arg.value, **arg.dictionary))
        cell.click()

    def _execute_SEND_KEYS(self, argument):
        """
        Types the value specified into the web element.

        Args:
            argument:

        """

        try:
            el = WebDriverWait(self.browser,
                               timeout=argument.timeout,
                               poll_frequency=0.1).until(
                element_to_be_clickable((argument.selector, argument.element_name))
            )
            if el:
                el.send_keys(argument.value)

        except WebDriverException as e:
            self.fail_test_with_cause(f"""
            Failed send keys to element.
            Check if window is not closed.
            {e}
            """)

    def _execute_SCREENSHOT(self, argument):
        try:
            self.browser.get_screenshot_as_file(argument.filename)
        except WebDriverException:
            self.fail_test_with_cause(f"""
            Failed take screenshot.
            Check if window is not closed.
            """)

    def _execute_CLICK_ELEMENT(self, arg: Argument):
        """
        Clicks a web element.

        Args:
            arg: An Argument object with the element name and selector specified
        """

        try:
            element = WebDriverWait(self.browser, arg.timeout, poll_frequency=0.25).until(
                element_to_be_clickable((arg.selector, arg.element_name))
            )
            element.click()
        except ElementClickInterceptedException:
            self.fail_test_with_cause(f"""
            Could not click element '{arg.element_name}' with selector {arg.selector}.
            A possible cause could be that the element is hidden behind another element. 
            """)
        except TimeoutException:
            self.fail_test_with_cause(f"""
            failed to click element '{arg.element_name}' with selector {arg.selector}
            within the time specified.
            """)


    def _execute_DROPDOWN_SELECT(self, arg):
        """
        Selects an element from a dropdown menu.

        Args:
            arg: Argument object with the dropdown list name ,selector and value specified.
        """

        element = self._execute_ASSERT_CLICKABLE(arg)
        try:
            if element:
                select = Select(element)
                select.select_by_visible_text(arg.value)
        except UnexpectedTagNameException:
            self.fail_test_with_cause(f"""
            The element {arg.element_name} with selector {arg.selector}
            was not a SELECT tag.
            """)


    def _execute_EXECUTE_SCRIPT(self, arg: Argument):
        """
        Executes the given javascript in the browser.
        Args:
            arg:
        """
        result = self.browser.execute_script(arg.dictionary['script'], *arg.value)
        # cell = WebDriverWait(self.browser,15).until(table_cell_clickable(False,"Link",**{"Serial Number":"F3FA33"}))
        # cell.click()

    def _execute_ASSERT_TEXT_VALUE(self, arg):
        """
        Checks if the text inside an element is equal to the given value.

        Args:
            arg: An Argument object with the text value, element name and selector specified.

        """
        try:
            if arg.by_value:
                WebDriverWait(self.browser, arg.timeout).until(
                    stripped_text_to_be_present_in_value((arg.selector, arg.element_name), arg.value)
                )
            else:
                WebDriverWait(self.browser, arg.timeout).until(
                    stripped_text_to_be_present_in_element((arg.selector, arg.element_name), arg.value)
                )
        except TimeoutException:
            self.fail_test_with_cause(f"""
            Failed to get the text of element {arg.element_name} with selector {arg.selector}
            within the time specified.
            Possible causes:
                    - Wrong element name
                    - Wrong selector
                    - The text is not present in the element.
            """)

    def _execute_ASSERT_PAGE_TITLE(self, arg):
        """
        Checks if the title of the current page is equal to
        the value specified.

        Args:
            arg: an Argument object with the page name specified as value.

        """
        try:
            WebDriverWait(self.browser, arg.timeout).until(
                title_is(arg.value)
            )
        except TimeoutException:
            self.fail_test_with_cause(f"""
            Page title assertion failed, title was not '{arg.value}', it was {self.browser.title}
            """)

    def _execute_FIND_ELEMENT(self, arg):
        """
        Tries to find an element in the time specified.

        Args:
            arg: an Argument object with the needed values specified.

        Returns:
            The web element if it was found, None otherwise.
        """
        try:
            return WebDriverWait(driver=self.browser, timeout=arg.timeout, poll_frequency=0.1) \
                .until(visibility_of_element_located((arg.selector, arg.element_name)))

        except NoSuchElementException:
            self.fail_test_with_cause(f"""
            No element '{arg.element_name}' was found with selector '{arg.selector}'.
            Try changing the name or the selector.
            """)
        except WebDriverException:
            self.fail_test_with_cause(f"""
            No element '{arg.element_name}' was found with selector '{arg.selector}'.
            Check if the window is closed during execution.
            """)

        return None

    def _execute_OPEN_PAGE(self, arg: Argument):
        """
        Opens the url specified.

        Args:
            arg: an Argument object with the URL specified as value.
        """
        try:
            self.browser.get(arg.value)
        except WebDriverException:
            self.fail_test_with_cause(f"""
            Failed to open page {arg.value}.
            Check the url or if the window is not closed during execution.
            """)

    def _execute_ASSERT_SELECTED(self, arg: Argument):
        """
        Checks if a web element is selected.

        Args:
            arg: an Argument object with the element name and selector specified.
        """

        try:
            if arg.negate:
                WebDriverWait(self.browser, arg.timeout).until_not(
                    element_located_to_be_selected((arg.selector, arg.element_name)))
            else:
                WebDriverWait(self.browser, arg.timeout).until(
                    element_located_to_be_selected((arg.selector, arg.element_name)))

        except TimeoutException:
            if arg.negate:
                self.fail_test_with_cause(f"""
                The element {arg.element_name} with selector {arg.selector}
                was selected.
                """)
            else:
                self.fail_test_with_cause(f"""
                The element {arg.element_name} with selector {arg.selector}
                was not selected.
                """)

    def _execute_ASSERT_CLICKABLE(self, arg: Argument):
        """
        Checks if a web element is clickable.

        Args:
            arg: an Argument object with the element name and selector specified.
        """
        try:
            if arg.negate:
                return WebDriverWait(self.browser, 1).until_not(
                    element_to_be_clickable((arg.selector, arg.element_name)))
            else:
                return WebDriverWait(self.browser, 1).until(
                    element_to_be_clickable((arg.selector, arg.element_name)))

        except TimeoutException:
            if arg.negate:
                self.fail_test_with_cause(f"""
                The element {arg.element_name} with selector {arg.selector}
                was clickable.
                """)
            else:
                self.fail_test_with_cause(f"""
                The element {arg.element_name} with selector {arg.selector}
                was not clickable.
                """)
            return None
        except InvalidSelectorException:
            pass

    def _execute_ASSERT_ENABLED(self, arg: Argument):
        """
        Checks if a web element is enabled.

        Args:
            arg: an Argument object with the element name and selector specified.
        """
        # TODO: write a good expected condition.
        WebDriverWait(self.browser, arg.timeout).until(
            text_to_be_present_in_element((arg.selector, arg.element_name), arg.value)
        )

        if False:
            self.fail_test_with_cause(f"""
            The element {arg.element_name} with selector {arg.selector}
            was not enabled.
            """)

    def fail_test_with_cause(self, cause: str):
        """
        Fails the current test with the given cause

        Args:
            cause: the reason the test failed
        """

        self.__testcase.result = TestResult.FAIL
        self.__testcase.cause = cause
        try:
            self.browser.get_screenshot_as_file('error.png')
        except ScreenshotException:
            print("Failed to take screenshot of the error.")

    def _execute_ASSERT_VISIBLE(self, arg: Argument):
        """
        Checks if a web element is visible.

        Args:
            arg: an Argument object with the element name and selector specified.
        """
        try:
            if arg.negate:
                WebDriverWait(self.browser, arg.timeout).until_not(
                    visibility_of_element_located((arg.selector, arg.element_name))
                )
            else:
                WebDriverWait(self.browser, arg.timeout).until(
                    visibility_of_element_located((arg.selector, arg.element_name)))

        except TimeoutException:
            if arg.negate:
                self.fail_test_with_cause(f"""
                The element {arg.element_name} with selector {arg.selector}
                is displayed.
                """)
            else:
                self.fail_test_with_cause(f"""
                The element {arg.element_name} with selector {arg.selector}
                is not displayed.
                """)

    def _execute_EXISTS(self, arg: Argument):
        """
        Checks if a web element exists on the page.
        Args:
            arg: an Argument object with the element name and selector specified.
        """
        try:
            # self.browser.find_element(value=arg.element_name, by=arg.selector)
            if arg.negate:
                WebDriverWait(self.browser, arg.timeout).until(
                    presence_of_element_located((arg.selector, arg.element_name))
                )
            else:
                WebDriverWait(self.browser, arg.timeout).until_not(
                    presence_of_element_located((arg.selector, arg.element_name))
                )
        except TimeoutException:
            if arg.negate:
                self.fail_test_with_cause(f"""
                The element {arg.element_name} with selector {arg.selector}
                does exist.
                """)
            else:
                self.fail_test_with_cause(f"""
                The element {arg.element_name} with selector {arg.selector}
                does not exist.
                """)

    def _execute_WAIT(self, arg: Argument):
        """
        Stops the program execution for the given amount of seconds

        Args:
            arg: an Argument object with the time specified in seconds as value.

        """
        time.sleep(arg.value)

    def _execute_TEXT_ASSERT_DISPLAYED(self, arg):

        WebDriverWait(self.browser, timeout=arg.timeout).until(
            text_to_be_displayed(arg.value)
        )

    def _execute_TEXT_ASSERT_CLICKABLE(self, arg):
        pass

    def _execute_TEXT_ASSERT_SELECTED(self, arg):
        pass

    def _execute_TEXT_CLICK(self, arg: Argument):
        element = WebDriverWait(self.browser, timeout=arg.timeout).until(
            text_to_be_clickable(arg.value)
        )

        element.click()

    def execute(self):
        """
        Executes the commands of the current testcase.
        """

        for op in self.__testcase.commands:
            print(f"crrent handle:{self.browser.current_window_handle}")
            print(f"curent_url : {self.browser.current_url}")
            if self.__testcase.result is TestResult.FAIL:
                break
            command = op[0]
            inputs:Argument = op[1]
            self.ctx_pos = op[2]
            fun = self.__OPS.get(command)
            if fun is None:
                raise RuntimeError(f"Command not implemented: {command}")
            try:
                fun(inputs)
            except InvalidSelectorException:
                self.fail_test_with_cause(f"Invalid selector {inputs.selector}")

        self.generate_report()

    def generate_report(self):
        """
        Prints the results of the testcase.
        """
        with StringIO() as buffer:
            buffer.write(str(self.__testcase.name))
            buffer.write(": ")
            result = self.__testcase.result
            result = color(Fore.RED, result) if result is TestResult.FAIL else color(Fore.GREEN, result)
            buffer.write(result)

            if self.__testcase.result is TestResult.FAIL:
                buffer.write(str(self.__testcase.cause))
                buffer.write(f"Error at line {self.ctx_pos[0]}, column {self.ctx_pos[1]}")
            print(buffer.getvalue())
