from unittest.mock import MagicMock

import pytest
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

from browserjquery import BrowserJQuery


@pytest.fixture
def mock_driver():
    driver = MagicMock(spec=webdriver.Chrome)
    return driver


@pytest.fixture
def browser_jquery(mock_driver):
    return BrowserJQuery(mock_driver)


def test_init(mock_driver):
    jquery = BrowserJQuery(mock_driver)
    assert jquery.driver == mock_driver


def test_ensure_jquery_injects_when_not_present(browser_jquery):
    browser_jquery.is_jquery_injected = False
    browser_jquery.inject_jquery = MagicMock()

    browser_jquery.ensure_jquery()

    browser_jquery.inject_jquery.assert_called_once()


def test_ensure_jquery_does_not_inject_when_present(browser_jquery):
    browser_jquery.is_jquery_injected = True
    browser_jquery.inject_jquery = MagicMock()

    browser_jquery.ensure_jquery()

    browser_jquery.inject_jquery.assert_not_called()


def test_execute(browser_jquery):
    script = "return $('div')"
    args = ("arg1", "arg2")
    expected_result = [MagicMock(spec=WebElement)]

    browser_jquery.driver.execute_script.return_value = expected_result

    result = browser_jquery.execute(script, *args)

    browser_jquery.driver.execute_script.assert_called_once_with(script, *args)
    assert result == expected_result


def test_query(browser_jquery):
    script = "return $(arguments[0]).find('div')"
    element = MagicMock(spec=WebElement)
    args = ("arg1", "arg2")
    expected_result = [MagicMock(spec=WebElement)]

    browser_jquery.execute.return_value = expected_result

    result = browser_jquery.query(script, element, *args)

    browser_jquery.execute.assert_called_once_with(script, element, *args)
    assert result == expected_result


def test_document_property(browser_jquery):
    expected_result = MagicMock(spec=WebElement)
    browser_jquery.execute.return_value = expected_result

    result = browser_jquery.document

    browser_jquery.execute.assert_called_once_with("return $(document.documentElement)")
    assert result == expected_result


def test_page_html_property(browser_jquery):
    expected_html = "<html><body>Test</body></html>"
    browser_jquery.execute.return_value = expected_html

    result = browser_jquery.page_html

    assert result == expected_html


def test_find_with_selector(browser_jquery):
    selector = "div.test"
    element = MagicMock(spec=WebElement)
    expected_result = [MagicMock(spec=WebElement)]

    browser_jquery.query.return_value = expected_result

    result = browser_jquery.find(selector, element)

    browser_jquery.query.assert_called_once()
    assert result == expected_result


def test_find_with_first_match(browser_jquery):
    selector = "div.test"
    element = MagicMock(spec=WebElement)
    expected_result = [MagicMock(spec=WebElement)]

    browser_jquery.query.return_value = expected_result

    result = browser_jquery.find(selector, element, first_match=True)

    browser_jquery.query.assert_called_once()
    assert result == expected_result[0]


def test_find_elements_with_text(browser_jquery):
    text = "Test Text"
    selector = "div"
    element = MagicMock(spec=WebElement)
    expected_result = [MagicMock(spec=WebElement)]

    browser_jquery.query.return_value = expected_result

    result = browser_jquery.find_elements_with_text(text, selector, element)

    browser_jquery.query.assert_called_once()
    assert result == expected_result


def test_find_closest_ancestor(browser_jquery):
    selector = "div.parent"
    element = MagicMock(spec=WebElement)
    expected_result = MagicMock(spec=WebElement)

    browser_jquery.query.return_value = expected_result

    result = browser_jquery.find_closest_ancestor(selector, element)

    browser_jquery.query.assert_called_once()
    assert result == expected_result


def test_has_class(browser_jquery):
    element = MagicMock(spec=WebElement)
    class_name = "test-class"
    expected_result = True

    browser_jquery.query.return_value = expected_result

    result = browser_jquery.has_class(element, class_name)

    browser_jquery.query.assert_called_once()
    assert result == expected_result


def test_parent(browser_jquery):
    element = MagicMock(spec=WebElement)
    expected_result = MagicMock(spec=WebElement)

    browser_jquery.query.return_value = expected_result

    result = browser_jquery.parent(element)

    browser_jquery.query.assert_called_once()
    assert result == expected_result


def test_parents(browser_jquery):
    element = MagicMock(spec=WebElement)
    expected_result = [MagicMock(spec=WebElement)]

    browser_jquery.query.return_value = expected_result

    result = browser_jquery.parents(element)

    browser_jquery.query.assert_called_once()
    assert result == expected_result
