# BrowserJQuery

A Python library for using jQuery with Selenium WebDriver. This library provides a convenient way to interact with web elements using jQuery selectors and methods in your Selenium tests.

## Installation

```bash
pip install browserjquery
```

For development, install with test dependencies:

```bash
pip install "browserjquery[dev]"
```

## Usage

```python
from selenium import webdriver
from browserjquery import BrowserJQuery

# Initialize the WebDriver
driver = webdriver.Chrome()

# Create a BrowserJQuery instance
jquery = BrowserJQuery(driver)

# Navigate to a page
driver.get("https://example.com")

# Find elements using jQuery selectors
elements = jquery.find("div.test-class")
first_element = jquery.find("div.test-class", first_match=True)

# Find elements containing specific text
elements_with_text = jquery.find_elements_with_text("Hello World")

# Check if an element has a specific class
has_class = jquery.has_class(element, "active")

# Get parent elements
parent = jquery.parent(element)
all_parents = jquery.parents(element)

# Find closest ancestor with specific selector
closest = jquery.find_closest_ancestor("div.container", element)
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=browserjquery

# Run specific test file
pytest tests/test_jquery.py
```

### Code Style

The project uses:
- Black for code formatting
- isort for import sorting
- mypy for type checking

To format code:

```bash
black .
isort .
```

To check types:

```bash
mypy .
```

## License

MIT License
