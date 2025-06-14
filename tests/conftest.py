import logging
import os
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from browserjquery import BrowserJQuery

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def driver():
    """Create a Chrome WebDriver instance."""
    logger.debug("Setting up Chrome WebDriver")
    options = Options()
    # options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    logger.debug("Chrome WebDriver created successfully")
    yield driver
    logger.debug("Quitting Chrome WebDriver")
    driver.quit()


@pytest.fixture(scope="session")
def test_page_path():
    """Get the path to the test HTML file."""
    path = str(Path(__file__).parent / "data" / "test_page.html")
    logger.debug(f"Test page path: {path}")
    assert os.path.exists(path), f"Test page not found at {path}"
    return path


@pytest.fixture(scope="session")
def browser(driver, test_page_path):
    """Create a BrowserJQuery instance with the test page loaded."""
    logger.debug("Creating BrowserJQuery instance")

    url = f"file:///{test_page_path}"

    logger.debug(f"Loading test page from: {url}")
    driver.get(url)

    # Verify page loaded
    current_url = driver.current_url
    logger.debug(f"Current URL: {current_url}")
    assert current_url.startswith("file://"), f"Page not loaded correctly. Current URL: {current_url}"

    browser = BrowserJQuery(driver)

    return browser
