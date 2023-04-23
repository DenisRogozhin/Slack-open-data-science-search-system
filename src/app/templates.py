from src.app.utils import Comment, Post


def search_results_stat(results_count: int, duration: float) -> str:
    return f"""
    <div style="text-align:center;color:grey;font-size:95%;">
        {results_count} результатов (время: {duration:.2f} с)
    </div>"""


def empty_search_results() -> str:
    return f"""
    <div style="text-align:center;color:grey;font-size:125%;">
        Ничего не найдено  ̄\\_(ツ)_/ ̄
        <br>
        Попробуйте изменить  запрос
    </div>"""


def results_per_page_count_text() -> str:
    return f"""
    <div style="
        text-align: center;
        color: dark;
        font-size: 105%;
    ">
        Число результатов на странице
    </div>
    """


def page_number_text() -> str:
    return f"""
    <div style="
        text-align: center;
        color: dark;
        font-size: 105%;
    ">
        Текущая страница
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
    return f"""
    <div style="
        box-sizing: border-box; 
        padding: 5px; 
        border: 0.5px solid #CACFD2; 
        border-radius: 3px; 
        margin-bottom: 4px
    ">
        <div style="
            font-family:    Arial, Helvetica, sans-serif;
            font: italic;
        ">
            {post.text if len(post.text) <= max_snippet_len else 
             post.text[: max_snippet_len] + "..."}
        </div>
        <div style="
            display: flex; 
            justify-content: space-between";
        >
            <div>
                {post.datetime.strftime("%Y-%m-%d %H:%M:%S")}
            </div>
            <div style="
                font: italic 1.2em
            ">
                {post.author}
            </div>
            <div>
                Number of comments: {len(post.comments)}
            </div>
        </div>
    </div>"""


def load_style() -> str:
    return """<style>
    .stButton>button {
        color: #F4F6F7;
        background-color: #8E44AD;
        border-color: #8E44AD;
        # width: 10em;
        width: auto;
        display: block;
        margin: auto;
    # .stButton button:hover {
    #     background-color:#018749;
    #     color: black;
    # }
    }</style>"""


def main_page_header() -> str:
    return """
    <h1 style='text-align: center; color: #8E44AD;'>ODS dump search system 🗿</h1>
    """


def result_page_header() -> str:
    return """
    <h1 style='text-align: center; color: #8E44AD;'>Search result 🗿</h1>
    """


def result_page_post_header() -> str:
    return """
    <h2 style='text-align: center; color: #8E44AD;'>Post 🗿</h2>
    """


def result_page_comments_header() -> str:
    return """
    <h2 style='text-align: center; color: #8E44AD;'>Comments 🗿</h2>
    """


def search_result_comment(comment: Comment) -> str:
    return f"""
    <div style="
        box-sizing: border-box; 
        padding: 5px; 
        border: 0.5px solid #CACFD2; 
        border-radius: 3px; 
        margin-bottom: 4px
    ">
        <div style="
            font-family:    Arial, Helvetica, sans-serif;
            font: italic;
        ">
            {comment.text}
        </div>
        <div style="
            display: flex; 
            justify-content: space-between";
        >
            <div>
                {comment.datetime.strftime("%Y-%m-%d %H:%M:%S")}
            </div>
            <div style="
                font: italic 1.2em
            ">
                {comment.author}
            </div>
        </div>
    </div>"""
