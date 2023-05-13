import streamlit

from src.app.templates.common import load_style


def button_decorator(func):
    def wrapper(*args, **kwargs):
        streamlit.write(load_style(), unsafe_allow_html=True)
        return func(*args, **kwargs)

    return wrapper
