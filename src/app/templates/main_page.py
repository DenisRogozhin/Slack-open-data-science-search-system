from src.app.utils import Post


def main_page_header() -> str:
    return """
    <h1 style="
        text-align: center;
        color: #8E44AD;
    ">
        ODS dump search system 🗿
    </h1>"""


def search_results_stat(results_count: int, duration: float) -> str:
    return f"""
    <div style="
        text-align: center;
        color: grey;
        font-size: 95%;
    ">
        Число результатов: {results_count} (время: {duration:.2f} с)
    </div>"""


def empty_search_results() -> str:
    return f"""
    <div style="
        text-align: center;
        color: grey;
        font-size:125%;
    ">
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
