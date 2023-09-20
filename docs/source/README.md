# BrowserJQuery: Streamline Selenium with jQuery

Enhance your Selenium-driven web automation tasks with **BrowserJQuery**, a Python package that empowers you to use jQuery effortlessly. This straightforward yet robust package simplifies the execution of jQuery scripts and includes built-in utility methods.

# Installation

Get started quickly by installing **BrowserJQuery** from PyPI:

```bash
pip install browserjquery
```

# Usage

Here's how you can harness the power of **BrowserJQuery** in your Selenium scripts:

```python
import time
from selenium.webdriver import Chrome
from browserjquery import BrowserJQuery

# Initialize a Selenium driver
driver = Chrome()

# Navigate to a website
driver.get("https://www.yahoo.com")

# Pause to allow page loading (you can adjust the duration)
time.sleep(10)

# Create a jQuery object for the driver
jquery = BrowserJQuery(driver)

# Execute a jQuery script
jquery.execute("""return $("div.stream-item")""")

# Use the jQuery object to find and select items
stream = jquery(".stream-item")

# Access methods and attributes of the jQuery object
print(jquery.document)

# Find elements within the selected items
print(jquery.find(".stream-item a"))

# Find elements with specific text
print(jquery.find_elements_with_text("Hello"))

# Find elements with specific text within a specific element
print(jquery.find_elements_with_text("Hello", element=stream[0]))

# Get the parent element of a selected item
print(jquery.parent(stream[0]))
```

With **BrowserJQuery**, you can effortlessly integrate jQuery into your Selenium workflows, making web automation more efficient and powerful.
