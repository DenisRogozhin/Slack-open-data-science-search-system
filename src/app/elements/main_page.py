import datetime
import time

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from src.app.elements.common import EmptySpace, SessionStateMixin, Element
from src.app.templates.main_page import (
    page_number_display,
    page_number_text,
    results_per_page_count_text,
    search_element,
    empty_search_results,
    search_results_stat,
    main_page_header,
)
from src.app.utils import Post, search, sort_results

__all__ = [
    "Header",
    "SearchResults",
    "SearchBar",
]


class Header(Element):
    def display(self) -> None:
        st.markdown(main_page_header(), unsafe_allow_html=True)


class SearchElement(Element, SessionStateMixin):
    def __init__(self, post: Post) -> None:
        self._post = post

    def _switch_page(self, page_name: str) -> None:
        self.set_state("default_pages_count", self.get_state("pages_count"))
        self.set_state("default_sorting_direction", self.get_state("sorting_direction"))
        switch_page(page_name)

    def display(self, idx: int) -> None:
        st.markdown(
            search_element(post=self._post, max_snippet_len=self.max_snippet_len),
            unsafe_allow_html=True,
        )
        klick = st.button(
            label="Посмотреть",
            type="primary",
            key=idx + 1,
        )
        if klick:
            self.set_state("search_result", self._post)
            self._switch_page("ResultPage")


class SearchResults(Element, SessionStateMixin):
    pages_options = [5, 10, 20, 40, 80]

    def __init__(self) -> None:
        self._init_state()

    def _init_state(self) -> None:
        self.add_state("search_results", None)
        self.add_state("search_result", None)
        self.add_state("search_time", 0.0)
        self.add_state("current_pages_count", None)
        self.add_state("page_number", None)
        self.add_state("default_pages_count", self.pages_options[0])

    def search_callback(self) -> None:
        _, center, _ = st.columns([3, 2, 2])
        with center:
            if self.get_state("search_query"):
                start_time = time.time()
                new_search_result = search(
                    self.get_state("search_query"),
                    self.get_state("start_date"),
                    self.get_state("end_date"),
                )
                end_time = time.time()
                self.set_state("search_time", end_time - start_time)
                # TODO: need sort results by sorting_directon here
                self.set_state("search_results", new_search_result)
                self.set_state("page_number", 1)
            else:
                self.set_state("search_results", None)
                self.set_state("page_number", None)

    def sort_results_callback(self) -> None:
        search_results = self.get_state("search_results")
        if search_results:
            sorted_results = sort_results(
                self.get_state("search_query"),
                search_results,
                self.get_state("sorting_direction"),
            )
            self.set_state("search_results", sorted_results)

    def _pages_count_callback(self) -> None:
        self.set_state("page_number", 1)
        self.set_state("default_pages_count", self.pages_options[0])

    def display_page_count(self, column) -> None:
        if self.get_state("search_results") is not None:
            column.markdown(results_per_page_count_text(), unsafe_allow_html=True)
            _, center, _ = column.columns([2, 2, 2])
            center.selectbox(
                "Число результатов на странице",
                label_visibility="collapsed",  # "visible",
                options=self.pages_options,
                index=self.pages_options.index(self.get_state("default_pages_count")),
                key="pages_count",
                on_change=self._pages_count_callback,
            )

    def display_sorting_stat(self, column) -> None:
        search_result = self.get_state("search_results")
        if search_result:
            with column:
                EmptySpace(2).display()
                st.write(
                    search_results_stat(
                        len(self.get_state("search_results")),
                        self.get_state("search_time"),
                    ),
                    unsafe_allow_html=True,
                )
                EmptySpace(2).display()

    def display_page_number(self, column) -> None:
        if self.get_state("search_results") is not None:
            page_number = self.get_state("page_number")
            results_per_page = self.get_state("pages_count")
            results_cnt = len(self.get_state("search_results"))
            pages_count = (results_cnt - 1) // results_per_page + 1

            column.markdown(page_number_text(), unsafe_allow_html=True)

            _, left, center, rigth, _ = column.columns([1, 2, 2, 2, 1])

            if page_number > 1:
                left.button(
                    "◀️",
                    on_click=lambda: self.set_state("page_number", page_number - 1),
                )

            center.markdown(
                page_number_display(page_number, pages_count), unsafe_allow_html=True
            )

            if page_number < pages_count:
                rigth.button(
                    "▶️",
                    on_click=lambda: self.set_state("page_number", page_number + 1),
                )

    def display_search_results(self, column) -> None:
        with column:
            search_results = self.get_state("search_results")

            if search_results is not None:
                page_number = self.get_state("page_number")
                pages_count = self.get_state("pages_count")

                cur_page_results = search_results[
                    (page_number - 1)
                    * pages_count : min(page_number * pages_count, len(search_results))
                ]
                for i, search_result in enumerate(cur_page_results):
                    search_result_element = SearchElement(post=search_result)
                    search_result_element.display(idx=i)
            else:
                st.write(empty_search_results(), unsafe_allow_html=True)
                st.caption("")

    def display(self) -> None:
        self._init_state()
        left, center, right = st.columns([1, 2, 1])

        self.display_page_count(left)
        self.display_sorting_stat(center)
        self.display_page_number(right)

        _, content, _ = st.columns([1, 2, 1])

        self.display_search_results(content)


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
        self.add_state("default_sorting_direction", self.sorting_options[0])

    def display_search_bar(self, column) -> None:
        search_query = column.text_input(
            label="Search",
            placeholder="Введите поисковый запрос",
            label_visibility="collapsed",
            value=self.get_state("search_query"),
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
        )
        # update date range
        if len(date) == 2:
            self.set_state("start_date", date[0])
            self.set_state("end_date", date[1])

    def _sorting_direction_callback(self) -> None:
        self._search_results.sort_results_callback()
        self.set_state("default_sorting_direction", self.sorting_options[0])

    def display_sorting_options(self, column) -> None:
        column.selectbox(
            "Ранжировать",
            label_visibility="collapsed",
            options=self.sorting_options,
            index=self.sorting_options.index(
                self.get_state("default_sorting_direction")
            ),
            key="sorting_direction",
            on_change=self._sorting_direction_callback,
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
