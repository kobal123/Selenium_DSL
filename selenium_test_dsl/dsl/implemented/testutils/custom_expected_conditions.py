import time

from selenium.common import StaleElementReferenceException, JavascriptException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from dsl.implemented.testutils.js_scripts import table_select_script
from dsl.implemented.testutils.js_scripts import find_element_by_text_script

def flatten(l):
    return [item for sublist in l for item in sublist]


def stripped_text_to_be_present_in_element(locator, text_):
    """ An expectation for checking if the given text is present in the
    specified element.
    locator, text
    """

    def _predicate(driver):
        try:
            element_text = driver.find_element(*locator).text
            return text_.strip() in element_text.strip()
        except StaleElementReferenceException:
            return False

    return _predicate


def stripped_text_to_be_present_in_value(locator, text_):
    """
    An expectation for checking if the given text is present in the element's value.
    locator, text
    """

    def _predicate(driver):
        try:
            element_text = driver.find_element(*locator).get_attribute("value")

            return text_.strip() in element_text.strip()
        except StaleElementReferenceException:
            return False

    return _predicate


def text_to_be_displayed(text):
    def predicate_(driver):
        try:
            element = driver.execute_script(find_element_by_text_script,text)
            if element and element.is_displayed():
                return element
            else:
                return False
        except StaleElementReferenceException as e:
            print(e)
            return False
        except JavascriptException as e:
            print(e)
            return False
    return predicate_


def text_to_be_selected(text):
    def predicate_(driver):
        try:
            element = driver.execute_script(find_element_by_text_script, text)

            if element and element.is_selected():
                return element
            else:
                return False
        except StaleElementReferenceException:
            return False
        except JavascriptException:
            return False
    return predicate_


def text_to_be_clickable(text):
    def predicate_(driver):
        try:
            element = driver.execute_script(find_element_by_text_script, text)

            if element and element.is_displayed() and element.is_enabled():
                return element
            else:
                return False
        except StaleElementReferenceException:
            return False
        except JavascriptException as e:
            print(e)
            return False
    return predicate_


def table_cell_clickable(h_index, **expected_values):
    def _o_pred(driver):
        res = driver.execute_script(table_select_script, h_index, expected_values)

        if res:

            return res
        else:
            return False

    def _predicate(driver):
        s = time.time()
        # print("from execute script")
        # print(f"result from running script: {result}, type of result is {type(result)}")

        table_rows = driver.find_elements(by=By.TAG_NAME, value="tr")
        results = list(map(lambda x: x.find_elements(by=By.TAG_NAME, value="td"), table_rows))
        headers = list(map(lambda x: x.find_elements(by=By.TAG_NAME, value="th"), table_rows))

        # TODO: below code is for searching a specific table for given elements.
        # table_rows: WebElement = driver.find_element(by=By.ID, value="table")
        ##print("asdf",table_rows.find_elements(by=By.TAG_NAME, value="tr"))
        # results = list(table_rows.find_elements(by=By.TAG_NAME, value="tr"))
        ##print(f"results are {results}")
        # results2 = results
        # results = list(map(lambda x:x.find_elements(by=By.TAG_NAME,value="td"),results))
        # headers = list(results2[0].find_elements(by=By.TAG_NAME,value="th"))

        headers = flatten(headers)
        h_dict = dict()
        index = 0

        for header in headers:
            h_dict[header.text] = index
            index += 1
        found = True
        cell = False
        total = 0
        for row in results:
            for item_index in range(len(row)):
                total += 1
                found = True
                if len(row) == index:

                    for header, h_value in expected_values.items():
                        if row[h_dict.get(header)].text != h_value:
                            found = False
                            # print(row[h_dict.get(h_index)])
                            break
                    if found:
                        cell: WebElement = row[h_dict.get(h_index)]
                        children = cell.find_elements(By.CSS_SELECTOR, value="*")
                        if children:
                            e = time.time()
                            print(f"time taken: {e - s}")
                            return children[0]
                        elif cell:
                            e = time.time()
                            print(f"time taken: {e - s}")
                            return cell

        e = time.time()
        print(f"time taken: {e - s}, total {total}")
        return False

    return _o_pred
