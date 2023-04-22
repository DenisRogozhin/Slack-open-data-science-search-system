from src.app.utils import Post


def search_results_stat(results_count: int, duration: float) -> str:
    return f"""
    <div style="text-align:center;color:grey;font-size:95%;">
        {results_count} results ({duration:.2f} seconds)
    </div>"""


def empty_search_results() -> str:
    return f"""
    <div style="text-align:center;color:grey;font-size:125%;">
        Ничего не найдено  ̄\\_(ツ)_/ ̄
        <br>
        Попробуйте изменить  запрос
    </div>"""


def search_element(post: Post) -> str:
    return f"""
    <div style="border:0.5rem outset;border-radius: 1px;">
        {post.text}
        <br>
        {post.author}
        <br>
        Number of comments: {len(post.comments)}
    </div>"""
    # .stButton>button {
    #     color: #4F8BF9;
    #     border-radius: 50%;
    #     height: 10em;
    #     width: 10em;
    # }
    # outline: 0.5rem solid khaki;
    # box-shadow: 0 0 0 2rem skyblue;
    # border-radius: 1px;
    # font: bold 1rem sans-serif;
    # margin: 2rem;
    # padding: 1rem;
    # outline-offset: 0.5rem;


def load_style() -> str:
    return """<style>
    .stButton>button {
        color: #F4F6F7;
        background-color: #8E44AD;
        border-color: #8E44AD;
        width: 10em;
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
    <h1 style='text-align: center; color: purple;'>Search result 🗿</h1>
    """
