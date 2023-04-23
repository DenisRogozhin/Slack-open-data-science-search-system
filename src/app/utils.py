from dataclasses import dataclass
import datetime
from time import sleep


@dataclass
class Comment:
    text: str
    author: str
    datetime: datetime.datetime


@dataclass
class Post:
    text: str
    author: str
    datetime: datetime.datetime
    comments: list[Comment]


def search(
    query: str,
    start_date: datetime.date,
    end_date: datetime.date,
) -> list[Post]:
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


def sort_results(query: str, results: list[Post], sorting_direction: str) -> list[Post]:
    return results
