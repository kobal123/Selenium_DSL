import time
from enum import Enum
from io import StringIO
from selenium.common.exceptions import NoSuchElementException, UnexpectedTagNameException
from selenium.common.exceptions import ElementClickInterceptedException, WebDriverException, TimeoutException
from selenium.webdriver.support.expected_conditions import *
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from colorama import init, Fore
init()

enumval = 0

def auto_str(cls):
    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )
    cls.__str__ = __str__
    return cls


def enumvalue(reset=False):
    global enumval
    if reset:
        enumval = -1
    enumval += 1
    return enumval


def header(txt: str, width=45, filler='-', align='c'):
    assert align in 'lcr'
    return {'l': txt.ljust, 'c': txt.center, 'r': txt.rjust}[align](width, filler)


def color(color, text):
    return f"{color}{str(text)}{Fore.RESET}"

@auto_str
class Argument:
    def __str__(self) -> str:
        return super().__str__()

    def __init__(self, element_name=None, selector=None, negate=False, filename=None, value=None, timeout=0):
        self.element_name = element_name
        self.selector = selector
        self.negate = negate
        self.filename = filename
        self.timeout = timeout
        self.value = value



class Command(Enum):
    FIND_ELEMENT = enumvalue()
    CLICK_ELEMENT = enumvalue()
    SCREENSHOT = enumvalue()
    SEND_KEYS_TO_ELEMENT = enumvalue()
    SLEEP = enumvalue()
    OPEN_PAGE = enumvalue()
    DROPDOWN_SELECT = enumvalue()
    ASSERT_DISPLAYED = enumvalue()
    ASSERT_CLICKABLE = enumvalue()
    ASSERT_ENABLED = enumvalue()
    ASSERT_EXISTS = enumvalue()
    ASSERT_SELECTED = enumvalue()
    ASSERT_PAGE_TITLE = enumvalue()
    ASSERT_TEXT_VALUE = enumvalue()


class TestCase:
    __test_case_num = 0

    def __init__(self, browser, name=""):

        if name == "":
            self.name = f"test case {TestCase.__test_case_num}"
            TestCase.__test_case_num += 1
        else:
            self.name = name
            TestCase.__test_case_num += 1
        self.result = TestResult.PASS
        self.browser = browser
        self.operations = []
        self.cause = None
        self.current_web_element = None
        self._current_web_element_name = None
        self._current_web_element_selector = None
        self._current_ctx_pos = None
        self._wait_condition = None
        self.__current_argument = None
        self.__OPS: dict = {
            Command.ASSERT_CLICKABLE: self._execute_ASSERT_CLICKABLE,
            Command.ASSERT_ENABLED:  self._execute_ASSERT_ENABLED,
            Command.ASSERT_DISPLAYED:  self._execute_ASSERT_VISIBLE,
            Command.ASSERT_EXISTS:  self._execute_EXISTS,
            Command.ASSERT_SELECTED:  self._execute_ASSERT_SELECTED,
            Command.ASSERT_TEXT_VALUE:  self._execute_ASSERT_TEXT_VALUE,
            Command.ASSERT_PAGE_TITLE:  self._execute_ASSERT_PAGE_TITLE,
            Command.SLEEP: self._execute_WAIT,
            Command.SEND_KEYS_TO_ELEMENT:  self._execute_SEND_KEYS,
            Command.SCREENSHOT:  self._execute_SCREENSHOT,
            Command.DROPDOWN_SELECT:  self._execute_DROPDOWN_SELECT,
            Command.CLICK_ELEMENT: self._execute_CLICK_ELEMENT,
            Command.FIND_ELEMENT:  self._execute_FIND_ELEMENT,
            Command.OPEN_PAGE: self._execute_OPEN_PAGE
        }

    def put_op(self, function, ctx_pos, args=None):
        self.operations.append(tuple([function, args, ctx_pos]))

    def _execute_SEND_KEYS(self, argument):
        try:
            el = WebDriverWait(self.browser,
                               timeout=argument.timeout,
                               poll_frequency=0.1).until(
                visibility_of_element_located((argument.selector, argument.element_name))
            )
            # print(f"FROM SNED_KEYS, EL is {el}")
            if el:
                el.send_keys(argument.value)
        except WebDriverException as e:
            self.set_fail_with_cause(f"""
            Failed send keys to element.
            Check if window is not closed.
            {e}
            """)

    def _execute_SCREENSHOT(self, argument):
        try:
            self.browser.get_screenshot_as_file(argument.filename)
        except WebDriverException:
            self.set_fail_with_cause(f"""
            Failed take screenshot.
            Check if window is not closed.
            """)

    def _execute_CLICK_ELEMENT(self, arg):
        # print("FROM CLICK")
        try:
            element = WebDriverWait(self.browser, arg.timeout, poll_frequency=0.25).until(
                element_to_be_clickable((arg.selector, arg.element_name)))

            element.click()

        except ElementClickInterceptedException:
            self.set_fail_with_cause(f"""
            Could not click element '{arg.element_name}' with selector {arg.selector}.
            A possible cause could be that the element is hidden behind another element. 
            """)
        except TimeoutException:
            self.set_fail_with_cause(f"""
            failed to click element '{arg.element_name}' with selector {arg.selector}
            within the time specified.
            """)

    def _execute_DROPDOWN_SELECT(self, arg):
        # check if the element is clickable.

        # if this fails, it returns None.
        #       if it failed, do nothing, not even setting an error message, just return.
        #       else let the select class do its magic
        #           if this fails, add error message and return

        element = self._execute_ASSERT_CLICKABLE(arg)
        print(f"FROM DROPDOWN, ELEMENT IS {element}")
        try:
            if element:
                select = Select(element)
                #select.select_by_value(arg.value)
                select.select_by_visible_text(arg.value)

            else:
                return
        except UnexpectedTagNameException:
            self.set_fail_with_cause(f"""
            The element {arg.element_name} with selector {arg.selector}
            was not a SELECT tag.
            """)

    def _execute_ASSERT_TEXT_VALUE(self,arg):
        try:
            element = WebDriverWait(self.browser, arg.timeout).until(
                text_to_be_present_in_element((arg.selector, arg.element_name),arg.value)
            )

        except TimeoutException:
            self.set_fail_with_cause(f"""
            Failed to get the text of element {arg.element_name} with selector {arg.selector}
            within the time specified.
            Possible causes:
                    - Wrong element name
                    - Wrong selector
                    - The text is not present in the element.
            """)

    def _execute_ASSERT_PAGE_TITLE(self,arg):

        try:
            element = WebDriverWait(self.browser, arg.timeout).until(
                title_is(arg.value)
            )
        except TimeoutException:
            self.set_fail_with_cause(f"""
            Page title assertion failed, title was not '{arg.value}', it was {self.browser.title}
            """)


    def _execute_FIND_ELEMENT(self, arg):
        """
        Tries to find an element in the time specified.
        If the maximum wait time is not specified in the Argument object, it is set to 0.
        Args:
            arg: an Argument object with the needed values specified.

        Returns:
            The Webelement if it was found, None otherwise.
        """
        try:
            return WebDriverWait(driver=self.browser, timeout=arg.timeout, poll_frequency=0.1) \
                .until(visibility_of_element_located((arg.selector, arg.element_name)))

        except NoSuchElementException:
            self.set_fail_with_cause(f"""
            No element '{arg.element_name}' was found with selector '{arg.selector}'.
            Try changing the name or the selector.
            """)
        except WebDriverException:
            self.set_fail_with_cause(f"""
            No element '{arg.element_name}' was found with selector '{arg.selector}'.
            Check if the window is closed during execution.
            """)

        return None

    def _execute_OPEN_PAGE(self, arg: Argument):
        """
        Opens the url specified.

        Args:
            arg: an Argument object with the needed values specified.

        """
        try:
            self.browser.get(arg.value)
        except WebDriverException:
            self.set_fail_with_cause(f"""
            Failed to open page {arg.value}.
            Check the url or if the window is not closed during execution.
            """)

    def _execute_ASSERT_SELECTED(self, arg):
        try:
            if arg.negate:
                WebDriverWait(self.browser, arg.timeout).until_not(
                    element_located_to_be_selected((arg.selector, arg.element_name)))
            else:
                WebDriverWait(self.browser, arg.timeout).until(
                    element_located_to_be_selected((arg.selector, arg.element_name)))

        except TimeoutException:
            if arg.negate:
                self.set_fail_with_cause(f"""
                The element {self._current_web_element_name} with selector {self._current_web_element_selector}
                was selected.
                """)
            else:
                self.set_fail_with_cause(f"""
                The element {self._current_web_element_name} with selector {self._current_web_element_selector}
                was not selected.
                """)

    def _execute_ASSERT_CLICKABLE(self, arg):
        try:
            if arg.negate:
                return WebDriverWait(self.browser, 1).until_not(
                    element_to_be_clickable((arg.selector, arg.element_name)))
            else:
                return WebDriverWait(self.browser, 1).until(
                    element_to_be_clickable((arg.selector, arg.element_name)))

        except TimeoutException:
            if arg.negate:
                self.set_fail_with_cause(f"""
                The element {self._current_web_element_name} with selector {self._current_web_element_selector}
                was clickable.
                """)
            else:
                self.set_fail_with_cause(f"""
                The element {self._current_web_element_name} with selector {self._current_web_element_selector}
                was not clickable.
                """)
            return None

    def _execute_ASSERT_ENABLED(self, arg):
        # self._execute_FIND_ELEMENT(**value)
        WebDriverWait(self.browser, arg.timeout).until(
            text_to_be_present_in_element((arg.selector, arg.element_name),arg.value)
        )


        if not self.current_web_element.is_enabled():
            self.set_fail_with_cause(f"""
            The element {self._current_web_element_name} with selector {self._current_web_element_selector}
            was not enabled.
            """)

    def set_fail_with_cause(self, cause):
        self.result = TestResult.FAIL
        self.cause = cause

    def _execute_ASSERT_VISIBLE(self, arg):
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
                self.set_fail_with_cause(f"""
                The element {self._current_web_element_name} with selector {self._current_web_element_selector}
                is displayed.
                """)
            else:
                self.set_fail_with_cause(f"""
                The element {self._current_web_element_name} with selector {self._current_web_element_selector}
                is not displayed.
                """)

    def _execute_EXISTS(self, arg):
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
                self.set_fail_with_cause(f"""
                The element {self._current_web_element_name} with selector {self._current_web_element_selector}
                does exist.
                """)
            else:
                self.set_fail_with_cause(f"""
                The element {self._current_web_element_name} with selector {self._current_web_element_selector}
                does not exist.
                """)

    def _execute_WAIT(self, argument):
        time.sleep(argument.value)

    def execute(self):

        for op in self.operations:
            if self.result is TestResult.FAIL:
                return
            command = op[0]
            inputs = op[1]
            self._current_ctx_pos = op[2]
            self.__current_argument = inputs
            fun = self.__OPS.get(command)
            fun(inputs)
            #match command:
            #    case Command.CLICK_ELEMENT:
            #        self._execute_CLICK_ELEMENT(inputs)
            #    case Command.FIND_ELEMENT:
            #        self._execute_FIND_ELEMENT(inputs)
            #    case Command.SLEEP:
            #        self._execute_WAIT(inputs)
            #    case Command.DROPDOWN_SELECT:
            #        self._execute_DROPDOWN_SELECT(inputs)
            #    case Command.SCREENSHOT:
            #        self._execute_SCREENSHOT(inputs)
            #    case Command.SEND_KEYS_TO_ELEMENT:
            #        self._execute_SEND_KEYS(inputs)
            #    case Command.ASSERT_EXISTS:
            #        self._execute_EXISTS(inputs)
            #    case Command.ASSERT_DISPLAYED:
            #        self._execute_ASSERT_VISIBLE(inputs)
            #    case Command.ASSERT_ENABLED:
            #        self._execute_ASSERT_ENABLED(inputs)
            #    case Command.ASSERT_PAGE_TITLE:
            #        self._execute_ASSERT_PAGE_TITLE(inputs)
            #    case Command.ASSERT_TEXT_VALUE:
            #        self._execute_ASSERT_TEXT_VALUE(inputs)
            #    case Command.ASSERT_SELECTED:
            #        self._execute_ASSERT_SELECTED(inputs)
            #    case Command.ASSERT_CLICKABLE:
            #        self._execute_ASSERT_CLICKABLE(inputs)
            #    case _:
            #        raise RuntimeError(f"Command not implemented: {command}")


class TestFailedException(Exception):
    def __init__(self, msg=None):
        self.message = msg



def generate_report(testcase):
    with StringIO() as buffer:
        buffer.write(str(testcase.name))
        buffer.write(": ")
        buffer.write(testcase.result)

        if testcase.result is TestResult.FAIL:
            buffer.write(str(testcase.cause))
            buffer.write(f"Error at line {testcase._current_ctx_pos[0]}, column {testcase._current_ctx_pos[1]}")
        print(buffer.getvalue())


class TestExecutionManager:
    def __init__(self):
        self.testcases = []

    def add_testcase(self, testcase):
        self.testcases.append(testcase)

    def execute(self):
        start = time.time()
        # print("============================= test session starts =============================")
        print(header(" test session starts ", 70, "=", "c"))
        print()
        passed = 0
        total = len(self.testcases)
        for testcase in self.testcases:
            testcase.execute()
            if testcase.result is not TestResult.FAIL:
                passed += 1
            generate_report(testcase)
            del testcase
        end = time.time()
        t_taken = round(end - start, 3)
        print()
        print(header(f" {passed} {TestResult.PASS} ", 70, "=", "c"))
        print(header(f" {total - passed} {TestResult.FAIL} ", 70, "=", "c"))
        print(header(color(Fore.YELLOW, f"{total} Total") + f" in {color(Fore.CYAN, t_taken)} s ", 90, "=", "c"))
        print()


class TestResult:
    PASS = color(Fore.GREEN, "PASSED")
    FAIL = color(Fore.RED, "FAILED")
