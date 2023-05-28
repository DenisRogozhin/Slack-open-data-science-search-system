"""Elements of main page."""
import datetime
import time
from typing import List

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from src.app.elements.common import EmptySpace, SessionStateMixin, Element
from src.app.elements.utils import button_decorator
from src.app.templates.main_page import (
    date_period_text,
    page_number_display,
    page_number_text,
    results_per_page_count_text,
    search_element,
    empty_search_results,
    search_results_stat,
    main_page_header,
    sort_by_text,
)
from src.app.utils import Post, search, sort_results, _

__all__ = [
    "Header",
    "SearchResults",
    "SearchBar",
]


class Header(Element):
    """This class represents a header element. It inherits from `Element`."""

    def display(self) -> None:
        """
        Display method for a header element.

        This method displays the header element, w
        hich includes the title of the search results page.

        :return: None
        :rtype: None
        """
        st.markdown(main_page_header(), unsafe_allow_html=True)


class SearchElement(Element, SessionStateMixin):
    """
    SearchElement class.

    This class represents a search element. It inherits from `Element` and `SessionStateMixin`.
    """

    def __init__(self, post: Post) -> None:
        """
        Construct a `SearchElement` instance.

        :param post: The post to be displayed.
        :type post: Post

        :return: None
        :rtype: None
        """
        self._post = post

    def _switch_page(self, page_name: str) -> None:
        """
        Switche the page to the given name.

        :param page_name: The name of the page to switch to.
        :type page_name: str

        :return: None
        :rtype: None
        """
        self.set_state("default_pages_count", self.get_state("pages_count"))
        self.set_state("default_sorting_direction", self.get_state("sorting_direction"))
        switch_page(page_name)

    def display(self, idx: int) -> None:
        """
        Display the search element and handles the lookup button click.

        :param idx: The index of the search element.
        :type idx: int

        :return: None
        :rtype: None
        """
        st.markdown(
            search_element(post=self._post, max_snippet_len=self.max_snippet_len),
            unsafe_allow_html=True,
        )
        klick = st.button(
            label=_("Lookup"),  # "Посмотреть"
            type="primary",
            key=idx + 1,
        )
        if klick:
            self.set_state("search_result", self._post)
            self._switch_page("ResultPage")


class SearchResults(Element, SessionStateMixin):
    """
    SearchResults class.

    This class represents a search results element.
    It inherits from `Element` and `SessionStateMixin`.
    """

    pages_options: list[int] = [5, 10, 20, 40, 80]
    # A list of possible options for the number of results per page

    def __init__(self) -> None:
        """
        Construct a `SearchResults` instance.

        :return: None
        :rtype: None
        """
        self._init_state()

    def _init_state(self) -> None:
        """
        Initialize the state variables.

        :return: None
        :rtype: None
        """
        self.add_state("search_results", None)
        self.add_state("search_result", None)
        self.add_state("search_time", 0.0)
        self.add_state("current_pages_count", None)
        self.add_state("page_number", None)
        self.add_state("default_pages_count", self.pages_options[0])

    @button_decorator
    def search_callback(self) -> None:
        """
        Handle the search button click event.

        :return: None
        :rtype: None
        """
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

    @button_decorator
    def sort_results_callback(self) -> None:
        """
        Handle the sort button click event.

        :return: None
        :rtype: None
        """
        search_results = self.get_state("search_results")
        if search_results:
            sorted_results = sort_results(
                self.get_state("search_query"),
                search_results,
                self.get_state("sorting_direction"),
            )
            self.set_state("search_results", sorted_results)

    @button_decorator
    def _pages_count_callback(self) -> None:
        """
        Handle the change in the number of results per page.

        :return: None
        :rtype: None
        """
        self.set_state("page_number", 1)
        self.set_state("default_pages_count", self.pages_options[0])

    def display_page_count(self, column: st.DeltaGenerator) -> None:
        """
        Display the number of results per page selector.

        :param column: The column to display the selector in.
        :type column: streamlit.DeltaGenerator

        :return: None
        :rtype: None
        """
        if self.get_state("search_results") is not None:
            column.markdown(results_per_page_count_text(), unsafe_allow_html=True)
            _, center, _ = column.columns([2, 2, 2])
            center.selectbox(
                label="Number of results per page",
                label_visibility="collapsed",  # "visible",
                options=self.pages_options,
                index=self.pages_options.index(self.get_state("default_pages_count")),
                key="pages_count",
                on_change=self._pages_count_callback,
            )

    def display_sorting_stat(self, column: st.DeltaGenerator) -> None:
        """
        Display the statistics such as the number of results and search time.

        :param column: The column to display the statistics in.
        :type column: streamlit.DeltaGenerator

        :return: None
        :rtype: None
        """
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

    def display_page_number(self, column: st.DeltaGenerator) -> None:
        """
        Display the page number and navigation buttons for pagination.

        :param column: The column to display the page number in.
        :type column: streamlit.DeltaGenerator

        :return: None
        :rtype: None
        """
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

    def display_search_results(self, column: st.DeltaGenerator) -> None:
        """
        Display the search results in a column.

        :param column: The column to display the search results in.
        :type column: streamlit.DeltaGenerator

        :return: None
        :rtype: None
        """
        with column:
            search_results = self.get_state("search_results")

            if search_results is not None:
                page_number = self.get_state("page_number")
                pages_count = self.get_state("pages_count")

                cur_page_results = search_results[
                    (page_number - 1)
                    * pages_count: min(page_number * pages_count, len(search_results))
                ]
                for i, search_result in enumerate(cur_page_results):
                    search_result_element = SearchElement(post=search_result)
                    search_result_element.display(idx=i)
            else:
                st.write(empty_search_results(), unsafe_allow_html=True)
                st.caption("")

    def display(self) -> None:
        """
        Initialize the state and displays the search results and statistics.

        :return: None
        :rtype: None
        """
        self._init_state()
        left, center, right = st.columns([1, 2, 1])

        self.display_page_count(left)
        self.display_sorting_stat(center)
        self.display_page_number(right)

        EmptySpace(1).display()
        _, content, _ = st.columns([1, 2, 1])

        self.display_search_results(content)


class SearchBar(Element, SessionStateMixin):
    """A class used to display a search bar with filters and sorting options."""

    # The minimum date value for the date interval filter.
    MIN_DATE: datetime.date = datetime.date(2017, 1, 1)
    # The maximum date value for the date interval filter.
    MAX_DATE: datetime.date = datetime.date(2022, 1, 1)
    # The list of available sorting options for the search results.
    sorting_options: List[str] = [
        "⬇️" + " " + _("relevance"),
        "⬇️" + " " + _("date"),
        "⬆️" + " " + _("date"),
    ]

    def __init__(self, search_results: SearchResults) -> None:
        """
        Initialize the SearchBar object with the specified SearchResults object.

        :param search_results: Used to store and display the search results.
        :type search_results: SearchResults
        """
        self._search_results = search_results
        self._init_state()

    def _init_state(self) -> None:
        """
        Initialize the state of the SearchBar object.

        :return: None
        :rtype: None
        """
        self.add_state("search_query", "")
        self.add_state("start_date", self.MIN_DATE)
        self.add_state("end_date", self.MAX_DATE)
        self.add_state("default_sorting_direction", self.sorting_options[0])

    def display_search_bar(self, column: st.DeltaGenerator) -> None:
        """
        Display the search bar with a text input for the search query.

        :param column: The column to display the search bar in.
        :type column: streamlit.DeltaGenerator

        :return: None
        :rtype: None
        """
        column.write("")
        column.write("")
        search_query = column.text_input(
            label="Search",
            placeholder=_("Write a search query"),
            label_visibility="collapsed",
            value=self.get_state("search_query"),
        )
        # need store also current value of search query
        # for correct displaying after return from second page
        self.set_state("search_query", search_query)

    def display_date_interval(self, column: st.DeltaGenerator) -> None:
        """
        Display a date interval filter to search for results within a specified time period.

        :param column: The column to display the date interval filter in.
        :type column: streamlit.DeltaGenerator

        :return: None
        :rtype: None
        """
        column.markdown(date_period_text(), unsafe_allow_html=True)
        date = column.date_input(
            label="Time period",
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
        """
        Call callback for the sorting direction selectbox.

        :return: None
        :rtype: None
        """
        self._search_results.sort_results_callback()
        self.set_state("default_sorting_direction", self.sorting_options[0])
        self.set_state("page_number", 1)

    def display_sorting_options(self, column: st.DeltaGenerator) -> None:
        """
        Display the sorting options for the search results.

        :param column: The column to display the sorting options in.
        :type column: streamlit.DeltaGenerator

        :return: None
        :rtype: None
        """
        column.markdown(sort_by_text(), unsafe_allow_html=True)
        column.selectbox(
            label="Sort by",
            label_visibility="collapsed",
            options=self.sorting_options,
            index=self.sorting_options.index(
                self.get_state("default_sorting_direction")
            ),
            key="sorting_direction",
            on_change=self._sorting_direction_callback,
        )

    def display_search_button(self, column: st.DeltaGenerator) -> None:
        """
        Display the search button to trigger the search.

        :param column: The column to display the search button in.
        :type column: streamlit.DeltaGenerator

        :return: None
        :rtype: None
        """
        column.write("")
        column.write("")
        column.button(
            # label_visibility="collapsed",
            label=_("Search"),
            type="primary",
            on_click=self._search_results.search_callback,
        )

    def display(self) -> None:
        """
        Display the search bar, filters, sorting options, and search button.

        :return: None
        :rtype: None
        """
        self._init_state()
        col1, col2, col3, col4 = st.columns([5, 2, 2, 1])

        self.display_search_bar(col1)
        self.display_date_interval(col2)
        self.display_sorting_options(col3)
        self.display_search_button(col4)
