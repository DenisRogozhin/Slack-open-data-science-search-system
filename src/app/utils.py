"""Utils for app."""
import os
import gettext
from dataclasses import dataclass
import datetime
from time import sleep
from typing import List
import sys

import pandas as pd

import src.spellchecker.language_models as language_models
from src.spellchecker.spellchecker import SpellCorrector
from src.search_index.index import Index

# build index
inv = Index(os.path.join(os.path.dirname(__file__), "../../data/data.csv"))
inv.build()

# build spellchecker
sys.path.append(os.path.join(
    os.path.dirname(__file__), 
    "../spellchecker",
))
lm = pd.read_pickle(os.path.join(
    os.path.dirname(__file__), 
    "../spellchecker/models/language_model.pickle",
))
err = pd.read_pickle(os.path.join(
    os.path.dirname(__file__), 
    "../spellchecker/models/error_model.pickle",
))
bor = pd.read_pickle(os.path.join(
    os.path.dirname(__file__), 
    "../spellchecker/models/prefix_tree.pickle",
))
sc = SpellCorrector(lm, err, bor)


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
    print("Query:", query)
    corrected_query = " & ".join(sc.spellcorrect(query))
    print("Corrected query:", corrected_query)
    full_query = " & ".join(query.split()) + " | " + corrected_query
    print("Full query:", full_query)
    search_res = inv.search(full_query)

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

        if post.datetime.date >= start_date and post.datetime.date <= end_date:
            result.append(post)

    return sort_results(query, result, sorting_direction="relevance")


def sort_results(query: str, results: List[Post], sorting_direction: str) -> List[Post]:
    """Return query results."""
    return results
