import json
import os
import sys
from antlr4 import *
from selenium.common import WebDriverException

from dsl.generated.src.autodslVisitor import autodslVisitor
from dsl.generated.src.autodslLexer import autodslLexer
from dsl.generated.src.autodslParser import autodslParser
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.edge.service import Service as edgeService
from selenium.webdriver.edge.options import Options as edgeOptions
from selenium.webdriver.chrome.service import Service as chromeService
from selenium.webdriver.chrome.options import Options as chromeOptions
from selenium.webdriver.firefox.service import Service as firefoxService
from selenium.webdriver.firefox.options import Options as firefoxOptions

from dsl.implemented.testutils.js_scripts import table_select_script
from dsl.implemented.testutils.commands import *
from dsl.implemented.testutils.test_execution_manager import TestExecutionManager
from dsl.implemented.testutils.testcase import TestCase
from dsl.implemented.testutils.argument import Argument
from definitions import CONFIG_PATH
from definitions import RESOURCES_PATH
from definitions import EXAMPLE_INPUTS_PATH
from definitions import ENV_VAR_PATH
from json import load

total_terminals = 0


class ValueNotDefinedException(Exception):
    pass


def get_ctx_pos(ctx):
    """
    Returns a tuple of the position of the context in the input file.
    Used for error messages.
    Args:
        ctx: The antlr current context

    Returns:
        A tuple of positions, first the line number, second the column number.
    """
    return ctx.start.line, ctx.start.column


def get_action_command(action):
    return {
        "displayed": Command.ASSERT_DISPLAYED,
        "clickable": Command.ASSERT_CLICKABLE,
        "enabled": Command.ASSERT_ENABLED,
        "selected": Command.ASSERT_SELECTED,
    }.get(action)


def get_text_action_command(action):
    return {
        "displayed": Command.TEXT_ASSERT_DISPLAYED,
        "clickable": Command.TEXT_ASSERT_CLICKABLE,
        "enabled": Command.TEXT_ASSERT_ENABLED,
        "selected": Command.TEXT_ASSERT_SELECTED,
    }.get(action)


class Visitor(autodslVisitor):
    """Implementation of the antlr visitor for the selenium automation DSL"""

    def __init__(self):
        super().__init__()
        self.values = None
        self.config = None
        self.load_config_file()
        self.load_env_variables()
        self.browser = self.__init_browser()
        self.browser.maximize_window()

        self.line_counter = 1
        self.saved_file_counter = 0
        self.test_manager = TestExecutionManager(self.browser)
        self.current_test_case = TestCase(self.browser)
        self.type_dict = {
            "css": By.CSS_SELECTOR,
            "name": By.NAME,
            "xpath": By.XPATH,
            'id': By.ID,
            "text": By.PARTIAL_LINK_TEXT
        }

    def get_value(self, value: str):
        """
        Returns the input without trailing quotes, or if it's a reference, the reference value

        Args:
            value: A string with trailing quotes, or a value reference starting with $
        Returns:
            The input without trailing quotes or a reference value

        """
        s = str(value)
        if s.startswith("$"):
            val = self.values.get(s[1:])
            if val is None:
                print(f" The value {value} was not defined in the env.json file.")
                print(" Script exiting")
                self.browser.quit()
                sys.exit(1)
            return val
        return s[1:-1] if s[0] == "'" or s[0] == '"' else s

    def __driver_options(self, browser):
        option = {
            "firefox": firefoxOptions(),
            "chrome": chromeOptions(),
            "edge": edgeOptions()
        }[browser]

        if browser == "edge":
            option.add_experimental_option('excludeSwitches', ['enable-logging'])

        if self.config['headless']:
            option.add_argument("--headless")

        return option

    def __init_browser(self):
        """
        Returns: A WebDriver instance of the browser specified.

        """
        browser = self.config['browser']
        driverPath = self.config['driverPath']
        # service = Service(r"C:\selenium_drivers\msedgedriver.exe")
        # options = Options()
        # options.add_argument("--headless")
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # webdriver.Edge(service=ser, options=options)
        options_ = self.__driver_options(browser)
        get_browser = {
            "firefox": lambda: webdriver.Firefox(service=firefoxService(driverPath), options=options_),
            "chrome": lambda: webdriver.Chrome(service=chromeService(driverPath), options=options_),
            "edge": lambda: webdriver.Edge(service=edgeService(driverPath), options=options_)
        }[browser]
        return get_browser()

    def get_type(self, type_selector):
        return self.type_dict.get(type_selector, By.ID)

    def visitValue(self, ctx: autodslParser.ValueContext):
        return self.visitChildren(ctx)

    def visitExecute_script(self, ctx: autodslParser.Execute_scriptContext):
        arg_list = []
        script = self.visit(ctx.TEXT())
        if ctx.identifier():
            # if there are multiple arguments for the script
            if type(ctx.identifier()) is list:
                for identifier in ctx.identifier():
                    arg_list.append(self.visit(identifier))
            else:
                arg_list.append(self.visit(ctx.identifier()))
        arg = Argument(value=arg_list, dictionary={'script': script})

        self.current_test_case.put_op(Command.EXECUTE_SCRIPT, get_ctx_pos(ctx), arg)
        return self.visitChildren(ctx)

    def visitSet(self, ctx: autodslParser.SetContext):
        value = self.visit(ctx.set_text_value)
        value = self.get_value(value)
        arg: Argument = self.visit(ctx.expr())
        arg.value = value
        timeout = self.visit(ctx.wait()) if ctx.wait() else 0
        # print(f"timeout is {timeout}")
        arg.timeout = timeout

        self.current_test_case.put_op(Command.SEND_KEYS_TO_ELEMENT,
                                      get_ctx_pos(ctx),
                                      arg)

    def visitSleep(self, ctx: autodslParser.SleepContext):
        timeout = self.visit(ctx.INT())
        timeout = int(timeout)
        self.current_test_case.put_op(Command.SLEEP, get_ctx_pos(ctx), Argument(value=timeout))
        return self.visitChildren(ctx)

    def visitBegin_testcase(self, ctx: autodslParser.Begin_testcaseContext):
        test_name = ""
        if ctx.TEST_NAME():
            test_name = self.get_value(self.visit(ctx.TEST_NAME()))
        self.current_test_case = TestCase(test_name)

    def visitEnd_testcase(self, ctx: autodslParser.End_testcaseContext):
        self.test_manager.add_testcase(self.current_test_case)

    def visitType_select(self, ctx: autodslParser.Type_selectContext):
        # print("select type is:", self.visit(ctx.SELECT_TYPE()))
        return self.get_type(self.visit(ctx.SELECT_TYPE()))

    def visitText_result_assert(self, ctx: autodslParser.Text_result_assertContext):
        text_value = self.get_value(self.visit(ctx.assert_text_value))
        arg = self.visit(ctx.expr())
        arg.value = text_value
        # argument = Argument(element_name=element,
        #                    selector=by,
        #                    value=text_value)
        arg.by_value = False

        if ctx.INPUT():
            arg.by_value = True
        self.current_test_case.put_op(Command.ASSERT_TEXT_VALUE,
                                      get_ctx_pos(ctx),
                                      arg)

        return self.visitChildren(ctx)

    def visitDropdown_select(self, ctx: autodslParser.Dropdown_selectContext):
        dropdown_value = self.get_value(ctx.dropdown_value.text)
        arg = self.visit(ctx.basic_expr())
        arg.value = dropdown_value
        self.current_test_case.put_op(Command.DROPDOWN_SELECT,
                                      get_ctx_pos(ctx),
                                      arg)

    def visitClickTableCell(self, ctx: autodslParser.ClickTableCellContext):
        arg = self.visit(ctx.table_select_expr())
        self.current_test_case.put_op(Command.TABLE_SELECT,
                                      get_ctx_pos(ctx),
                                      arg)

    def visitScrollFixedLength(self, ctx: autodslParser.ScrollFixedLengthContext):
        self.current_test_case.put_op(Command.EXECUTE_SCRIPT,
                                      get_ctx_pos(ctx),
                                      Argument(dictionary={"script": '"window.scrollBy(0,arguments[0])"'},
                                               value=[self.visit(ctx.INT())]))

    def visitScrollToElement(self, ctx: autodslParser.ScrollToElementContext):
        pass

    def visitScreenshot(self, ctx: autodslParser.ScreenshotContext):
        filename = ""
        if ctx.TEXT():
            filename = self.visit(ctx.TEXT())
        else:
            filename = "screenshot_{}.png".format(self.saved_file_counter)
            self.saved_file_counter += 1
        self.current_test_case.put_op(Command.SCREENSHOT, get_ctx_pos(ctx), Argument(filename=filename))

    def visitExists_assert(self, ctx: autodslParser.Exists_assertContext):
        return self.visitChildren(ctx)

    def visitAction_assert(self, ctx: autodslParser.Action_assertContext):
        negate = True if ctx.NEGATE() else False
        action = self.visit(ctx.ACTION())
        command = get_action_command(action)
        arg = self.visit(ctx.expr())
        arg.negate = negate
        self.current_test_case.put_op(command,
                                      get_ctx_pos(ctx),
                                      arg)

    def visitPage_assert(self, ctx: autodslParser.Page_assertContext):
        page_title = self.visit(ctx.identifier())
        self.current_test_case.put_op(Command.ASSERT_PAGE_TITLE,
                                      get_ctx_pos(ctx),
                                      Argument(value=page_title))

    def visitTerminal(self, node):
        global total_terminals
        s = str(node)
        # print(total_terminals,s)
        total_terminals += 1
        return s[1:-1] if s[0] == "'" or s[0] == '"' else s

    def visitClick(self, ctx: autodslParser.ClickContext):
        timeout = self.visit(ctx.wait()) if ctx.wait() else 0
        arg: Argument = self.visit(ctx.expr())
        arg.timeout = timeout
        self.current_test_case.put_op(Command.CLICK_ELEMENT,
                                      get_ctx_pos(ctx),
                                      arg)

    def visitProgram(self, ctx: autodslParser.ProgramContext):
        self.load_config_file()
        self.load_env_variables()
        self.visitChildren(ctx)

    def visitUrlopen(self, ctx: autodslParser.UrlopenContext):

        url = self.get_value(self.visit(ctx.identifier()))
        self.current_test_case.put_op(Command.OPEN_PAGE, get_ctx_pos(ctx), Argument(value=url))

    def visitWait(self, ctx: autodslParser.WaitContext):
        timeout = self.visit(ctx.INT())
        timeout = int(timeout)
        return timeout

    def visitExpr(self, ctx: autodslParser.ExprContext):
        """
        Returns:
            An Argument with the element selector and value specified
        """
        if ctx.basic_expr():
            return self.visit(ctx.basic_expr())
        elif ctx.table_select_expr():
            return self.visit(ctx.table_select_expr())

    def visitBasic_expr(self, ctx: autodslParser.Basic_exprContext):
        type_selector = ctx.type_select()
        by = self.visit(type_selector)
        element_name = self.visit(ctx.identifier())
        element_name = self.get_value(element_name)
        return Argument(selector=by, element_name=element_name)

    def load_config_file(self):
        with open(CONFIG_PATH) as file:
            self.config = json.load(file)

    def load_env_variables(self):
        with open(ENV_VAR_PATH) as file:
            self.values = json.load(file)

    def visitClearInput(self, ctx: autodslParser.ClearInputContext):
        arg = self.visit(ctx.basic_expr())
        self.current_test_case.put_op(Command.CLEAR_INPUT,
                                      get_ctx_pos(ctx),
                                      arg)

    def visitIdentifier(self, ctx: autodslParser.IdentifierContext):
        value = None
        if ctx.TEXT():
            value = self.visit(ctx.TEXT())
        elif ctx.INLINE_IDENTIFIER():
            value = self.visit(ctx.INLINE_IDENTIFIER())
        return self.get_value(value)

    def visitTable_select_expr(self, ctx: autodslParser.Table_select_exprContext):
        cell_to_be_clicked = self.visit(ctx.tableCellToClickOn)
        header_name = self.visit(ctx.hname)
        header_value = self.visit(ctx.hval)
        arg = Argument(value=cell_to_be_clicked, dictionary={header_name: header_value})
        arg.script = table_select_script
        return arg

    def visitText_action_assert(self, ctx: autodslParser.Text_action_assertContext):
        value = self.visit(ctx.identifier())
        value = self.get_value(value)
        timeout = self.visit(ctx.wait()) if ctx.wait() else 0

        arg = Argument(value=value, timeout=timeout)
        self.current_test_case.put_op(Command.TEXT_ASSERT_DISPLAYED,
                                      get_ctx_pos(ctx),
                                      arg)

    def visitRefreshPage(self, ctx:autodslParser.RefreshPageContext):
        self.current_test_case.put_op(Command.REFRESH_PAGE,
                                      get_ctx_pos(ctx),
                                      None)

    def visitText_click(self, ctx: autodslParser.Text_clickContext):
        value = self.visit(ctx.identifier())
        value = self.get_value(value)
        timeout = self.visit(ctx.wait()) if ctx.wait() else 0

        arg = Argument(value=value, timeout=timeout)
        self.current_test_case.put_op(Command.TEXT_CLICK,
                                      get_ctx_pos(ctx),
                                      arg)


def start():
    lexer = None
    if len(sys.argv) == 2:
        lexer = autodslLexer(FileStream(sys.argv[1]))
    else:
        lexer = autodslLexer(FileStream(
            os.path.join(EXAMPLE_INPUTS_PATH, "input.dsl")
        ))

    stream = CommonTokenStream(lexer)
    parser = autodslParser(stream)
    tree = parser.program()
    print("Starting browser")
    visitor = Visitor()
    visitor.visit(tree)
    #try:
    visitor.test_manager.execute()
    visitor.browser.quit()
    #except WebDriverException:
    #    print("An error happened, check if the browser was closed during execution")
    #    print("Ending script.")
    #    visitor.browser.quit()


def main():
    start()


if __name__ == '__main__':
    main()
