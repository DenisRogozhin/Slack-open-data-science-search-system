"""Templates for displaying on the mane page."""
from src.app.utils import Post, _, ngettext


def main_page_header() -> str:
    """
    Return the HTML code for the main header of the ODS dump search system.

    :return: HTML code
    :rtype: str
    """
    _main_header = _("ODS dump search system")
    return f"""
    <h1 style="
        text-align: center;
        color: #8E44AD;
    ">
        {_main_header}
    </h1>"""


def search_results_stat(results_count: int, duration: float) -> str:
    """
    Return the HTML code for displaying the search results statistics.

    :param results_count: The number of search results.
    :type results_count: int

    :param duration: The duration of the search.
    :type duration: float

    :return: HTML code
    :rtype: str
    """
    _search_stat = ngettext(
        "{0} result:  ({1:.2f} seconds)", "{0} results ({1:.2f} seconds)", results_count
    ).format(results_count, duration)
    return f"""
    <div style="
        text-align: center;
        color: grey;
        font-size: 95%;
    ">
        {_search_stat}
    </div>"""


def empty_search_results() -> str:
    """
    Return the HTML code for displaying a message when there are no search results.

    :return: HTML code
    :rtype: str
    """
    _empty_results = _("No results")
    _try_to_change_query = _("Try to change query")
    return f"""
    <div style="
        text-align: center;
        color: grey;
        font-size:125%;
    ">
        {_empty_results}  ̄\\_(ツ)_/ ̄
        <br>
        {_try_to_change_query}
    </div>"""


def results_per_page_count_text() -> str:
    """
    Return the HTML code for displaying the text "Results per page".

    :return: HTML code
    :rtype: str
    """
    _results_per_page = _("Results per page")
    return f"""
    <div style="
        text-align: center;
        color: dark;
        font-size: 105%;
    ">
        {_results_per_page}
    </div>
    """


def page_number_text() -> str:
    """
    Return the HTML code for displaying the text "Current page".

    :return: HTML code
    :rtype: str
    """
    _current_page = _("Current page")
    return f"""
    <div style="
        text-align: center;
        color: dark;
        font-size: 105%;
    ">
        {_current_page}
    </div>
    """


def sort_by_text() -> str:
    """
    Return the HTML code for displaying the text "Sort by".

    :return: HTML code
    :rtype: str
    """
    _current_page = _("Sort by")
    return f"""
    <div style="
        text-align: center;
        color: dark;
        font-size: 105%;
    ">
        {_current_page}
    </div>
    """


def date_period_text() -> str:
    """
    Return the HTML code for displaying the text "Date period".

    Return a string with a HTML div element containing the localized text "Current page"
    centered and styled with a dark color and font-size of 105%.

    :return: A string with a HTML div element containing the localized text "Current page".
    :rtype: str
    """
    _current_page = _("Current page")
    return f"""
    <div style="
        text-align: center;
        color: dark;
        font-size: 105%;
    ">
        {_current_page}
    </div>
    """


def page_number_display(page_number: int, pages_count: int) -> str:
    """
    Page number display template.

    Return a string with a HTML div element containing the page number and the total number
    of pages, centered and styled with a color of #8E44AD and font-size of 130%.

    :param page_number: The current page number.
    :type page_number: int

    :param pages_count: The total number of pages.
    :type pages_count: int

    :return: A HTML div containing the page number and the total number of pages.
    :rtype: str
    """
    return f"""
    <div style="
        text-align: center;
        color: #8E44AD;
        font-size: 130%;
    ">
        {page_number} / {pages_count}
    </div>
    """


def search_element(post: Post, max_snippet_len: int) -> str:
    """
    Search element template.

    Return a string with a HTML div element containing the text of a post,
    the date and time it was posted,
    the author's name and the number of comments it has.
    The text is truncated to a maximum length set by the
    max_snippet_len parameter if it exceeds this length.

    :param post: The Post object to display.
    :type post: Post

    :param max_snippet_len: The maximum length of the post text snippet to display.
    :type max_snippet_len: int

    :return: A HTML div element containing the post text, date and time, author's info.
    :rtype: str
    """
    _number_of_comments = _("Number of comments")
    return f"""
    <div style="
        box-sizing: border-box;
        padding: 5px;
        border: 0.5px solid #CACFD2;
        border-radius: 3px;
        margin-bottom: 4px
    ">
        <div style="
            text-align: center;
        ">
            {post.text if len(post.text) <= max_snippet_len else
             post.text[: max_snippet_len] + "..."}
        </div>
        <br>
        <div style="
            display: flex;
            justify-content: space-between";
        >
            <div style="
                font-family: 'Roboto', sans-serif;
            ">
                {post.datetime.strftime("%Y-%m-%d %H:%M:%S")}
            </div>
            <div style="
                font-family: 'Prompt', sans-serif;
            ">
                {post.author}
            </div>
            <div style="
                font-family: 'Roboto', sans-serif;
            ">
                {_number_of_comments}: {len(post.comments)}
            </div>
        </div>
    </div>"""
