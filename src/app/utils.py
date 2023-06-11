"""Utils for app."""
import os
import gettext
from dataclasses import dataclass
import datetime
from time import sleep
from typing import List


translation = gettext.translation(
    domain="app",
    localedir=os.path.join(os.path.dirname(__file__), "../locales"),
    languages=["en", "ru"],
)
_, ngettext = translation.gettext, translation.ngettext


@dataclass
class Comment:
    """Comment."""

    text: str
    author: str
    datetime: datetime.datetime


@dataclass
class Post:
    """Post."""

    text: str
    author: str
    datetime: datetime.datetime
    comments: List[Comment]


def search(
    query: str,
    start_date: datetime.date,
    end_date: datetime.date,
) -> List[Post]:
    """Search relevant posts for query."""
    sleep(2)
    comments = [
        Comment(
            text="; ".join(100 * [f"comment text {i}"])
            if i % 2 == 0
            else f"comment text {i}",
            author=f"comment author {i}",
            datetime=datetime.datetime.now(),
        )
        for i in range(20)
    ]
    return [
        Post(
            text="; ".join(100 * [f"post text {i}"])
            if i % 2 == 0
            else f"post text {i}",
            author=f"post author {i}",
            comments=comments,
            datetime=datetime.datetime.now(),
        )
        for i in range(30)
    ]


def sort_results(query: str, results: List[Post], sorting_direction: str) -> List[Post]:
    """Return query results."""
    return results
