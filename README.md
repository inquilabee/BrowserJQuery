# BrowserJQuery

A Python library that seamlessly integrates jQuery functionality with Selenium WebDriver. This library provides a convenient and powerful way to interact with web elements using jQuery selectors and methods in your Selenium tests, making web automation more intuitive and efficient.

## Features

- Use jQuery selectors to find elements
- Chain jQuery methods for complex element interactions
- Built-in support for common jQuery operations
- Type-safe implementation with mypy support
- Comprehensive test coverage

## Installation

```bash
pip install browserjquery
```

For development, install with test dependencies:

```bash
pip install "browserjquery[dev]"
```

## Quick Start

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

## Advanced Usage

### Chaining Methods

```python
# Chain multiple jQuery operations
result = jquery.find("div.item").filter(".active").find("span").text()
```

### Working with Forms

```python
# Fill form fields
jquery.find("input[name='username']").val("testuser")
jquery.find("input[name='password']").val("password123")

# Submit form
jquery.find("form").submit()
```

### Event Handling

```python
# Attach event handlers
jquery.find("button").on("click", "alert('clicked!')")
```

## Contributing

Contributions are welcome! Feel free to submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
