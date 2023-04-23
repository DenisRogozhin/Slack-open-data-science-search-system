from typing import Any, Optional

import streamlit as st


class Element:
    max_snippet_len = 200

    def display(self) -> None:
        raise NotImplementedError


class EmptySpace(Element):
    def __init__(self, size: int) -> None:
        self._size = size

    def display(self) -> None:
        for _ in range(self._size):
            st.write("")


class SessionStateMixin:
    def add_state(self, state_name: str, state_value: Optional[Any]) -> None:
        if state_name not in st.session_state:
            self.set_state(state_name, state_value)

    def set_state(self, state_name: str, state_value: Optional[Any]) -> None:
        st.session_state[state_name] = state_value

    def get_state(self, state_name: str) -> Any:
        return st.session_state[state_name]
