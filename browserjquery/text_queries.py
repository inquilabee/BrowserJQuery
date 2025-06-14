from selenium import webdriver
from selenium.webdriver.remote import webelement

from browserjquery import jquery_scripts


class TextQuery:
    """Mixin class providing text-based query methods."""

    def __init__(self, driver: webdriver.Chrome | webdriver.Firefox):
        """Initialize TextBasedQueries with a webdriver instance.

        Args:
            driver: A Chrome or Firefox webdriver instance.
        """
        self.driver = driver

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
        return self.execute(script, element, *args)

    @property
    def document(self):
        """Get the document element wrapped in jQuery.

        Returns:
            The document element as a jQuery object.
        """
        return self.execute(jquery_scripts.DOCUMENT_QUERY)

    def _prepare_result(
        self, result: list[webelement.WebElement] | webelement.WebElement | None, first: bool
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

    def find_elements_with_text(
        self, text: str, selector: str = "*", element: webelement.WebElement | None = None, *, first_match: bool = False
    ) -> list[webelement.WebElement] | webelement.WebElement | None:
        """Find elements containing specific text.

        Args:
            text: Text to search for.
            selector: jQuery selector to filter elements.
            element: Optional element to search within. If None, searches entire document.
            first_match: Whether to return only the first match.

        Returns:
            Either a single WebElement, a list of WebElements, or None if no matches found.
        """
        method = ".first()" if first_match else ""
        element = element or self.document
        if element is None:
            return None

        script = jquery_scripts.FIND_ELEMENTS_WITH_TEXT.format(selector=selector, text=text, method=method)
        return self._prepare_result(
            self.query(script=script, element=element),
            first=first_match,
        )

    def find_lowest_element_with_text(
        self, text: str, selector: str = "*", element: webelement.WebElement | None = None, *, exact_match: bool = False
    ) -> webelement.WebElement | None:
        """Find the lowest element in the DOM tree containing specific text.

        Args:
            text: Text to search for.
            selector: jQuery selector to filter elements.
            element: Optional element to search within. If None, searches entire document.
            exact_match: Whether to require an exact text match.

        Returns:
            The lowest matching WebElement or None if not found.
        """
        element = element or self.document
        if element is None:
            return None

        script = (
            jquery_scripts.FIND_LOWEST_ELEMENT_WITH_EXACT_TEXT
            if exact_match
            else jquery_scripts.FIND_LOWEST_ELEMENT_WITH_TEXT
        ).format(selector=selector, text=text)
        return self.query(script=script, element=element)

    def find_elements_with_selector_and_text(
        self,
        selector: str,
        text: str,
        element: webelement.WebElement | None = None,
        *,
        first_match: bool = False,
        exact_match: bool = False,
    ) -> list[webelement.WebElement] | webelement.WebElement | None:
        """Find elements matching both selector and text criteria.

        Args:
            selector: jQuery selector to filter elements.
            text: Text to search for.
            element: Optional element to search within. If None, searches entire document.
            first_match: Whether to return only the first match.
            exact_match: Whether to require an exact text match.

        Returns:
            Either a single WebElement, a list of WebElements, or None if no matches found.
        """
        method = ".first()" if first_match else ""
        element = element or self.document
        if element is None:
            return None

        script = (
            jquery_scripts.FIND_ELEMENTS_WITH_SELECTOR_AND_EXACT_TEXT
            if exact_match
            else jquery_scripts.FIND_ELEMENTS_WITH_SELECTOR_AND_TEXT
        ).format(selector=selector, text=text, method=method)
        return self._prepare_result(
            self.query(script=script, element=element),
            first=first_match,
        )
