from src.app.utils import Comment
from src.app.utils import _


def result_page_header() -> str:
    result_header_str = _("Search result")
    return f"""
    <h1 style="
        text-align: center;
        color: #8E44AD;
    ">
        {result_header_str}
    </h1>"""


def result_page_post_header() -> str:
    post_str = _("Post")
    return f"""
    <h2 style="
        text-align: center; 
        color: #8E44AD;
    ">
        {post_str}
    </h2>"""


def result_page_comments_header() -> str:
    comment_str = _("Comments")
    return f"""
    <h2 style="
        text-align: center; 
        color: #8E44AD;
    ">
        {comment_str}
    </h2>"""


def search_result_comment(comment: Comment, with_border: bool = True) -> str:
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
            <div style="
                font-family: 'Prompt', sans-serif;
            ">
                {comment.author}
            </div>
        </div>
    </div>"""
