from src.app.utils import Post
from src.app.utils import _


def main_page_header() -> str:
    _main_header = _("ODS dump search system")
    return f"""
    <h1 style="
        text-align: center;
        color: #8E44AD;
    ">
        {_main_header}
    </h1>"""


def search_results_stat(results_count: int, duration: float) -> str:
    _search_stat = "Results count: {0} (time: {1:.2f} seconds)".format(
        results_count, duration
    )
    return f"""
    <div style="
        text-align: center;
        color: grey;
        font-size: 95%;
    ">
        {_search_stat}
    </div>"""


def empty_search_results() -> str:
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
