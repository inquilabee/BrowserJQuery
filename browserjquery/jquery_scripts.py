JQUERY_INJECTION = """
    var script = document.createElement( 'script' );
    script.type = 'text/javascript';
    script.src =  'https://code.jquery.com/jquery-3.7.1.min.js';
    document.head.appendChild(script);

    script.onload = function() {
        var $ = window.jQuery;
    }
"""

PAGE_HTML = """
    return "<html>" + $("html").html() + "</html>";
"""

JQUERY_INJECTION_CHECK = """
    return $
"""

# Document and element queries
DOCUMENT_QUERY = """return $(document.documentElement)"""

# Element state checks
MATCHES_SELECTOR = """return $(arguments[0]).is('{selector}')"""
HAS_DESCENDANTS = """return $(arguments[0]).has('{selector}').length > 0"""
IS_VISIBLE = """return $(arguments[0]).is(':visible')"""
IS_CHECKED = """return $(arguments[0]).is(':checked')"""
IS_DISABLED = """return $(arguments[0]).is(':disabled')"""
HAS_CLASS = """return $(arguments[0]).hasClass('{class_name}')"""

# Content queries
GET_ATTR = """return $(arguments[0]).attr('{attribute_name}')"""
GET_TEXT = """return $(arguments[0]).text()"""
GET_HTML = """return $(arguments[0]).html()"""

# Traversal queries
GET_PARENT = """return $(arguments[0]).parent()"""
GET_PARENTS = """return $(arguments[0]).parents()"""
GET_CHILDREN = """return $(arguments[0]).children('{selector}')"""
GET_CHILDREN_ALL = """return $(arguments[0]).children()"""
GET_SIBLINGS = """return $(arguments[0]).siblings('{selector}')"""
GET_SIBLINGS_ALL = """return $(arguments[0]).siblings()"""
GET_NEXT = """return $(arguments[0]).next('{selector}').first()[0]"""
GET_NEXT_ALL = """return $(arguments[0]).next().first()[0]"""
GET_PREV = """return $(arguments[0]).prev('{selector}').first()[0]"""
GET_PREV_ALL = """return $(arguments[0]).prev().first()[0]"""
GET_CLOSEST = """return $(arguments[0]).closest('{selector}')"""
GET_FIRST = """return $(arguments[0]).children().first()"""
GET_LAST = """return $(arguments[0]).children().last()"""

# Find elements
FIND_ELEMENTS = """return $(arguments[0]).find("{selector}"){method};"""

FIND_ELEMENTS_WITH_TEXT = """
    return $(arguments[0])
        .find('{selector}')
        .filter(function() {{
            return $(this).text().indexOf('{text}') !== -1;
        }}){method}.get();
"""


FIND_LOWEST_ELEMENT_WITH_TEXT = """
    var elements = $(arguments[0]).find('{selector}').filter(function() {{
        return $(this).text().indexOf('{text}') !== -1;
    }}).get();
    if (elements.length === 0) return null;

    // Find the element with the most parents (deepest in DOM)
    var deepest = elements[0];
    var maxDepth = $(deepest).parents().length;

    for (var i = 1; i < elements.length; i++) {{
        var depth = $(elements[i]).parents().length;
        if (depth > maxDepth) {{
            maxDepth = depth;
            deepest = elements[i];
        }}
    }}
    return deepest;
"""


FIND_LOWEST_ELEMENT_WITH_EXACT_TEXT = """
    var elements = $(arguments[0]).find('{selector}').filter(function() {{
        return $(this).text().trim() === '{text}';
    }}).get();

    if (elements.length === 0) return null;

    // Find the element with the most parents (deepest in DOM)
    var deepest = elements[0];
    var maxDepth = $(deepest).parents().length;

    for (var i = 1; i < elements.length; i++) {{
        var depth = $(elements[i]).parents().length;
        if (depth > maxDepth) {{
            maxDepth = depth;
            deepest = elements[i];
        }}
    }}
    return deepest;
"""

FIND_ELEMENTS_WITH_SELECTOR_AND_TEXT = """
    return $(arguments[0]).find('{selector}').filter(function() {{
        return $(this).text().indexOf('{text}') !== -1;
    }}){method}.get();
"""

FIND_ELEMENTS_WITH_SELECTOR_AND_EXACT_TEXT = """
    return $(arguments[0]).find('{selector}').filter(function() {{
        return $(this).text().trim() === '{text}';
    }}){method}.get();
"""
