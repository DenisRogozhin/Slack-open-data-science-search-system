import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="Search result",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    "<h1 style='text-align: center; color: purple;'>Search result 🗿</h1>",
    unsafe_allow_html=True,
)
st.write("")
st.write("")

st.write(st.session_state.start_date, st.session_state.end_date)

klick = st.button("Назад")
if klick:
    switch_page("App")
