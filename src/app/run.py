"""Run MainPage code."""

import os


path = os.path.join(os.path.dirname(__file__), 'MainPage.py')
os.system(f'streamlit run {path}')
