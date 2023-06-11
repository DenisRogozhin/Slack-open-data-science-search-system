"""Utils for app."""
import os
import gettext
from dataclasses import dataclass
import datetime
from time import sleep
from typing import List

from src.search_index.index import Index

inv = Index(os.path.join(os.path.dirname(__file__), "../../data.csv"))
inv.build()

# дамп/загрузка
inv.dump('index')
# inv.load('файл с дампом')


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
) -> list[Post]:
    # sleep(2)
    print("Query:", query)
    search_res = inv.search(query)
    print("Search results count:")
    print(len(search_res))

    result = []
    for _res in search_res:
        comments = []
        for _comment in _res[1]:
            comments.append(Comment(
                text=_comment[0], 
                author="", 
                datetime=datetime.datetime.fromisoformat(_comment[1]),
            ))
        post = Post(
            text=_res[0][0], 
            author="", 
            datetime=datetime.datetime.fromisoformat(_res[0][1]), 
            comments=comments,
        )
        result.append(post)

    return result


def sort_results(query: str, results: List[Post], sorting_direction: str) -> List[Post]:
    """Return query results."""
    return results
