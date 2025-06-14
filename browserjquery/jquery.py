import contextlib
import time

from selenium import webdriver
from selenium.webdriver.remote import webelement

from browserjquery import jquery_scripts, settings
from browserjquery.text_queries import TextQuery

logger = settings.getLogger(__name__)


class BrowserJQuery(TextQuery):
    """Main class for jQuery-based browser interactions."""

    def __init__(self, driver: webdriver.Chrome | webdriver.Firefox):
        """Initialize BrowserJQuery with a webdriver instance.

        Args:
            driver: A Chrome or Firefox webdriver instance.
        """
        self.driver = driver
        self.ensure_jquery()

    def __call__(self, *args, **kwargs):
        """Allow the class instance to be called directly, equivalent to find().

        Returns:
            The result of find() with the provided arguments.
        """
        return self.find(*args, **kwargs)

    def ensure_jquery(self):
        """Ensures that jQuery is injected into the page.

        Returns:
            bool: True if jQuery is successfully injected, False otherwise.
        """
        if not self.is_jquery_injected:
            self.inject_jquery()

    def execute(self, script, *args):
        """Execute JavaScript on the page.

        Args:
            script: The JavaScript code to execute.
            *args: Additional arguments to pass to the script.

        Returns:
            The result of the JavaScript execution.
        """
        return self.driver.execute_script(script, *args)

    def query(self, script: str, element: webelement.WebElement, *args):
        """Execute jQuery script on a specific element.

        Args:
            script: The jQuery script to execute.
            element: The WebElement to execute the script on.
            *args: Additional arguments to pass to the script.

        Returns:
            The result of the jQuery script execution.
        """
        logger.info(f"Executing script : {script} on element: {element}")
        return self.execute(script, element, *args)

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

    @staticmethod
    def _prepare_result(  # type: ignore
        result: list[webelement.WebElement] | webelement.WebElement | None, first: bool
    ) -> list[webelement.WebElement] | webelement.WebElement | None:
        """Prepare the result based on whether first match is requested.

        Args:
            result: The query result to process.
            first: Whether to return only the first match.

        Returns:
            The processed result, either a single element or a list of elements.
        """
        if isinstance(result, list):
            if first:
                return result[0] if result else None
            return result
        return result

    def find(
        self, selector: str, element: webelement.WebElement | None = None, *, first_match: bool = False
    ) -> list[webelement.WebElement] | webelement.WebElement | None:
        """Find elements using jQuery selector.

        Args:
            selector: jQuery selector to find elements.
            element: Optional element to search within. If None, searches entire document.
            first_match: Whether to return only the first match.

        Returns:
            Either a single WebElement, a list of WebElements, or None if no matches found.
        """
        first_match = first_match or selector.startswith("#")
        element = element or self.document
        if element is None:
            return None
        method = ".first()" if first_match else ""

        return self._prepare_result(
            self.query(
                script=jquery_scripts.FIND_ELEMENTS.format(selector=selector, method=method),
                element=element,
            ),
            first=first_match,
        )

    def find_closest_ancestor(self, selector: str, element: webelement.WebElement) -> webelement.WebElement | None:
        """Find the closest ancestor matching the selector.

        Args:
            selector: jQuery selector to match ancestor.
            element: Element to start search from.

        Returns:
            The closest matching ancestor WebElement or None if not found.
        """
        result = self._prepare_result(
            self.query(script=jquery_scripts.GET_CLOSEST.format(selector=selector), element=element), first=True
        )
        if isinstance(result, list):
            return result[0] if result else None
        return result

    def has_class(self, element: webelement.WebElement, class_name: str) -> bool:
        """Check if element has a specific class.

        Args:
            element: Element to check.
            class_name: Class name to look for.

        Returns:
            bool: True if element has the class, False otherwise.
        """
        return self.query(
            script=jquery_scripts.HAS_CLASS.format(class_name=class_name),
            element=element,
        )

    def parent(self, element: webelement.WebElement) -> webelement.WebElement:
        """Get the parent element.

        Args:
            element: Element to get parent of.

        Returns:
            The parent WebElement.
        """
        return self.query(
            script=jquery_scripts.GET_PARENT,
            element=element,
        )

    def parents(self, element: webelement.WebElement) -> list[webelement.WebElement]:
        """Get all parent elements.

        Args:
            element: Element to get parents of.

        Returns:
            List of parent WebElements.
        """
        return self.query(
            script=jquery_scripts.GET_PARENTS,
            element=element,
        )

    def matches_selector(self, element: webelement.WebElement, selector: str) -> bool:
        """Check if element matches a selector.

        Args:
            element: Element to check.
            selector: jQuery selector to match against.

        Returns:
            bool: True if element matches selector, False otherwise.
        """
        return self.query(
            script=jquery_scripts.MATCHES_SELECTOR.format(selector=selector),
            element=element,
        )

    def has(self, element: webelement.WebElement, selector: str) -> bool:
        """Check if element has descendants matching selector.

        Args:
            element: Element to check.
            selector: jQuery selector to match descendants.

        Returns:
            bool: True if element has matching descendants, False otherwise.
        """
        return self.query(
            script=jquery_scripts.HAS_DESCENDANTS.format(selector=selector),
            element=element,
        )

    def attr(self, element: webelement.WebElement, attribute_name: str) -> str | None:
        """Get attribute value of element.

        Args:
            element: Element to get attribute from.
            attribute_name: Name of the attribute.

        Returns:
            The attribute value or None if not found.
        """
        return self.query(
            script=jquery_scripts.GET_ATTR.format(attribute_name=attribute_name),
            element=element,
        )

    def text(self, element: webelement.WebElement) -> str:
        """Get text content of element.

        Args:
            element: Element to get text from.

        Returns:
            The text content of the element.
        """
        return self.query(
            script=jquery_scripts.GET_TEXT,
            element=element,
        )

    def html(self, element: webelement.WebElement) -> str:
        """Get HTML content of element.

        Args:
            element: Element to get HTML from.

        Returns:
            The HTML content of the element.
        """
        return self.query(
            script=jquery_scripts.GET_HTML,
            element=element,
        )

    def children(self, element: webelement.WebElement, selector: str | None = None) -> list[webelement.WebElement]:
        """Get direct children of element.

        Args:
            element: Element to get children from.
            selector: Optional selector to filter children.

        Returns:
            List of child WebElements.
        """
        script = jquery_scripts.GET_CHILDREN.format(selector=selector) if selector else jquery_scripts.GET_CHILDREN_ALL
        return self.query(
            script=script,
            element=element,
        )

    def siblings(self, element: webelement.WebElement, selector: str | None = None) -> list[webelement.WebElement]:
        """Get sibling elements.

        Args:
            element: Element to get siblings of.
            selector: Optional selector to filter siblings.

        Returns:
            List of sibling WebElements.
        """
        script = jquery_scripts.GET_SIBLINGS.format(selector=selector) if selector else jquery_scripts.GET_SIBLINGS_ALL
        return self.query(
            script=script,
            element=element,
        )

    def next(
        self, element: webelement.WebElement, selector: str | None = None
    ) -> list[webelement.WebElement] | webelement.WebElement | None:
        """Get next sibling element.

        Args:
            element: Element to get next sibling of.
            selector: Optional selector to filter next sibling.

        Returns:
            Either a single WebElement, a list of WebElements, or None if not found.
        """
        script = jquery_scripts.GET_NEXT.format(selector=selector) if selector else jquery_scripts.GET_NEXT_ALL
        return self._prepare_result(
            self.query(
                script=script,
                element=element,
            ),
            first=True,
        )

    def prev(
        self, element: webelement.WebElement, selector: str | None = None
    ) -> list[webelement.WebElement] | webelement.WebElement | None:
        """Get previous sibling element.

        Args:
            element: Element to get previous sibling of.
            selector: Optional selector to filter previous sibling.

        Returns:
            Either a single WebElement, a list of WebElements, or None if not found.
        """
        script = jquery_scripts.GET_PREV.format(selector=selector) if selector else jquery_scripts.GET_PREV_ALL
        return self._prepare_result(
            self.query(
                script=script,
                element=element,
            ),
            first=True,
        )

    def is_visible(self, element: webelement.WebElement) -> bool:
        """Check if element is visible.

        Args:
            element: Element to check.

        Returns:
            bool: True if element is visible, False otherwise.
        """
        return self.query(
            script=jquery_scripts.IS_VISIBLE,
            element=element,
        )

    def is_checked(self, element: webelement.WebElement) -> bool:
        """Check if checkbox/radio is checked.

        Args:
            element: Element to check.

        Returns:
            bool: True if element is checked, False otherwise.
        """
        return self.query(
            script=jquery_scripts.IS_CHECKED,
            element=element,
        )

    def is_disabled(self, element: webelement.WebElement) -> bool:
        """Check if element is disabled.

        Args:
            element: Element to check.

        Returns:
            bool: True if element is disabled, False otherwise.
        """
        return self.query(
            script=jquery_scripts.IS_DISABLED,
            element=element,
        )
