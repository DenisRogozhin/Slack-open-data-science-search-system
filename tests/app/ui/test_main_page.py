from playwright.sync_api import Page, expect

from .fixtures import before_module, before_test
from src.app.utils import _


def test_main_page_header(page: Page):
    expect(page).to_have_title("ODS dump search")
