import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from src.app.elements.common import SessionStateMixin, Element
from src.app.templates import result_page_header, search_element

__all__ = [
    "header",
    "back_botton",
    "search_result",
]


class Header(Element):
    def display(self) -> None:
        st.markdown(result_page_header(), unsafe_allow_html=True)


class SearchResult(Element, SessionStateMixin):
    def display(self) -> None:
        st.markdown(
            search_element(self.get_state("search_result")), unsafe_allow_html=True
        )


class BackBotton(Element, SessionStateMixin):
    def display(self) -> None:
        klick = st.button("Назад")
        if klick:
            switch_page("MainPage")


header = Header()
search_result = SearchResult()
back_botton = BackBotton()
