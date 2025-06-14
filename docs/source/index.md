% BrowserJQuery documentation master file, created by
% sphinx-quickstart on Wed Sep 20 01:03:18 2023.
% You can adapt this file completely to your liking, but it should at least
% contain the root `toctree` directive.

# BrowserJQuery Documentation

Welcome to the BrowserJQuery documentation! This library provides jQuery-like functionality for browser automation using Selenium WebDriver.

## Quick Start

```python
from browserjquery import BrowserJQuery
from selenium import webdriver

# Initialize the browser
driver = webdriver.Chrome()  # or Firefox
browser = BrowserJQuery(driver)

# Navigate to a page
driver.get("https://example.com")

# Find elements using jQuery selectors
elements = browser.find(".my-class")
first_element = elements.first()

# Get element properties
text = first_element.text()
href = first_element.attr("href")
```

## Features

- jQuery-style element selection and traversal
- Automatic jQuery injection
- Text-based element finding
- Element state checking
- Attribute and content access
- Collection operations

## Documentation Sections

- [API Reference](browserjquery.md) - Detailed API documentation
- [Examples](examples.md) - Usage examples and common patterns
- [Installation](installation.md) - Installation and setup guide
- [Contributing](contributing.md) - How to contribute to the project

## Requirements

- Python 3.8+
- Selenium WebDriver
- Chrome or Firefox browser

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

```{toctree}
:caption: 'Contents:'
:maxdepth: 2

README.md
browserjquery.md
```

# Indices and tables

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`
