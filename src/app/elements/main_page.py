import abc
import datetime

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from src.app.elements.common import SessionStateMixin, Element
from src.app.utils import search

__all__ = [
    "header",
    "search_bar",
    "search_results",
]


class Header(Element):
    def display(self) -> None:
        st.markdown(
            "<h1 style='text-align: center; color: purple;'>ODS dump search system 🗿</h1>",
            unsafe_allow_html=True,
        )


class SearchResults(Element, SessionStateMixin):
    def __init__(self) -> None:
        self._init_state()

    def _init_state(self) -> None:
        self.add_state("search_results", None)

    def search_callback(self) -> None:
        _, center, _ = st.columns([3, 2, 2])
        with center:
            with st.spinner("Поиск..."):
                if self.get_state("search_query"):
                    new_search_result = search(
                        self.get_state("search_query"),
                        self.get_state("start_date"),
                        self.get_state("end_date"),
                    )
                    self.set_state("search_results", new_search_result)
                else:
                    self.set_state("search_results", None)

    def display(self) -> None:
        self._init_state()
        _, center, _ = st.columns([3, 2, 2])

        with center:
            if self.get_state("search_results") is not None:
                for i, search_result in enumerate(self.get_state("search_results")):
                    klick = st.button(
                        label=f"Результат поиска {i}",
                        type="primary",
                    )
                    if klick:
                        switch_page("ResultPage")
            else:
                st.caption("_Ничего не найдено_  ̄\\\_(ツ)\_/ ̄")
                st.caption("_Попробуйте изменить  запрос_")


class SearchBar(Element, SessionStateMixin):
    MIN_DATE = datetime.date(2017, 1, 1)
    MAX_DATE = datetime.date(2022, 1, 1)
    sorting_options = ["⬇️ по релевантности", "⬇️ по дате", "⬆️ по дате"]

    def __init__(self, search_results: SearchResults) -> None:
        self._search_results = search_results
        self._init_state()

    def _init_state(self) -> None:
        self.add_state("search_query", "")
        self.add_state("start_date", self.MIN_DATE)
        self.add_state("end_date", self.MAX_DATE)
        self.add_state("sorting_direction", None)

    def display_search_bar(self, column) -> None:
        search_query = column.text_input(
            label="Search",
            placeholder="Введите поисковый запрос",
            label_visibility="collapsed",
            value=self.get_state("search_query"),
            # key="search_query",
        )
        # need store also current value of search query
        # for correct displaying after return from second page
        self.set_state("search_query", search_query)

    def display_date_interval(self, column) -> None:
        date = column.date_input(
            "Time period",
            value=[self.get_state("start_date"), self.get_state("end_date")],
            min_value=self.MIN_DATE,
            max_value=self.MAX_DATE,
            label_visibility="collapsed",
            # TODO: callback for date
        )
        # update date range
        if len(date) == 2:
            self.set_state("start_date", date[0])
            self.set_state("end_date", date[1])
        # elif len(date) == 1:
        #     self.set_state("start_date", date[0])
        #     self.set_state("end_date", self.MAX_DATE)

    def display_search_button(self, column) -> None:
        column.button(
            label="Найти",
            type="primary",
            # on_click=search_callback,
            on_click=self._search_results.search_callback,
            # args=(query, st.session_state.start_date, st.session_state.end_date),
        )

    def display_sorting_options(self, column) -> None:
        st.session_state.sorting_direction = column.selectbox(
            "Ранжировать",
            options=self.sorting_options,
            label_visibility="collapsed",
        )

    def display(self) -> None:
        self._init_state()
        col1, col2, col3, col4 = st.columns([5, 2, 2, 1])

        self.display_search_bar(col1)
        self.display_date_interval(col2)
        self.display_sorting_options(col3)
        self.display_search_button(col4)


class Result(Element):
    def __init__(self) -> None:
        self._init_state()

    def _init_state(self) -> None:
        self.add_state("search_query", "")
        self.add_state("start_date", self.MIN_DATE)
        self.add_state("end_date", self.MAX_DATE)
        self.add_state("sorting_direction", None)


header = Header()
search_results = SearchResults()
search_bar = SearchBar(search_results)
