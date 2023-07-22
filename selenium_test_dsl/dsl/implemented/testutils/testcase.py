from .TestResult import TestResult
from .commands import Command
from .testutility import Argument
from dsl.implemented.utility.util import auto_str

@auto_str
class TestCase:
    """
    Represents a single testcase with a list of commands.
    """

    __test_case_num = 0

    def __init__(self, name=""):

        if name == "":
            self.name = f"test case {TestCase.__test_case_num}"
        else:
            self.name = name

        self.result = TestResult.PASS
        self.commands = []
        self.cause = None
        TestCase.__test_case_num += 1

    def put_op(self, command: Command, ctx_pos: tuple, args: Argument = None):
        """
        Adds a command to be executed in this testcase.

        Args:
            command: a Command type to be executed.
            ctx_pos: the position of the antlr context, needed for error messages.
            args: the arguments the command will be executed with.
        """
        self.commands.append(tuple([command, args, ctx_pos]))
