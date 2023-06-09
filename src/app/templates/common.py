"""Templates for displaying on both pages."""


def load_style() -> str:
    """
    Return the CSS style for customizing the appearance of Streamlit widgets.

    :return: The CSS style for customizing the appearance of Streamlit widgets.
    :rtype: str
    """
    return """<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap');
    @import url('https://fonts.cdnfonts.com/css/prompt');
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
