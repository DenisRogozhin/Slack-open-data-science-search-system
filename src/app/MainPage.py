"""Main page."""
import streamlit as st

from src.app.elements.main_page import Header, SearchResults, SearchBar
from src.app.elements.common import EmptySpace
from src.app.templates.common import load_style
from src.app.utils import _


def main():
    st.set_page_config(
        page_title=_("ODS dump search"),
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # load styles
    st.write(load_style(), unsafe_allow_html=True)

    # init page elements
    header = Header()

    search_results = SearchResults()

    search_bar = SearchBar(search_results)

    # display page elements
    header.display()

    EmptySpace(2).display()

    search_bar.display()

    search_results.display()


if __name__ == "__main__":
    main()
