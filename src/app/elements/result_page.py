import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from src.app.elements.common import SessionStateMixin, Element

__all__ = [
    "header",
    "back_botton",
]


class Header(Element):
    def display(self) -> None:
        st.markdown(
            "<h1 style='text-align: center; color: purple;'>Search result 🗿</h1>",
            unsafe_allow_html=True,
        )


class BackBotton(Element, SessionStateMixin):
    def display(self) -> None:
        klick = st.button("Назад")
        if klick:
            switch_page("MainPage")


header = Header()

back_botton = BackBotton()
