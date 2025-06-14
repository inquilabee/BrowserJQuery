# BrowserJQuery API Documentation

## Overview

BrowserJQuery is a Python library that provides jQuery-like functionality for browser automation using Selenium WebDriver. It allows you to interact with web elements using familiar jQuery-style selectors and methods.

## Core Classes

### BrowserJQuery

The main class for jQuery-based browser interactions.

#### Initialization

```python
from browserjquery import BrowserJQuery
from selenium import webdriver

driver = webdriver.Chrome()  # or Firefox
browser = BrowserJQuery(driver)
```

#### Core Methods

##### Element Finding

- `find(selector: str) -> BrowserJQueryCollection`: Find elements using jQuery selector
- `find_elements_with_text(text: str, selector: str = "*") -> BrowserJQueryCollection`: Find elements containing specific text
- `find_lowest_element_with_text(text: str, selector: str = "*", exact_match: bool = False) -> BrowserJQuery`: Find the lowest element containing text
- `find_elements_with_selector_and_text(selector: str, text: str, exact_match: bool = False) -> BrowserJQueryCollection`: Find elements matching both selector and text

##### Element Traversal

- `parent() -> BrowserJQuery`: Get the parent element
- `parents() -> list[BrowserJQuery]`: Get all parent elements
- `children(selector: str | None = None) -> list[BrowserJQuery]`: Get direct children
- `siblings(selector: str | None = None) -> list[BrowserJQuery]`: Get sibling elements
- `next(selector: str | None = None) -> BrowserJQuery`: Get next sibling
- `prev(selector: str | None = None) -> BrowserJQuery`: Get previous sibling

##### Element State

- `has_class(class_name: str) -> bool`: Check if element has a class
- `matches_selector(selector: str) -> bool`: Check if element matches selector
- `has(selector: str) -> bool`: Check if element has matching descendants
- `is_visible() -> bool`: Check if element is visible
- `is_checked() -> bool`: Check if checkbox/radio is checked
- `is_disabled() -> bool`: Check if element is disabled

##### Element Properties

- `attr(attribute_name: str) -> str | None`: Get attribute value
- `text() -> str`: Get text content
- `html() -> str`: Get HTML content

### BrowserJQueryCollection

A collection of elements that can be filtered and transformed.

#### Methods

- `__len__() -> int`: Get number of elements
- `__iter__()`: Iterate over elements
- `__getitem__(index: int) -> BrowserJQuery`: Get element by index
- `first() -> BrowserJQuery`: Get first element
- `last() -> BrowserJQuery`: Get last element
- `items() -> list[BrowserJQuery]`: Get all elements

## Usage Examples

### Basic Element Selection

```python
# Find elements by selector
elements = browser.find(".my-class")
first_element = elements.first()

# Find elements with specific text
elements_with_text = browser.find_elements_with_text("Click me")
```

### Element Traversal

```python
# Get parent element
parent = element.parent()

# Get all children
children = element.children()

# Get siblings
siblings = element.siblings()
```

### Element State Checking

```python
# Check element state
if element.is_visible():
    if element.has_class("active"):
        print(element.text())
```

### Attribute Access

```python
# Get element attributes
href = element.attr("href")
text = element.text()
html = element.html()
```

## jQuery Integration

The library automatically injects jQuery into the page if it's not already present. You can control this behavior:

```python
# Check if jQuery is injected
if browser.is_jquery_injected:
    print("jQuery is available")

# Manually inject jQuery
browser.inject_jquery(by="file")  # or "cdn"
```

```{eval-rst}
.. automodule:: browserjquery.jquery
   :members:
   :undoc-members:
   :show-inheritance:
```
