from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_webelement_method_redirection(browser):
    """Test that WebElement methods are properly redirected."""
    wait = WebDriverWait(browser.driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Get an input element
    input_element = browser.find("#username").first()
    assert input_element, "Should find username input"

    # Test WebElement methods
    assert input_element.get_attribute("id") == "username", "Should get correct attribute"
    assert input_element.tag_name == "input", "Should get correct tag name"
    assert input_element.is_displayed(), "Should be displayed"
    assert input_element.is_enabled(), "Should be enabled"


def test_webelement_method_chaining(browser):
    """Test that WebElement methods can be chained with BrowserJQuery methods."""
    wait = WebDriverWait(browser.driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Test chaining WebElement and BrowserJQuery methods
    element = browser.find("input").first()
    assert element, "Should find input element"

    # Chain WebElement and BrowserJQuery methods
    assert element.get_attribute("type") == "text", "Should get correct type"
    assert element.has_class("form-control") is False, "Should not have form-control class"
    assert element.is_displayed(), "Should be displayed"
    assert element.next() is not None, "Should have next element"


def test_webelement_property_access(browser):
    """Test that WebElement properties are properly accessed."""
    wait = WebDriverWait(browser.driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Get an element
    element = browser.find("a").first()
    assert element, "Should find anchor element"

    # Test WebElement properties
    assert element.tag_name == "a", "Should get correct tag name"
    assert element.text() == "Sign in", "Should get correct text"
    assert element.get_attribute("class") == "nav-link", "Should get correct class"


def test_webelement_method_result_wrapping(browser):
    """Test that WebElement method results are properly wrapped in BrowserJQuery instances."""
    wait = WebDriverWait(browser.driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Get a parent element
    parent = browser.find("nav").first()
    assert parent, "Should find nav element"

    # Test that find_element returns a wrapped element
    child = parent.find_element(By.TAG_NAME, "a")
    assert child, "Should find child element"
    assert child.has_class("nav-link"), "Should have nav-link class"
    assert child.text() == "Sign in", "Should have correct text"


def test_webelement_list_result_wrapping(browser):
    """Test that WebElement list results are properly wrapped in BrowserJQueryCollection."""
    wait = WebDriverWait(browser.driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Get a parent element
    parent = browser.find("nav").first()
    assert parent, "Should find nav element"

    # Test that find_elements returns a collection
    children = parent.find_elements(By.TAG_NAME, "a")
    assert children, "Should find child elements"
    assert len(children) > 0, "Should have at least one child"
    # Access the first element directly since we get a list
    first_child = children[0]
    assert isinstance(first_child, browser.__class__), "First child should be wrapped in BrowserJQuery"
    assert first_child.text() == "Sign in", "First child should have correct text"
