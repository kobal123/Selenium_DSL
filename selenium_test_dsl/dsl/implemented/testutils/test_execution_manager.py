import time
from io import StringIO
from colorama import Fore
from dsl.implemented.testutils.test_executor import TestExecutor
from dsl.implemented.testutils.testcase import TestCase
from dsl.implemented.testutils.TestResult import TestResult
from dsl.implemented.utility.util import header
from dsl.implemented.utility.util import color
from colorama import init, Fore

init()

from dsl.implemented.utility.util import auto_str


@auto_str
class TestExecutionManager:
    """
    Holds the list of testcases to be executed and  provides some statistics about
    the execution.
    """

    def __init__(self, browser):
        self.testcases = []
        self.browser = browser

    def add_testcase(self, testcase_):
        self.testcases.append(testcase_)

    def execute(self):
        executor = TestExecutor(self.browser)
        start = time.time()
        print(header(" test session starts ", 70, "=", "c"))
        print()
        passed = 0
        total = len(self.testcases)
        for testcase_ in self.testcases:
            executor.set_testcase(testcase_)
            executor.execute()

            if testcase_.result is not TestResult.FAIL:
                passed += 1

        self.testcases = []
        end = time.time()
        t_taken = round(end - start, 3)
        print()
        print(header(f" {passed} {color(Fore.GREEN, TestResult.PASS)} ", 70, "=", "c"))
        print(header(f" {str(total - passed)} {color(Fore.RED, TestResult.FAIL)} ", 70, "=", "c"))
        print(header(color(Fore.YELLOW, f"{total} Total") + f" in {color(Fore.CYAN, t_taken)} s ", 90, "=", "c"))
        print()
