# Installation Guide

This guide will help you install and set up BrowserJQuery for your project.

## Requirements

- Python 3.8 or higher
- Selenium WebDriver
- Chrome or Firefox browser

## Installation

### Using pip

```bash
pip install browserjquery
```

### Using Poetry

```bash
poetry add browserjquery
```

### From Source

1. Clone the repository:
```bash
git clone https://github.com/yourusername/browserjquery.git
cd browserjquery
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install the package:
```bash
pip install -e .
```

## Setting Up Selenium WebDriver

### Chrome WebDriver

1. Install Chrome browser if not already installed
2. Download ChromeDriver from [ChromeDriver Downloads](https://sites.google.com/chromium.org/driver/)
3. Add ChromeDriver to your system PATH

### Firefox WebDriver

1. Install Firefox browser if not already installed
2. Download geckodriver from [geckodriver Releases](https://github.com/mozilla/geckodriver/releases)
3. Add geckodriver to your system PATH

## Basic Setup

```python
from browserjquery import BrowserJQuery
from selenium import webdriver

# Initialize Chrome WebDriver
driver = webdriver.Chrome()
# Or Firefox
# driver = webdriver.Firefox()

# Create BrowserJQuery instance
browser = BrowserJQuery(driver)

# Navigate to a page
driver.get("https://example.com")

# Start using BrowserJQuery
elements = browser.find(".my-class")
```

## Configuration

### WebDriver Options

```python
from selenium.webdriver.chrome.options import Options

# Configure Chrome options
options = Options()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Initialize with options
driver = webdriver.Chrome(options=options)
browser = BrowserJQuery(driver)
```

### jQuery Injection

BrowserJQuery automatically injects jQuery into pages. You can control this behavior:

```python
# Check if jQuery is injected
if browser.is_jquery_injected:
    print("jQuery is available")

# Manually inject jQuery
browser.inject_jquery(by="file")  # From local file
browser.inject_jquery(by="cdn")   # From CDN
```

## Troubleshooting

### Common Issues

1. **WebDriver not found**
   - Ensure WebDriver is installed and in your system PATH
   - Try specifying the WebDriver path explicitly:
     ```python
     from selenium.webdriver.chrome.service import Service
     service = Service(path="/path/to/chromedriver")
     driver = webdriver.Chrome(service=service)
     ```

2. **jQuery injection fails**
   - Check if the page already has jQuery
   - Try using a different injection method (file vs CDN)
   - Ensure the page is fully loaded before injection

3. **Element not found**
   - Verify the selector syntax
   - Check if the element is in an iframe
   - Ensure the element is visible and loaded

### Getting Help

- Check the [API Reference](browserjquery.md) for detailed documentation
- Look at [Examples](examples.md) for usage patterns
- Open an issue on GitHub for bugs or feature requests 