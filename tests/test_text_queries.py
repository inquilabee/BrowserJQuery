from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_find_elements_with_text(browser):
    """Test finding elements containing specific text."""
    # Wait for the page to load
    wait = WebDriverWait(browser.driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    elements = browser.find_elements_with_text("Sign in")
    assert elements, "Should find elements containing 'Sign in' text"
    assert len(elements) > 0


def test_find_elements_with_text_first_match(browser):
    """Test finding first element containing specific text."""
    wait = WebDriverWait(browser.driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    element = browser.find_elements_with_text("Sign in", selector=".nav-link", first_match=True)
    assert element, "Should find first element containing 'Sign in' text"
    assert element.text == "Sign in"


def test_find_elements_with_text_no_matches(browser):
    """Test finding elements with non-existent text."""
    wait = WebDriverWait(browser.driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    elements = browser.find_elements_with_text("ThisTextShouldNotExist123")
    assert not elements, "Should not find any elements with non-existent text"


def test_find_lowest_element_with_text(browser):
    """Test finding lowest element containing specific text."""
    wait = WebDriverWait(browser.driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    element = browser.find_lowest_element_with_text("Sign in")
    assert element, "Should find lowest element containing 'Sign in' text"
    assert element.text == "Sign in"


def test_find_lowest_element_with_text_exact_match(browser):
    """Test finding lowest element with exact text match."""
    wait = WebDriverWait(browser.driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    element = browser.find_lowest_element_with_text("Sign in", exact_match=True)
    assert element, "Should find lowest element with exact 'Sign in' text"
    assert element.text == "Sign in"


def test_find_lowest_element_with_text_no_matches(browser):
    """Test finding lowest element with non-existent text."""
    wait = WebDriverWait(browser.driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    element = browser.find_lowest_element_with_text("ThisTextShouldNotExist123")
    assert element is None, "Should not find any element with non-existent text"


def test_find_elements_with_selector_and_text(browser):
    """Test finding elements matching selector and containing text."""
    wait = WebDriverWait(browser.driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    elements = browser.find_elements_with_selector_and_text("a", "Sign in")
    assert elements, "Should find anchor elements containing 'Sign in' text"
    assert len(elements) > 0


def test_find_elements_with_selector_and_text_exact_match(browser):
    """Test finding elements matching selector with exact text match."""
    wait = WebDriverWait(browser.driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    elements = browser.find_elements_with_selector_and_text("a", "Sign in", exact_match=True)
    assert elements, "Should find anchor elements with exact 'Sign in' text"
    assert len(elements) > 0


def test_find_elements_with_selector_and_text_first_match(browser):
    """Test finding first element matching selector and containing text."""
    wait = WebDriverWait(browser.driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    element = browser.find_elements_with_selector_and_text("a", "Sign in", first_match=True)
    assert element, "Should find first anchor element containing 'Sign in' text"
    assert element.text == "Sign in"


def test_find_elements_with_selector_and_text_no_matches(browser):
    """Test finding elements with non-existent selector and text combination."""
    wait = WebDriverWait(browser.driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    elements = browser.find_elements_with_selector_and_text("div", "ThisTextShouldNotExist123")
    assert not elements, "Should not find any elements with non-existent selector and text"
