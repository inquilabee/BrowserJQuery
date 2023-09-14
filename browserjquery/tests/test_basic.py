import time

from selenium.webdriver import Chrome

from browserjquery.jquery import BrowserJQuery


def test_basic_function():
    driver = Chrome()

    driver.get("https://www.yahoo.com")

    time.sleep(10)

    jquery = BrowserJQuery(driver)

    assert jquery(".stream-item"), "BrowserQuery is not working"
