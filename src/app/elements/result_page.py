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
from src.app.utils import Comment, _

__all__ = [
    "Header",
    "BackBotton",
    "SearchResult",
]


class Header(Element):
    """
    This class represents a header element. It inherits from `Element`.
    """

    def display(self) -> None:
        """
        Display method for a header element.

        This method displays the header element,
        which includes the title of the search results page.

        :return: None
        :rtype: None
        """
        st.markdown(result_page_header(), unsafe_allow_html=True)


class SearchComment(Element, SessionStateMixin):
    """
    This class represents a search comment element.
    It inherits from `Element` and `SessionStateMixin`.
    """

    def __init__(self, comment: Comment) -> None:
        """
        Constructor for a search comment element.

        :param comment: The comment to be displayed
        :type comment: Comment

        :return: None
        :rtype: None
        """
        self._comment = comment

    def display(self) -> None:
        """
        Display method for a search comment element.

        This method displays the search comment,
        including the text and a snippet of the comment if it is too long.

        :return: None
        :rtype: None
        """
        if len(self._comment.text) <= self.max_snippet_len:
            st.markdown(search_result_comment(self._comment), unsafe_allow_html=True)
        else:
            with st.expander(self._comment.text[: self.max_snippet_len] + "..."):
                st.markdown(
                    search_result_comment(self._comment, with_border=False),
                    unsafe_allow_html=True,
                )


class SearchResult(Element, SessionStateMixin):
    """
    This class represents a search result element.
    It inherits from `Element` and `SessionStateMixin`.
    """

    def display(self) -> None:
        """
        Display method for a search result element.

        This method displays the search result, including the post, comments, and headers.

        :return: None
        :rtype: None
        """
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
    """
    A class that represents a back button element.

    This class inherits from `Element` and `SessionStateMixin`.
    """

    def display(self) -> None:
        """
        Display method for a back button element.

        This method displays a Streamlit button labeled "Back".
        When the button is clicked, it switches the page to "MainPage".

        :return: None
        :rtype: None
        """
        klick = st.button(_("Back"))
        if klick:
            switch_page("MainPage")
