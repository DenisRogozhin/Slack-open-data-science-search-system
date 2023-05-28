from playwright.sync_api import Page, expect

from .fixtures import before_module, before_test
from src.app.utils import _


def test_main_page_header(page: Page):
    expect(page).to_have_title("ODS dump search")


def test_empty_search_klick(page: Page):
    expect(page.get_by_text(_("No results"))).to_be_visible()

    page.get_by_role("button", name="Search").click()

    expect(page.get_by_text(_("No results"))).to_be_visible()


def test_sorting_direction_selectbox(page: Page):
    option_1_text = "⬇️" + " " + _("relevance")
    option_2_text = "⬇️" + " " + _("date")
    option_3_text = "⬆️" + " " + _("date")

    selectbox = page.locator("label").filter(has_text=_("Sort by")).locator("p")

    expect(selectbox).to_be_hidden()

    option_1 = page.get_by_text(option_1_text)
    option_2 = page.get_by_text(option_2_text)
    option_3 = page.get_by_text(option_3_text)

    expect(option_1).to_be_visible()
    expect(option_2).to_be_hidden()
    expect(option_3).to_be_hidden()


def test_search_bar(page: Page):
    expect(page.get_by_text(_("Write a search query"))).to_be_hidden()
