import datetime
import logging
import random
import re

import streamlit as st
import streamlit.components.v1 as components

from utils import search


logging.basicConfig(format="\n%(asctime)s\n%(message)s", level=logging.INFO, force=True)

MIN_DATE = datetime.date(2017, 1, 1)
MAX_DATE = datetime.date(2022, 1, 1)

# ----- Page header ------

st.set_page_config(page_title="ODS dump search", page_icon="🤖", layout="wide")

# st.write(
#     """<style>
#     [data-testid="column"] {
#         width: calc(50% - 1rem);
#         flex: 1 1 calc(50% - 1rem);
#         min-width: calc(50% - 1rem);
#     }
#     </style>""",
#     unsafe_allow_html=True,
# )


st.markdown(
    "<h1 style='text-align: center; color: purple;'>ODS dump search system 🗿</h1>",
    unsafe_allow_html=True,
)
st.write("")
st.write("")
# st.title(":blue[ODS dump search system] 🗿")

# ----- Utils ------

if "search_result" not in st.session_state:
    st.session_state.search_result = None
if "start_date" not in st.session_state:
    st.session_state.start_date = MIN_DATE
if "end_date" not in st.session_state:
    st.session_state.end_date = MAX_DATE


def search_callback(query: str, start_date: datetime.date, end_date: datetime.date):
    if query:
        st.session_state.search_result = search(query, start_date, end_date)
    else:
        st.session_state.search_result = None


# ----- Query paraneters ------

col1, col2, col3, col4 = st.columns([5, 2, 2, 1])
# query input
query = col1.text_input(
    label="Search",
    placeholder="Введите поисковый запрос",
    label_visibility="collapsed",
)

date = col2.date_input(
    "Time period",
    value=[MIN_DATE, MAX_DATE],
    min_value=MIN_DATE,
    max_value=MAX_DATE,
    label_visibility="collapsed",
)
# update date range
if len(date) == 2:
    st.session_state.start_date = date[0]
    st.session_state.end_date = date[1]
elif len(date) == 1:
    st.session_state.start_date = date[0]
    st.session_state.end_date = MAX_DATE

sorting = col3.selectbox(
    "Ранжировать",
    ["⬇️ по дате", "⬆️ по дате", "⬇️ по релевантности"],
    label_visibility="collapsed",
)

# search button
search_button = col4.button(
    label="Найти",
    type="primary",
    # on_click=search_callback,
    # args=(query, st.session_state.start_date, st.session_state.end_date),
)

# ----- Search results ------

st.write("")
st.write("")

_, center, _ = st.columns([3, 2, 2])

with center:
    if search_button:
        with st.spinner("Поиск..."):
            if query:
                st.session_state.search_result = search(
                    query, st.session_state.start_date, st.session_state.end_date
                )
            else:
                st.session_state.search_result = None

    if st.session_state.search_result is not None:
        for i, search_result in enumerate(st.session_state.search_result):
            st.button(
                label=f"Результат поиска {i}",
                type="primary",
                # on_click=search,
                # args=(query, st.session_state.start_date, st.session_state.end_date),
            )
    else:
        st.caption("_Ничего не найдено_  ̄\\\_(ツ)\_/ ̄")
        st.caption("_Попробуйте изменить  запрос_")
