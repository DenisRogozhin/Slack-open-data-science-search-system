from src.app.utils import Comment


def result_page_header() -> str:
    return """
    <h1 style="
        text-align: center;
        color: #8E44AD;
    ">
        Search result 🗿
    </h1>"""


def result_page_post_header() -> str:
    return """
    <h2 style="
        text-align: center; 
        color: #8E44AD;
    ">
        Post 🗿
    </h2>"""


def result_page_comments_header() -> str:
    return """
    <h2 style="
        text-align: center; 
        color: #8E44AD;
    ">
        Comments 🗿
    </h2>"""


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
