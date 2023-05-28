from contextlib import contextmanager
import os
from time import sleep

import pytest
from playwright.sync_api import Page


PORT = 8502


@contextmanager
def run_streamlit():
    """Run the streamlit app at examples/streamlit_app.py on port 8599"""
    import subprocess

    SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    ROOT_PATH = os.path.abspath(os.path.join(SRC_PATH, ".."))

    my_env = os.environ.copy()
    my_env["PYTHONPATH"] = f"{SRC_PATH}" + ":" + my_env.get("PYTHONPATH", "")

    p = subprocess.Popen(
        [
            "streamlit",
            "run",
            "src/app/MainPage.py",
            "--server.port",
            f"{PORT}",
        ],
        # cwd=ROOT_PATH,
        env=my_env,
        # shell=True,
    )

    sleep(5)

    try:
        yield 1
    finally:
        p.kill()


@pytest.fixture(scope="module", autouse=True)
def before_module():
    with run_streamlit():
        yield


@pytest.fixture(scope="function", autouse=True)
def before_test(page: Page):
    page.goto(f"localhost:{PORT}")
