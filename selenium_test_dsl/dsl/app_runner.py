import sys
import pathlib

# DO NOT MOVE THIS FILE ANYWHERE
# TODO: solve PYTHONPATH import problems without modifying sys.path
sys.path.insert(0,str(pathlib.Path(__file__).parent.parent.resolve()))

import dsl.implemented.visitor.selenium_visitor as sel
if len(sys.argv) == 2 and sys.argv[1] == "--harness":
    import dsl.implemented.harness.test_mode_selenium_visitor as tsel
    print("running test harness")
    tsel.main()
else:
    sel.main()
