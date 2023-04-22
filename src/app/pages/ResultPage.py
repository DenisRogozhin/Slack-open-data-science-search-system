import streamlit as st

from src.app.elements.common import EmptySpace
from src.app.elements.result_page import header, back_botton, search_result
from src.app.templates import load_style


st.set_page_config(
    page_title="Search result",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.write(load_style(), unsafe_allow_html=True)

header.display()

EmptySpace(1).display()

back_botton.display()

EmptySpace(1).display()

search_result.display()
