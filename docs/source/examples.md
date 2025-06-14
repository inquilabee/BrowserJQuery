# Usage Examples

This page provides detailed examples of how to use BrowserJQuery for common browser automation tasks.

## Basic Element Selection

### Finding Elements by Selector

```python
# Find all elements with a specific class
elements = browser.find(".my-class")

# Find elements with multiple classes
elements = browser.find(".class1.class2")

# Find elements by ID
element = browser.find("#my-id")

# Find elements by tag name
divs = browser.find("div")

# Find elements by attribute
elements = browser.find("[data-test='value']")
```

### Finding Elements by Text

```python
# Find elements containing specific text
elements = browser.find_elements_with_text("Click me")

# Find elements with exact text match
element = browser.find_lowest_element_with_text("Submit", exact_match=True)

# Find elements matching both selector and text
elements = browser.find_elements_with_selector_and_text(
    selector="button",
    text="Submit",
    exact_match=True
)
```

## Element Traversal

### Parent and Child Navigation

```python
# Get parent element
parent = element.parent()

# Get all parents
parents = element.parents()

# Get direct children
children = element.children()

# Get children matching selector
matching_children = element.children(".active")

# Get all descendants
all_descendants = element.find("*")
```

### Sibling Navigation

```python
# Get next sibling
next_sibling = element.next()

# Get next sibling matching selector
next_button = element.next("button")

# Get previous sibling
prev_sibling = element.prev()

# Get all siblings
siblings = element.siblings()

# Get siblings matching selector
active_siblings = element.siblings(".active")
```

## Element State and Properties

### Checking Element State

```python
# Check visibility
if element.is_visible():
    print("Element is visible")

# Check if element has class
if element.has_class("active"):
    print("Element is active")

# Check if element matches selector
if element.matches_selector(".my-class"):
    print("Element matches selector")

# Check if element has matching descendants
if element.has(".child-class"):
    print("Element has matching children")
```

### Working with Form Elements

```python
# Check if checkbox is checked
if checkbox.is_checked():
    print("Checkbox is checked")

# Check if element is disabled
if button.is_disabled():
    print("Button is disabled")
```

### Getting Element Properties

```python
# Get text content
text = element.text()

# Get HTML content
html = element.html()

# Get attribute value
href = element.attr("href")
data_value = element.attr("data-test")

# Get multiple attributes
attributes = {
    "href": element.attr("href"),
    "class": element.attr("class"),
    "id": element.attr("id")
}
```

## Working with Collections

### Collection Operations

```python
# Get number of elements
count = len(elements)

# Iterate over elements
for element in elements:
    print(element.text())

# Get element by index
first = elements[0]
last = elements[-1]

# Get first and last elements
first = elements.first()
last = elements.last()

# Get all elements as list
element_list = elements.items()
```

### Filtering Collections

```python
# Filter elements by text
matching_elements = [
    element for element in elements
    if element.text() == "Expected Text"
]

# Filter elements by attribute
matching_elements = [
    element for element in elements
    if element.attr("data-test") == "value"
]
```

## jQuery Integration

### Managing jQuery Injection

```python
# Check if jQuery is available
if browser.is_jquery_injected:
    print("jQuery is available")

# Manually inject jQuery
browser.inject_jquery(by="file")  # From local file
browser.inject_jquery(by="cdn")   # From CDN

# Wait for jQuery to be ready
time.sleep(2)  # After injection
```

### Custom jQuery Scripts

```python
# Execute custom jQuery script
result = browser.execute("""
    return $(arguments[0]).find('.child').map(function() {
        return $(this).text();
    }).get();
""", element)
``` 