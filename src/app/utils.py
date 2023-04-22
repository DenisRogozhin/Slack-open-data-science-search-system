from dataclasses import dataclass
import datetime
from time import sleep


@dataclass
class Comment:
    id: int
    text: str
    author: str


@dataclass
class Post:
    id: int
    text: str
    author: str
    comments: list[Comment]
    snippet: str = ""


def search(
    query: str,
    start_date: datetime.date,
    end_date: datetime.date,
) -> list[Post]:
    sleep(2)
    comments = [
        Comment(id=i, text=f"comment text {i}", author=f"author {i}") for i in range(20)
    ]
    return [
        Post(id=i, text=f"post text {i}", author=f"author {i}", comments=comments)
        for i in range(30)
    ]


def sort_results(query: str, results: list[Post], sorting_direction: str) -> list[Post]:
    return results
