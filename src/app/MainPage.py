import streamlit as st

from src.app.elements.main_page import header, search_bar, search_results
from src.app.elements.common import EmptySpace
from src.app.templates import load_style

st.set_page_config(
    page_title="ODS dump search",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.write(load_style(), unsafe_allow_html=True)

# st.write(
#     """<style>
#     [data-testid="column"] {
#         width: calc(50% - 1rem);
#         flex: 1 1 calc(50% - 1rem);
#         min-width: calc(50% - 1rem);
#     }
#     </style>""",
#     unsafe_allow_html=True,
# )

header.display()

EmptySpace(2).display()

search_bar.display()

search_results.display()
