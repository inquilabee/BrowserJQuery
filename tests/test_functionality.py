from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_has_class(browser):
    """Test if an element has a specific class."""
    # Wait for the container element to be present
    wait = WebDriverWait(browser.driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "container")))

    # Find the element using BrowserJQuery
    element = browser.find("#container", first_match=True)
    assert element, "Should find container element"

    # Test the class
    assert browser.has_class(element, "test-class"), "Should have the expected class"


def test_matches_selector(browser):
    element = browser.find("a", first_match=True)
    assert element, "Should find an anchor element"
    assert browser.matches_selector(element, "a"), "Should match anchor selector"


def test_has_descendants(browser):
    element = browser.find("body", first_match=True)
    assert element, "Should find body element"
    assert browser.has(element, "a"), "Should have anchor descendants"


def test_attr(browser):
    element = browser.find("a", first_match=True)
    assert element, "Should find an anchor element"
    href = browser.attr(element, "href")
    assert href == "#", "Href should be #"


def test_text(browser):
    element = browser.find("a", first_match=True)
    assert element, "Should find an anchor element"
    text = browser.text(element)
    assert text == "Sign in", "Should have correct text content"


def test_html(browser):
    element = browser.find("body", first_match=True)
    assert element, "Should find body element"
    html = browser.html(element)
    assert html, "Should have HTML content"
    assert "<" in html, "HTML should contain tags"


def test_children(browser):
    element = browser.find("body", first_match=True)
    assert element, "Should find body element"
    children = browser.children(element)
    assert children, "Should have children"
    assert len(children) > 0, "Should have at least one child"


def test_children_with_selector(browser):
    element = browser.find("nav", first_match=True)
    assert element, "Should find nav element"
    children = browser.children(element, "a")
    assert children, "Should have anchor children"
    assert len(children) > 0, "Should have at least one anchor child"


def test_siblings(browser):
    element = browser.find("a", first_match=True)
    assert element, "Should find an anchor element"
    siblings = browser.siblings(element)
    assert siblings, "Should have siblings"
    assert len(siblings) > 0, "Should have at least one sibling"


def test_siblings_with_selector(browser):
    element = browser.find("a", first_match=True)
    assert element, "Should find an anchor element"
    siblings = browser.siblings(element, "a")
    assert siblings, "Should have sibling anchors"
    assert len(siblings) > 0, "Should have at least one sibling anchor"


def test_next(browser):
    element = browser.find("a", first_match=True)
    assert element, "Should find an anchor element"
    next_element = browser.next(element)
    assert next_element, "Should have next element"


def test_next_with_selector(browser):
    element = browser.find("a", first_match=True)
    assert element, "Should find an anchor element"
    next_element = browser.next(element, "a")
    assert next_element, "Should have next anchor element"


def test_prev(browser):
    element = browser.find("a.nav-link", first_match=False)
    assert element, "Should find an anchor element"
    prev_element = browser.prev(element)
    assert prev_element, "Should have previous element"


def test_prev_with_selector(browser):
    element = browser.find("a.nav-link", first_match=False)
    assert element, "Should find an anchor element"
    prev_element = browser.prev(element, "a")
    assert prev_element, "Should have previous anchor element"


def test_is_visible(browser):
    element = browser.find("p:not(.hidden)", first_match=True)
    assert element, "Should find a visible paragraph"
    assert browser.is_visible(element), "Element should be visible"


def test_is_checked(browser):
    element = browser.find("#remember", first_match=True)
    assert element, "Should find checkbox element"
    assert browser.is_checked(element), "Checkbox should be checked"


def test_is_disabled(browser):
    element = browser.find("button[type='submit']", first_match=True)
    assert element, "Should find submit button"
    assert browser.is_disabled(element), "Button should be disabled"
