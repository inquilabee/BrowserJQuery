import contextlib
import functools
import time
from collections.abc import Callable
from typing import Any, Generic, TypeVar, Union

from selenium import webdriver
from selenium.webdriver.remote import webelement

from browserjquery import jquery_scripts, settings

logger = settings.getLogger(__name__)

T = TypeVar("T", bound=Union[webelement.WebElement, str])
ResultType = Union[list[T], T, None]
WrappedResultType = Union["BrowserJQueryCollection", "BrowserJQuery", str, None]


class BrowserJQueryCollection(Generic[T]):
    """A collection of elements that can be filtered and transformed."""

    def __init__(self, driver: webdriver.Chrome | webdriver.Firefox, elements: list[T]):
        """Initialize a collection of elements.

        Args:
            driver: The webdriver instance.
            elements: List of elements in the collection.
        """
        self.driver = driver
        self.elements = elements

    def __len__(self) -> int:
        """Get the number of elements in the collection."""
        return len(self.elements)

    def __iter__(self):
        """Iterate over the elements in the collection."""
        for element in self.elements:
            if isinstance(element, str):
                yield element
            else:
                yield BrowserJQuery(self.driver, default_element=element)

    def __getitem__(self, index: int) -> Union["BrowserJQuery", str]:
        """Get an element by index."""
        element = self.elements[index]
        if isinstance(element, str):
            return element
        return BrowserJQuery(self.driver, default_element=element)

    def first(self) -> Union["BrowserJQuery", str, None]:
        """Get the first element in the collection.

        Returns:
            A BrowserJQuery instance wrapping the first element, or None if empty.
        """
        if not self.elements:
            return None
        element = self.elements[0]
        if isinstance(element, str):
            return element
        return BrowserJQuery(self.driver, default_element=element)

    def last(self) -> Union["BrowserJQuery", str, None]:
        """Get the last element in the collection.

        Returns:
            A BrowserJQuery instance wrapping the last element, or None if empty.
        """
        if not self.elements:
            return None
        element = self.elements[-1]
        if isinstance(element, str):
            return element
        return BrowserJQuery(self.driver, default_element=element)

    def items(self) -> list[Union["BrowserJQuery", str]]:
        """Get all elements in the collection.

        Returns:
            List of elements wrapped in BrowserJQuery instances.
        """
        return [BrowserJQuery(self.driver, default_element=e) if not isinstance(e, str) else e for e in self.elements]


def prepare_result(func: Callable[..., ResultType]) -> Callable[..., WrappedResultType]:
    """Decorator to prepare query results.
    If result is a WebElement or list of WebElements, wraps it appropriately.
    Text elements are left as is.

    Args:
        func: The function to decorate.

    Returns:
        The decorated function that processes its result.
    """

    @functools.wraps(func)
    def wrapper(self: "BrowserJQuery", *args: Any, **kwargs: Any) -> WrappedResultType:
        result = func(self, *args, **kwargs)

        if isinstance(result, list):
            return BrowserJQueryCollection(self.driver, result)

        if result is not None and not isinstance(result, str):
            return BrowserJQuery(self.driver, default_element=result)

        return result

    return wrapper


class BrowserJQuery:
    """Main class for jQuery-based browser interactions."""

    def __init__(self, driver: webdriver.Chrome | webdriver.Firefox, default_element=None):
        """Initialize BrowserJQuery with a webdriver instance.

        Args:
            driver: A Chrome or Firefox webdriver instance.
        """
        self.driver = driver
        self.ensure_jquery()
        self.default_element = default_element or self.document

    def __call__(self, *args, **kwargs):
        """Allow the class instance to be called directly, equivalent to find().

        Returns:
            The result of find() with the provided arguments.
        """
        return self.find(*args, **kwargs)

    def __getattr__(self, name: str):
        """Redirect attribute access to the default element if not found in this class.

        Args:
            name: Name of the attribute to get.

        Returns:
            The attribute from the default element.

        Raises:
            AttributeError: If the attribute is not found in either this class or the default element.
        """
        if self.default_element is None:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

        # Try to get the attribute from the default element
        try:
            attr = getattr(self.default_element, name)
            # If it's a method, wrap it to maintain the BrowserJQuery context
            if callable(attr):

                def wrapper(*args, **kwargs):
                    result = attr(*args, **kwargs)
                    # If the result is a WebElement, wrap it in a new BrowserJQuery instance
                    if hasattr(result, "tag_name"):  # Check if it's a WebElement
                        return BrowserJQuery(self.driver, default_element=result)
                    # If the result is a list of WebElements, wrap each element
                    elif isinstance(result, list) and result and hasattr(result[0], "tag_name"):
                        return [BrowserJQuery(self.driver, default_element=item) for item in result]
                    return result

                return wrapper
            return attr
        except AttributeError:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    # Core/Initialization methods
    def ensure_jquery(self):
        """Ensures that jQuery is injected into the page.

        Returns:
            bool: True if jQuery is successfully injected, False otherwise.
        """
        if not self.is_jquery_injected:
            self.inject_jquery()

    def inject_jquery(self, by: str = "file", wait: int = 5) -> bool:
        """Inject jQuery into the current page.

        Args:
            by: Method of injection, either "file" or "cdn".
            wait: Time to wait after injection in seconds.

        Returns:
            bool: True if jQuery was successfully injected, False otherwise.
        """
        logger.info("Jquery being injected.")
        self._inject_jquery_file(wait=wait) if by == "file" else self._inject_jquery_cdn(wait=wait)
        return self.is_jquery_injected

    def _inject_jquery_cdn(self, wait: int = 2):
        """Inject jQuery from CDN.

        Args:
            wait: Time to wait after injection in seconds.
        """
        self.driver.execute_script(jquery_scripts.JQUERY_INJECTION)
        time.sleep(wait)

    def _inject_jquery_file(self, wait: int = 5):
        """Inject jQuery from local file.

        Args:
            wait: Time to wait after injection in seconds.
        """
        with open(settings.JQUERY_INJECTION_FILE) as f:
            self.execute(f.read())
        time.sleep(wait)

    @property
    def is_jquery_injected(self) -> bool:
        """Check if jQuery is already injected into the page.

        Returns:
            bool: True if jQuery is present, False otherwise.
        """
        with contextlib.suppress(Exception):
            self.execute(jquery_scripts.JQUERY_INJECTION_CHECK)
            return True
        return False

    # Document/Page methods
    @property
    def document(self):
        """Get the document element wrapped in jQuery.

        Returns:
            The document element as a jQuery object.
        """
        return self.execute(jquery_scripts.DOCUMENT_QUERY)

    @property
    def page_html(self) -> str:
        """Get the complete HTML of the current page.

        Returns:
            str: The HTML content of the page.
        """
        return self.execute(jquery_scripts.PAGE_HTML)

    # Core execution methods
    def execute(self, script, *args, **kwargs):
        """Execute JavaScript on the page.

        Args:
            script: The JavaScript code to execute.
            *args: Additional arguments to pass to the script.

        Returns:
            The result of the JavaScript execution.
        """
        return self.driver.execute_script(script, *args, **kwargs)

    def query(self, script: str, element: webelement.WebElement | None = None, *args, **kwargs):
        """Execute jQuery script on an element.

        Args:
            script: The jQuery script to execute.
            element: The WebElement to execute the script on. If None, uses default_element.
            *args: Additional arguments to pass to the script.
            **kwargs: Additional keyword arguments.

        Returns:
            The result of the jQuery script execution.
        """
        element = element or self.default_element
        logger.info(f"Executing script : {script} on element: {element}")
        return self.execute(script, element, *args, **kwargs)

    # Element finding methods
    @prepare_result
    def find(self, selector: str) -> list[webelement.WebElement] | webelement.WebElement | None:
        """Find elements using jQuery selector.

        Args:
            selector: jQuery selector to find elements.

        Returns:
            A BrowserJQueryCollection of matching elements.
        """
        method = ".first()" if selector.startswith("#") else ""
        return self.query(
            script=jquery_scripts.FIND_ELEMENTS.format(selector=selector, method=method),
        )

    @prepare_result
    def find_closest_ancestor(self, selector: str) -> webelement.WebElement | None:
        """Find the closest ancestor matching the selector.

        Args:
            selector: jQuery selector to match ancestor.

        Returns:
            The closest matching ancestor WebElement or None if not found.
        """
        return self.query(script=jquery_scripts.GET_CLOSEST.format(selector=selector))

    # Element traversal methods
    def parent(self) -> webelement.WebElement:
        """Get the parent element.

        Returns:
            The parent WebElement.
        """
        return self.query(
            script=jquery_scripts.GET_PARENT,
        )

    def parents(self) -> list[webelement.WebElement]:
        """Get all parent elements.

        Returns:
            List of parent WebElements.
        """
        return self.query(
            script=jquery_scripts.GET_PARENTS,
        )

    def children(self, selector: str | None = None) -> list[webelement.WebElement]:
        """Get direct children of element.

        Args:
            selector: Optional selector to filter children.

        Returns:
            List of child WebElements.
        """
        script = jquery_scripts.GET_CHILDREN.format(selector=selector) if selector else jquery_scripts.GET_CHILDREN_ALL
        return self.query(
            script=script,
        )

    def siblings(self, selector: str | None = None) -> list[webelement.WebElement]:
        """Get sibling elements.

        Args:
            selector: Optional selector to filter siblings.

        Returns:
            List of sibling WebElements.
        """
        script = jquery_scripts.GET_SIBLINGS.format(selector=selector) if selector else jquery_scripts.GET_SIBLINGS_ALL
        return self.query(
            script=script,
        )

    @prepare_result
    def next(self, selector: str | None = None) -> webelement.WebElement | None:
        """Get next sibling element.

        Args:
            selector: Optional selector to filter next sibling.

        Returns:
            The next sibling WebElement or None if not found.
        """
        script = jquery_scripts.GET_NEXT.format(selector=selector) if selector else jquery_scripts.GET_NEXT_ALL
        return self.query(
            script=script,
        )

    @prepare_result
    def prev(self, selector: str | None = None) -> webelement.WebElement | None:
        """Get previous sibling element.

        Args:
            selector: Optional selector to filter previous sibling.

        Returns:
            The previous sibling WebElement or None if not found.
        """
        script = jquery_scripts.GET_PREV.format(selector=selector) if selector else jquery_scripts.GET_PREV_ALL
        return self.query(
            script=script,
        )

    def items(self) -> list[webelement.WebElement]:
        """Get all child elements of the default element.

        Returns:
            List of child WebElements.
        """
        return self.query(
            script=jquery_scripts.GET_CHILDREN_ALL,
        )

    @prepare_result
    def first(self) -> webelement.WebElement | None:
        """Get the first child element of the default element.

        Returns:
            The first child WebElement or None if no children exist.
        """
        return self.query(
            script=jquery_scripts.GET_FIRST,
        )

    @prepare_result
    def last(self) -> webelement.WebElement | None:
        """Get the last child element of the default element.

        Returns:
            The last child WebElement or None if no children exist.
        """
        return self.query(
            script=jquery_scripts.GET_LAST,
        )

    # Element state/attribute methods
    def has_class(self, class_name: str) -> bool:
        """Check if element has a specific class.

        Args:
            class_name: Class name to look for.

        Returns:
            bool: True if element has the class, False otherwise.
        """
        return self.query(
            script=jquery_scripts.HAS_CLASS.format(class_name=class_name),
        )

    def matches_selector(self, selector: str) -> bool:
        """Check if element matches a selector.

        Args:
            selector: jQuery selector to match against.

        Returns:
            bool: True if element matches selector, False otherwise.
        """
        return self.query(
            script=jquery_scripts.MATCHES_SELECTOR.format(selector=selector),
        )

    def has(self, selector: str) -> bool:
        """Check if element has descendants matching selector.

        Args:
            selector: jQuery selector to match descendants.

        Returns:
            bool: True if element has matching descendants, False otherwise.
        """
        return self.query(
            script=jquery_scripts.HAS_DESCENDANTS.format(selector=selector),
        )

    def attr(self, attribute_name: str) -> str | None:
        """Get attribute value of element.

        Args:
            attribute_name: Name of the attribute.

        Returns:
            The attribute value or None if not found.
        """
        return self.query(
            script=jquery_scripts.GET_ATTR.format(attribute_name=attribute_name),
        )

    def text(self) -> str:
        """Get text content of element.

        Returns:
            The text content of the element.
        """
        return self.query(
            script=jquery_scripts.GET_TEXT,
        )

    def html(self) -> str:
        """Get HTML content of element.

        Returns:
            The HTML content of the element.
        """
        return self.query(
            script=jquery_scripts.GET_HTML,
        )

    def is_visible(self) -> bool:
        """Check if element is visible.

        Returns:
            bool: True if element is visible, False otherwise.
        """
        return self.query(
            script=jquery_scripts.IS_VISIBLE,
        )

    def is_checked(self) -> bool:
        """Check if checkbox/radio is checked.

        Returns:
            bool: True if element is checked, False otherwise.
        """
        return self.query(
            script=jquery_scripts.IS_CHECKED,
        )

    def is_disabled(self) -> bool:
        """Check if element is disabled.

        Returns:
            bool: True if element is disabled, False otherwise.
        """
        return self.query(
            script=jquery_scripts.IS_DISABLED,
        )

    # Text-based search methods
    @prepare_result
    def find_elements_with_text(
        self, text: str, selector: str = "*"
    ) -> list[webelement.WebElement] | webelement.WebElement | None:
        """Find elements containing specific text.

        Args:
            text: Text to search for.
            selector: jQuery selector to filter elements.

        Returns:
            A BrowserJQueryCollection of matching elements.
        """
        script = jquery_scripts.FIND_ELEMENTS_WITH_TEXT.format(selector=selector, text=text, method="")
        return self.query(script=script)

    @prepare_result
    def find_lowest_element_with_text(
        self, text: str, selector: str = "*", *, exact_match: bool = False
    ) -> webelement.WebElement | None:
        """Find the lowest element in the DOM tree containing specific text.

        Args:
            text: Text to search for.
            selector: jQuery selector to filter elements.
            exact_match: Whether to require an exact text match.

        Returns:
            The lowest matching WebElement or None if not found.
        """
        script = (
            jquery_scripts.FIND_LOWEST_ELEMENT_WITH_EXACT_TEXT
            if exact_match
            else jquery_scripts.FIND_LOWEST_ELEMENT_WITH_TEXT
        ).format(selector=selector, text=text)

        return self.query(script=script)

    @prepare_result
    def find_elements_with_selector_and_text(
        self,
        selector: str,
        text: str,
        *,
        exact_match: bool = False,
    ) -> list[webelement.WebElement] | webelement.WebElement | None:
        """Find elements matching both selector and text criteria.

        Args:
            selector: jQuery selector to filter elements.
            text: Text to search for.
            exact_match: Whether to require an exact text match.

        Returns:
            A BrowserJQueryCollection of matching elements.
        """
        script = (
            jquery_scripts.FIND_ELEMENTS_WITH_SELECTOR_AND_EXACT_TEXT
            if exact_match
            else jquery_scripts.FIND_ELEMENTS_WITH_SELECTOR_AND_TEXT
        ).format(selector=selector, text=text, method="")

        return self.query(script=script)
