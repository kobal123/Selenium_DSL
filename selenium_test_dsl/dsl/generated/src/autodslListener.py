# Generated from .\src\autodsl.g4 by ANTLR 4.10.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .autodslParser import autodslParser
else:
    from autodslParser import autodslParser

# This class defines a complete listener for a parse tree produced by autodslParser.
class autodslListener(ParseTreeListener):

    # Enter a parse tree produced by autodslParser#program.
    def enterProgram(self, ctx:autodslParser.ProgramContext):
        pass

    # Exit a parse tree produced by autodslParser#program.
    def exitProgram(self, ctx:autodslParser.ProgramContext):
        pass


    # Enter a parse tree produced by autodslParser#test.
    def enterTest(self, ctx:autodslParser.TestContext):
        pass

    # Exit a parse tree produced by autodslParser#test.
    def exitTest(self, ctx:autodslParser.TestContext):
        pass


    # Enter a parse tree produced by autodslParser#statement.
    def enterStatement(self, ctx:autodslParser.StatementContext):
        pass

    # Exit a parse tree produced by autodslParser#statement.
    def exitStatement(self, ctx:autodslParser.StatementContext):
        pass


    # Enter a parse tree produced by autodslParser#expr.
    def enterExpr(self, ctx:autodslParser.ExprContext):
        pass

    # Exit a parse tree produced by autodslParser#expr.
    def exitExpr(self, ctx:autodslParser.ExprContext):
        pass


    # Enter a parse tree produced by autodslParser#basic_expr.
    def enterBasic_expr(self, ctx:autodslParser.Basic_exprContext):
        pass

    # Exit a parse tree produced by autodslParser#basic_expr.
    def exitBasic_expr(self, ctx:autodslParser.Basic_exprContext):
        pass


    # Enter a parse tree produced by autodslParser#table_select_expr.
    def enterTable_select_expr(self, ctx:autodslParser.Table_select_exprContext):
        pass

    # Exit a parse tree produced by autodslParser#table_select_expr.
    def exitTable_select_expr(self, ctx:autodslParser.Table_select_exprContext):
        pass


    # Enter a parse tree produced by autodslParser#list_expr.
    def enterList_expr(self, ctx:autodslParser.List_exprContext):
        pass

    # Exit a parse tree produced by autodslParser#list_expr.
    def exitList_expr(self, ctx:autodslParser.List_exprContext):
        pass


    # Enter a parse tree produced by autodslParser#urlopen.
    def enterUrlopen(self, ctx:autodslParser.UrlopenContext):
        pass

    # Exit a parse tree produced by autodslParser#urlopen.
    def exitUrlopen(self, ctx:autodslParser.UrlopenContext):
        pass


    # Enter a parse tree produced by autodslParser#set.
    def enterSet(self, ctx:autodslParser.SetContext):
        pass

    # Exit a parse tree produced by autodslParser#set.
    def exitSet(self, ctx:autodslParser.SetContext):
        pass


    # Enter a parse tree produced by autodslParser#wait.
    def enterWait(self, ctx:autodslParser.WaitContext):
        pass

    # Exit a parse tree produced by autodslParser#wait.
    def exitWait(self, ctx:autodslParser.WaitContext):
        pass


    # Enter a parse tree produced by autodslParser#sleep.
    def enterSleep(self, ctx:autodslParser.SleepContext):
        pass

    # Exit a parse tree produced by autodslParser#sleep.
    def exitSleep(self, ctx:autodslParser.SleepContext):
        pass


    # Enter a parse tree produced by autodslParser#text_click.
    def enterText_click(self, ctx:autodslParser.Text_clickContext):
        pass

    # Exit a parse tree produced by autodslParser#text_click.
    def exitText_click(self, ctx:autodslParser.Text_clickContext):
        pass


    # Enter a parse tree produced by autodslParser#click.
    def enterClick(self, ctx:autodslParser.ClickContext):
        pass

    # Exit a parse tree produced by autodslParser#click.
    def exitClick(self, ctx:autodslParser.ClickContext):
        pass


    # Enter a parse tree produced by autodslParser#refreshPage.
    def enterRefreshPage(self, ctx:autodslParser.RefreshPageContext):
        pass

    # Exit a parse tree produced by autodslParser#refreshPage.
    def exitRefreshPage(self, ctx:autodslParser.RefreshPageContext):
        pass


    # Enter a parse tree produced by autodslParser#clickTableCell.
    def enterClickTableCell(self, ctx:autodslParser.ClickTableCellContext):
        pass

    # Exit a parse tree produced by autodslParser#clickTableCell.
    def exitClickTableCell(self, ctx:autodslParser.ClickTableCellContext):
        pass


    # Enter a parse tree produced by autodslParser#screenshot.
    def enterScreenshot(self, ctx:autodslParser.ScreenshotContext):
        pass

    # Exit a parse tree produced by autodslParser#screenshot.
    def exitScreenshot(self, ctx:autodslParser.ScreenshotContext):
        pass


    # Enter a parse tree produced by autodslParser#value.
    def enterValue(self, ctx:autodslParser.ValueContext):
        pass

    # Exit a parse tree produced by autodslParser#value.
    def exitValue(self, ctx:autodslParser.ValueContext):
        pass


    # Enter a parse tree produced by autodslParser#type_select.
    def enterType_select(self, ctx:autodslParser.Type_selectContext):
        pass

    # Exit a parse tree produced by autodslParser#type_select.
    def exitType_select(self, ctx:autodslParser.Type_selectContext):
        pass


    # Enter a parse tree produced by autodslParser#identifier.
    def enterIdentifier(self, ctx:autodslParser.IdentifierContext):
        pass

    # Exit a parse tree produced by autodslParser#identifier.
    def exitIdentifier(self, ctx:autodslParser.IdentifierContext):
        pass


    # Enter a parse tree produced by autodslParser#action_assert.
    def enterAction_assert(self, ctx:autodslParser.Action_assertContext):
        pass

    # Exit a parse tree produced by autodslParser#action_assert.
    def exitAction_assert(self, ctx:autodslParser.Action_assertContext):
        pass


    # Enter a parse tree produced by autodslParser#text_result_assert.
    def enterText_result_assert(self, ctx:autodslParser.Text_result_assertContext):
        pass

    # Exit a parse tree produced by autodslParser#text_result_assert.
    def exitText_result_assert(self, ctx:autodslParser.Text_result_assertContext):
        pass


    # Enter a parse tree produced by autodslParser#exists_assert.
    def enterExists_assert(self, ctx:autodslParser.Exists_assertContext):
        pass

    # Exit a parse tree produced by autodslParser#exists_assert.
    def exitExists_assert(self, ctx:autodslParser.Exists_assertContext):
        pass


    # Enter a parse tree produced by autodslParser#page_assert.
    def enterPage_assert(self, ctx:autodslParser.Page_assertContext):
        pass

    # Exit a parse tree produced by autodslParser#page_assert.
    def exitPage_assert(self, ctx:autodslParser.Page_assertContext):
        pass


    # Enter a parse tree produced by autodslParser#text_action_assert.
    def enterText_action_assert(self, ctx:autodslParser.Text_action_assertContext):
        pass

    # Exit a parse tree produced by autodslParser#text_action_assert.
    def exitText_action_assert(self, ctx:autodslParser.Text_action_assertContext):
        pass


    # Enter a parse tree produced by autodslParser#dropdown_select.
    def enterDropdown_select(self, ctx:autodslParser.Dropdown_selectContext):
        pass

    # Exit a parse tree produced by autodslParser#dropdown_select.
    def exitDropdown_select(self, ctx:autodslParser.Dropdown_selectContext):
        pass


    # Enter a parse tree produced by autodslParser#begin_testcase.
    def enterBegin_testcase(self, ctx:autodslParser.Begin_testcaseContext):
        pass

    # Exit a parse tree produced by autodslParser#begin_testcase.
    def exitBegin_testcase(self, ctx:autodslParser.Begin_testcaseContext):
        pass


    # Enter a parse tree produced by autodslParser#end_testcase.
    def enterEnd_testcase(self, ctx:autodslParser.End_testcaseContext):
        pass

    # Exit a parse tree produced by autodslParser#end_testcase.
    def exitEnd_testcase(self, ctx:autodslParser.End_testcaseContext):
        pass


    # Enter a parse tree produced by autodslParser#dropdown_by.
    def enterDropdown_by(self, ctx:autodslParser.Dropdown_byContext):
        pass

    # Exit a parse tree produced by autodslParser#dropdown_by.
    def exitDropdown_by(self, ctx:autodslParser.Dropdown_byContext):
        pass


    # Enter a parse tree produced by autodslParser#execute_script.
    def enterExecute_script(self, ctx:autodslParser.Execute_scriptContext):
        pass

    # Exit a parse tree produced by autodslParser#execute_script.
    def exitExecute_script(self, ctx:autodslParser.Execute_scriptContext):
        pass


    # Enter a parse tree produced by autodslParser#scrollFixedLength.
    def enterScrollFixedLength(self, ctx:autodslParser.ScrollFixedLengthContext):
        pass

    # Exit a parse tree produced by autodslParser#scrollFixedLength.
    def exitScrollFixedLength(self, ctx:autodslParser.ScrollFixedLengthContext):
        pass


    # Enter a parse tree produced by autodslParser#scrollToElement.
    def enterScrollToElement(self, ctx:autodslParser.ScrollToElementContext):
        pass

    # Exit a parse tree produced by autodslParser#scrollToElement.
    def exitScrollToElement(self, ctx:autodslParser.ScrollToElementContext):
        pass


    # Enter a parse tree produced by autodslParser#clearInput.
    def enterClearInput(self, ctx:autodslParser.ClearInputContext):
        pass

    # Exit a parse tree produced by autodslParser#clearInput.
    def exitClearInput(self, ctx:autodslParser.ClearInputContext):
        pass



del autodslParser