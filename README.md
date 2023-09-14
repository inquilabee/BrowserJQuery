# BrowserQuery

Use JQuery on selenium drivers.

A simple, yet powerful package to execute Jquery while working on selenium drivers. It also comes built in with some utility methods built in.


# Install

```bash
pip install browserjquery
```

# Usage

```python
    import time

    from selenium.webdriver import Chrome
    from browserjquery import BrowserJQuery

    driver = Chrome()

    driver.get("https://www.yahoo.com")

    time.sleep(10)

    # create Jquery object
    jquery = BrowserJQuery(driver)

    # execute script
    jquery.execute("""return $("div.stream-item")""")

    # call the object as a method to find/select items
    stream = jquery(".stream-item")

    # call methods/attributes off of the object
    print(jquery.document)

    print(jquery.find(".stream-item a"))

    print(jquery.find_elements_with_text("Hello"))
    print(jquery.find_elements_with_text("Hello", element=stream[0]))

    print(jquery.parent(stream[0]))
```
