import streamlit as st

from src.app.elements.common import EmptySpace
from src.app.elements.result_page import header, back_botton


st.set_page_config(
    page_title="Search result",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

header.display()

EmptySpace().display()

back_botton.display()
