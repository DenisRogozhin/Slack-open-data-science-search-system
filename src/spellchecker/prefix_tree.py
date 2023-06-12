"""Realisation of Prefix tree with fixed words search."""
import sys
sys.path.append('.')
from src.spellchecker.support_functions import tokenize
from src.spellchecker.error_model import ErrorModel
from typing import List


class Node():
    """Realisation of Prefix tree node."""

    def __init__(self, word: str = None):
        """Init node of the prefix tree.

        :param word: word in the current node
        """
        self.word = word
        self.children = dict()
        self.freq = 0


class Bor():
    """Realisation of Prefix tree."""

    def __init__(self, error_model: ErrorModel):
        """Init prefix tree.

        :param error_model: trained error model
        """
        self.error_model = error_model
        self.tree = Node()
        self.alpha = 0.01
        self.beta = 1
        self.max_queue_len = 100
        self.max_candidates = 20

    def fit(self, correct_queries: List[str]):
        """Fit prefix tree with words.

        :param correct_queries: list of queries
        """
        for query in correct_queries:
            query = tokenize(query)
            for word in query:
                self.add(word)

    def add(self, word: str):
        """Add word to the prefix tree.

        :param word: word to add
        """
        current = self.tree.children
        n = len(word)
        if n == 0:
            return
        for i in range(n - 1):
            if word[i] not in current:
                new_node = Node()
                current[word[i]] = new_node
            current[word[i]].freq += 1
            current = current[word[i]].children
        if word[n - 1] not in current:
            new_node = Node(word)
            current[word[n - 1]] = new_node
            current[word[n - 1]].freq += 1
        else:
            current[word[n - 1]].freq += 1
            if current[word[n - 1]].word is None:
                current[word[n - 1]].word = word

    def get_prefix_freq(self, prefix: str) -> int:
        """Count frequence of the prefix in the tree.

        :param prefix: prefix to find
        :return: prefix frequence
        """
        current = self.tree.children
        n = len(prefix)
        if n == 0:
            return 1
        for i in range(n - 1):
            if prefix[i] not in current:
                return 0
            current = current[prefix[i]].children
        if prefix[n - 1] not in current:
            return 0
        return current[prefix[n - 1]].freq

    def search(self, word: str, max_lev: int = 2) -> List[str]:
        """Search words, which are close to the given word.

        :param word: word to find fixes
        :param max_lev: max levenshtein distance between given word and word from tree
        :return: list of close words
        """
        res = []
        first_row = [i for i in range(len(word) + 1)]
        for letter in self.tree.children:
            self._search(self.tree.children[letter], letter, word, first_row, res, max_lev)
        return res

    def _search(self, node: Node, letter: str, word: str, prev_row: List[int],
                res: List[str], max_lev: int):
        """Search words, which are close to the given word in the current node.

        :param node: current node
        :param letter: current letter in the tree
        :param word: word to find fixes
        :param prev_row: prev row of levenshtein matrix
        :param res: kist of result words
        :param max_lev: max levenshtein distance between given word and word from tree
        """
        cur_row = self.levenstein_iter(prev_row, word, letter)
        if cur_row[-1] <= max_lev and node.word:
            res.append([node.word, cur_row[-1]])

        if min(cur_row) <= max_lev:
            for letter in node.children:
                self._search(node.children[letter], letter, word, cur_row, res, max_lev)

    def levenstein_iter(self, prev_row: List[int], word: str, letter: str) -> List[int]:
        """Count next row of levenshtein matrix.

        :param prev_row: prev row of levenshtein matrix
        :param word: word to find fixes
        :param letter: current letter in the tree
        :return: next row of levenshtein matrix
        """
        cur_row = [prev_row[0] + 1]
        for column in range(1, len(word) + 1):
            insert_cost = cur_row[column - 1] + 1
            delete_cost = prev_row[column] + 1
            replace_cost = prev_row[column - 1] + int(word[column - 1] != letter)
            cur_row.append(min(insert_cost, delete_cost, replace_cost))
        return cur_row
