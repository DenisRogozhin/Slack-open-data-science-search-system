import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from src.app.elements.common import EmptySpace, SessionStateMixin, Element
from src.app.templates.result_page import (
    result_page_comments_header,
    result_page_header,
    result_page_post_header,
    search_result_comment,
)
from src.app.templates.main_page import search_element
from src.app.utils import Comment

__all__ = [
    "Header",
    "BackBotton",
    "SearchResult",
]


class Header(Element):
    def display(self) -> None:
        st.markdown(result_page_header(), unsafe_allow_html=True)


class SearchComment(Element, SessionStateMixin):
    def __init__(self, comment: Comment) -> None:
        self._comment = comment

    def display(self) -> None:
        if len(self._comment.text) <= self.max_snippet_len:
            st.markdown(search_result_comment(self._comment), unsafe_allow_html=True)
        else:
            with st.expander(self._comment.text[: self.max_snippet_len] + "..."):
                st.markdown(
                    search_result_comment(self._comment, with_border=False),
                    unsafe_allow_html=True,
                )


class SearchResult(Element, SessionStateMixin):
    def display(self) -> None:
        post = self.get_state("search_result")

        st.markdown(result_page_post_header(), unsafe_allow_html=True)

        st.markdown(search_element(post, len(post.text) + 1), unsafe_allow_html=True)

        _, center, _ = st.columns([1, 2, 1])
        with center:
            EmptySpace(1).display()
            st.markdown(result_page_comments_header(), unsafe_allow_html=True)

            for comment in post.comments:
                EmptySpace(1).display()
                SearchComment(comment).display()


class BackBotton(Element, SessionStateMixin):
    def display(self) -> None:
        klick = st.button("Назад")
        if klick:
            switch_page("MainPage")
