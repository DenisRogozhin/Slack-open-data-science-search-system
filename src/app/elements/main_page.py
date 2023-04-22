import abc
import datetime

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from src.app.elements.common import SessionStateMixin, Element
from src.app.templates import (
    search_element,
    empty_search_results,
    search_results_stat,
    main_page_header,
)
from src.app.utils import Post, search

__all__ = [
    "header",
    "search_bar",
    "search_results",
]


class Header(Element):
    def display(self) -> None:
        st.markdown(main_page_header(), unsafe_allow_html=True)


class SearchElement(Element, SessionStateMixin):
    def __init__(self, post: Post) -> None:
        self._post = post

    def display(self, idx: int) -> None:
        st.markdown(search_element(self._post), unsafe_allow_html=True)
        klick = st.button(
            label="Посмотреть",
            type="primary",
            key=idx + 1,
        )
        if klick:
            self.set_state("search_result", self._post)
            switch_page("ResultPage")


class SearchResults(Element, SessionStateMixin):
    def __init__(self) -> None:
        self._init_state()

    def _init_state(self) -> None:
        self.add_state("search_results", None)
        self.add_state("search_result", None)

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
                    # TODO: need sort results by sorting_directon here
                    self.set_state("search_results", new_search_result)
                else:
                    self.set_state("search_results", None)

    def display(self) -> None:
        self._init_state()
        _, center, _ = st.columns([1, 2, 1])

        with center:
            if self.get_state("search_results") is not None:
                st.write(search_results_stat(100, 2.0), unsafe_allow_html=True)
                for i, search_result in enumerate(self.get_state("search_results")):
                    search_result_element = SearchElement(post=search_result)
                    search_result_element.display(idx=i)
            else:
                st.write(empty_search_results(), unsafe_allow_html=True)
                st.caption("")


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
        self.add_state("sorting_direction_idx", 1)

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
            on_change=self._search_results.search_callback,
        )
        # update date range
        if len(date) == 2:
            self.set_state("start_date", date[0])
            self.set_state("end_date", date[1])

    def display_sorting_options(self, column) -> None:
        sorting_direction = column.selectbox(
            "Ранжировать",
            label_visibility="collapsed",
            options=self.sorting_options,
            index=self.get_state("sorting_direction_idx"),
            on_change=self._search_results.search_callback,
        )
        self.set_state(
            "sorting_direction_idx", self.sorting_options.index(sorting_direction)
        )

    def display_search_button(self, column) -> None:
        column.button(
            label="Найти",
            type="primary",
            on_click=self._search_results.search_callback,
        )

    def display(self) -> None:
        self._init_state()
        col1, col2, col3, col4 = st.columns([5, 2, 2, 1])

        self.display_search_bar(col1)
        self.display_date_interval(col2)
        self.display_sorting_options(col3)
        self.display_search_button(col4)


header = Header()
search_results = SearchResults()
search_bar = SearchBar(search_results)
