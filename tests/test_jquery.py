def test_document_property(browser):
    doc = browser.document
    assert doc is not None, "Should get document element"


def test_page_html_property(browser):
    html = browser.page_html
    assert html is not None and "<html" in html, "Should get page HTML"


def test_find_with_selector(browser):
    element = browser.find("a.nav-link").first()
    assert element is not None, "Should find anchor with nav-link class"


def test_find_with_first_match(browser):
    element = browser.find("a.nav-link").first()
    assert element is not None, "Should find first anchor with nav-link class"
    assert element.text() == "Sign in", "First nav-link should be 'Sign in'"


def test_find_elements_with_text(browser):
    elements = browser.find_elements_with_text("Sign in")
    assert elements, "Should find elements containing 'Sign in'"
    assert any(e.text() == "Sign in" for e in elements.items()), "At least one should have text 'Sign in'"


def test_find_closest_ancestor(browser):
    element = browser.find("a.nav-link").first()
    ancestor = element.find_closest_ancestor("nav")
    assert ancestor is not None, "Should find nav ancestor"


def test_has_class(browser):
    element = browser.find("#container").first()
    assert element.has_class("test-class"), "Should have test-class"


def test_parent(browser):
    element = browser.find("a.nav-link").first()
    parent = element.parent()
    assert parent is not None, "Should have parent element"


def test_parents(browser):
    element = browser.find("a.nav-link").first()
    parents = element.parents()
    assert parents, "Should have ancestor elements"
