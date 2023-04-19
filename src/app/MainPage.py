import streamlit as st

from src.app.elements.main_page import header, search_bar, search_results
from src.app.elements.common import EmptySpace

st.set_page_config(
    page_title="ODS dump search",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

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

EmptySpace().display()

search_bar.display()

EmptySpace().display()

search_results.display()
