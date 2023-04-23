import streamlit as st

from src.app.elements.common import EmptySpace
from src.app.elements.result_page import Header, SearchResult, BackBotton
from src.app.templates.common import load_style


st.set_page_config(
    page_title="Search result",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# load styles
st.write(load_style(), unsafe_allow_html=True)

# init page elements
header = Header()

search_result = SearchResult()

back_botton = BackBotton()

# display page elements
header.display()

EmptySpace(1).display()

back_botton.display()

EmptySpace(1).display()

search_result.display()
