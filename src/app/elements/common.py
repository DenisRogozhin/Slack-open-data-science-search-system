from typing import Any, Optional

import streamlit as st


class Element:
    """
    An abstract base class for UI elements in a Streamlit app.
    """

    # The maximum length of a text snippet to display.
    max_snippet_len: int = 200

    def display(self) -> None:
        """
        Displays the UI element.

        :return: None
        :rtype: None
        """
        raise NotImplementedError


class EmptySpace(Element):
    """
    A class used to display an empty space in a Streamlit app.
    """

    def __init__(self, size: int) -> None:
        """
        Initializes the EmptySpace object with the specified size.

        :param size: The size of the empty space.
        :type size: int

        :return: None
        :rtype: None
        """
        self._size = size

    def display(self) -> None:
        """
        Displays the empty space.

        :return: None
        :rtype: None
        """
        for _ in range(self._size):
            st.write("")


class SessionStateMixin:
    """
    A mixin class for adding session state functionality to a Streamlit app.
    """

    def add_state(self, state_name: str, state_value: Optional[Any]) -> None:
        """
        Adds a new state to the session state if it does not already exist.

        :param state_name: The name of the state to add.
        :type state_name: str

        :param state_value: The initial value of the state.
        :type state_value: Any

        :return: None
        :rtype: None
        """
        if state_name not in st.session_state:
            self.set_state(state_name, state_value)

    def set_state(self, state_name: str, state_value: Optional[Any]) -> None:
        """
        Sets the value of a state in the session state.

        :param state_name: The name of the state to set.
        :type state_name: str

        :param state_value: The new value of the state.
        :type state_value: Any

        :return: None
        :rtype: None
        """
        st.session_state[state_name] = state_value

    def get_state(self, state_name: str) -> Any:
        """
        Retrieves the value of a state from the session state.

        :param state_name: The name of the state to retrieve.
        :type state_name: str

        :return: The value of the state.
        :rtype: Any
        """
        return st.session_state[state_name]
