# Generated from .\src\autodsl.g4 by ANTLR 4.10.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .autodslParser import autodslParser
else:
    from autodslParser import autodslParser

# This class defines a complete generic visitor for a parse tree produced by autodslParser.

class autodslVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by autodslParser#program.
    def visitProgram(self, ctx:autodslParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by autodslParser#test.
    def visitTest(self, ctx:autodslParser.TestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by autodslParser#statement.
    def visitStatement(self, ctx:autodslParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by autodslParser#expr.
    def visitExpr(self, ctx:autodslParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by autodslParser#basic_expr.
    def visitBasic_expr(self, ctx:autodslParser.Basic_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by autodslParser#table_select_expr.
    def visitTable_select_expr(self, ctx:autodslParser.Table_select_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by autodslParser#list_expr.
    def visitList_expr(self, ctx:autodslParser.List_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by autodslParser#urlopen.
    def visitUrlopen(self, ctx:autodslParser.UrlopenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by autodslParser#set.
    def visitSet(self, ctx:autodslParser.SetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by autodslParser#wait.
    def visitWait(self, ctx:autodslParser.WaitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by autodslParser#sleep.
    def visitSleep(self, ctx:autodslParser.SleepContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by autodslParser#text_click.
    def visitText_click(self, ctx:autodslParser.Text_clickContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by autodslParser#click.
    def visitClick(self, ctx:autodslParser.ClickContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by autodslParser#refreshPage.
    def visitRefreshPage(self, ctx:autodslParser.RefreshPageContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by autodslParser#clickTableCell.
    def visitClickTableCell(self, ctx:autodslParser.ClickTableCellContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by autodslParser#screenshot.
    def visitScreenshot(self, ctx:autodslParser.ScreenshotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by autodslParser#value.
    def visitValue(self, ctx:autodslParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by autodslParser#type_select.
    def visitType_select(self, ctx:autodslParser.Type_selectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by autodslParser#identifier.
    def visitIdentifier(self, ctx:autodslParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by autodslParser#action_assert.
    def visitAction_assert(self, ctx:autodslParser.Action_assertContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by autodslParser#text_result_assert.
    def visitText_result_assert(self, ctx:autodslParser.Text_result_assertContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by autodslParser#exists_assert.
    def visitExists_assert(self, ctx:autodslParser.Exists_assertContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by autodslParser#page_assert.
    def visitPage_assert(self, ctx:autodslParser.Page_assertContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by autodslParser#text_action_assert.
    def visitText_action_assert(self, ctx:autodslParser.Text_action_assertContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by autodslParser#dropdown_select.
    def visitDropdown_select(self, ctx:autodslParser.Dropdown_selectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by autodslParser#begin_testcase.
    def visitBegin_testcase(self, ctx:autodslParser.Begin_testcaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by autodslParser#end_testcase.
    def visitEnd_testcase(self, ctx:autodslParser.End_testcaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by autodslParser#dropdown_by.
    def visitDropdown_by(self, ctx:autodslParser.Dropdown_byContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by autodslParser#execute_script.
    def visitExecute_script(self, ctx:autodslParser.Execute_scriptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by autodslParser#scrollFixedLength.
    def visitScrollFixedLength(self, ctx:autodslParser.ScrollFixedLengthContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by autodslParser#scrollToElement.
    def visitScrollToElement(self, ctx:autodslParser.ScrollToElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by autodslParser#clearInput.
    def visitClearInput(self, ctx:autodslParser.ClearInputContext):
        return self.visitChildren(ctx)



del autodslParser