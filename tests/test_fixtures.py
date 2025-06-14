from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_fixtures(browser):
    """Test that fixtures are working correctly."""
    # Wait for page to load
    wait = WebDriverWait(browser.driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Verify we can find elements
    container = browser.find("#container")
    assert container, "Should find container element"

    # Verify jQuery is working
    assert browser.has_class(container, "test-class"), "Should have test-class"
