"""Templates for displaying on the result page."""
import sys
sys.path.append('.')
from src.app.utils import Comment
from src.app.utils import _


def result_page_header() -> str:
    """
    Return a string representing the header of the search result page.

    :return: The HTML formatted header string for the search result page.
    :rtype: str
    """
    result_header_str = _("Search result")
    return f"""
    <h1 style="
        text-align: center;
        color: #8E44AD;
    ">
        {result_header_str}
    </h1>"""


def result_page_post_header() -> str:
    """
    Return a string representing the post header of the search result page.

    :return: The HTML formatted post header string for the search result page.
    :rtype: str
    """
    post_str = _("Post")
    return f"""
    <h2 style="
        text-align: center;
        color: #8E44AD;
    ">
        {post_str}
    </h2>"""


def result_page_comments_header() -> str:
    """
    Return a string representing the comments header of the search result page.

    :return: The HTML formatted comments header string for the search result page.
    :rtype: str
    """
    comment_str = _("Comments")
    return f"""
    <h2 style="
        text-align: center;
        color: #8E44AD;
    ">
        {comment_str}
    </h2>"""


def search_result_comment(comment: Comment, with_border: bool = True) -> str:
    """
    Return a string representing the formatted comment for the search result page.

    :param comment: The comment object to display.
    :type comment: Comment

    :param with_border: Whether or not to include a border around the comment.
    :type with_border: bool

    :return: The HTML formatted comment string for the search result page.
    :rtype: str
    """
    if with_border:
        style = """
        box-sizing: border-box;
        padding: 15px;
        border: 1px solid #CACFD2;
        border-radius: 3px;
        margin-bottom: 4px;"""
    else:
        style = """
        box-sizing: border-box;
        padding: 15px;
        margin-bottom: 4px;"""

    return f"""
    <div style="{style}">
        <div style="
            font-size: 90%;
            text-align: center;
        ">
            {comment.text}
        </div>
        <br>
        <div style="
            display: flex;
            justify-content: space-between";
        >
            <div style="
                font-family: 'Roboto', sans-serif;
            ">
                {comment.datetime.strftime("%Y-%m-%d %H:%M:%S")}
            </div>
        </div>
    </div>"""
