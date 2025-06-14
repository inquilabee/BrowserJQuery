from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_has_class(browser):
    """Test if an element has a specific class."""
    # Wait for the container element to be present
    wait = WebDriverWait(browser.driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "container")))

    # Find the element using BrowserJQuery
    element = browser.find("#container").first()
    assert element, "Should find container element"

    # Test the class
    assert element.has_class("test-class"), "Should have the expected class"


def test_matches_selector(browser):
    element = browser.find("a").first()
    assert element, "Should find an anchor element"
    assert element.matches_selector("a"), "Should match anchor selector"


def test_has_descendants(browser):
    element = browser.find("body").first()
    assert element, "Should find body element"
    assert element.has("a"), "Should have anchor descendants"


def test_attr(browser):
    element = browser.find("a").first()
    assert element, "Should find an anchor element"
    href = element.attr("href")
    assert href == "#", "Href should be #"


def test_text(browser):
    element = browser.find("a").first()
    assert element, "Should find an anchor element"
    text = element.text()
    assert text == "Sign in", "Should have correct text content"


def test_html(browser):
    element = browser.find("body").first()
    assert element, "Should find body element"
    html = element.html()
    assert html, "Should have HTML content"
    assert "<" in html, "HTML should contain tags"


def test_children(browser):
    element = browser.find("body").first()
    assert element, "Should find body element"
    children = element.children()
    assert children, "Should have children"
    assert len(children) > 0, "Should have at least one child"


def test_children_with_selector(browser):
    element = browser.find("nav").first()
    assert element, "Should find nav element"
    children = element.children("a")
    assert children, "Should have anchor children"
    assert len(children) > 0, "Should have at least one anchor child"


def test_siblings(browser):
    element = browser.find("a").first()
    assert element, "Should find an anchor element"
    siblings = element.siblings()
    assert siblings, "Should have siblings"
    assert len(siblings) > 0, "Should have at least one sibling"


def test_siblings_with_selector(browser):
    element = browser.find("a").first()
    assert element, "Should find an anchor element"
    siblings = element.siblings("a")
    assert siblings, "Should have sibling anchors"
    assert len(siblings) > 0, "Should have at least one sibling anchor"


def test_next(browser):
    element = browser.find("a").first()
    assert element, "Should find an anchor element"
    next_element = element.next()
    assert next_element, "Should have next element"
    assert next_element.text() == "Home", "Next element should be 'Home'"


def test_next_with_selector(browser):
    element = browser.find("a").first()
    assert element, "Should find an anchor element"
    next_element = element.next("a")
    assert next_element, "Should have next anchor element"
    assert next_element.text() == "Home", "Next element should be 'Home'"


def test_prev(browser):
    element = browser.find("a.nav-link:nth-child(2)").first()  # Second nav link
    assert element, "Should find an anchor element"
    prev_element = element.prev()
    assert prev_element, "Should have previous element"
    assert prev_element.text() == "Sign in", "Previous element should be 'Sign in'"


def test_prev_with_selector(browser):
    element = browser.find("a.nav-link:nth-child(2)").first()  # Second nav link
    assert element, "Should find an anchor element"
    prev_element = element.prev("a")
    assert prev_element, "Should have previous anchor element"
    assert prev_element.text() == "Sign in", "Previous element should be 'Sign in'"


def test_is_visible(browser):
    element = browser.find("p:not(.hidden)").first()
    assert element, "Should find a visible paragraph"
    assert element.is_visible(), "Element should be visible"


def test_is_checked(browser):
    element = browser.find("#remember").first()
    assert element, "Should find checkbox element"
    assert element.is_checked(), "Checkbox should be checked"


def test_is_disabled(browser):
    element = browser.find("button[type='submit']").first()
    assert element, "Should find submit button"
    assert element.is_disabled(), "Button should be disabled"
