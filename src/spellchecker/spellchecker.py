"""Realisation of SpellCorrector class."""
from utils import keyboard, tokenize
from language_models import BigramLanguageModel
from error_model import ErrorModel
from prefix_tree import Bor
from typing import List


class SpellCorrector():
    """Realisation of SpellCorrector."""

    def __init__(self, lm: BigramLanguageModel, err: ErrorModel, bor: Bor):
        """Init SpellCorrector with error model, prefix tree and language model.

        :param lm: language model
        :param err: error model
        :param bor: prefix tree
        """
        self.lm = lm
        self.err = err
        self.bor = bor
        self.max_candidates = 10

    def fix_join(self, words: List[str]) -> List[str]:
        """Join words to fox split error.

        :param words: list of words
        :return: list of fixing candidates
        """
        if len(words) < 2:
            return [words]
        joins = []
        for i in range(len(words) - 1):
            join = words[0:i]
            join.append(words[i] + words[i + 1])
            join.extend(words[i + 2:])
            joins.append(join)
        return joins

    def fix_split(self, words: List[str]) -> List[str]:
        """Separate words to fox join error.

        :param words: list of words
        :return: list of fixing candidates
        """
        splits = []
        for i in range(len(words)):
            word = words[i]
            for j in range(1, len(word)):
                split = words[0:i]
                split.append(word[0:j])
                split.append(word[j:])
                split.extend(words[i + 1:])
                splits.append(split)
        return splits

    def grammar_error_correct(self, words: List[str]) -> List[str]:
        """Fix grammar error in the word.

        :param words: list of words
        :return: list of fixing candidates
        """
        list_of_candidates = []
        for word in words:
            candidates = list(map(lambda x: x[0], self.bor.search(word)))
            list_of_candidates.append(candidates)
        res = []
        candidates1 = list_of_candidates[0]
        candidates1 = list(map(lambda x: [x], candidates1))
        if len(list_of_candidates) < 2:
            res = []
            for word1 in candidates1:
                cost = self.lm.P2(" ".join(word1))
                if len(res) < self.max_candidates:
                    res.append((word1, cost))
                else:
                    if cost > res[-1][1]:
                        res[-1] = (word1, cost)
                res = sorted(res, key=lambda x: x[1], reverse=True)
            return res    
        for i in range(1, len(list_of_candidates)):
            res = []
            candidates2 = list_of_candidates[i]
            for word1 in candidates1:
                for word2 in candidates2:
                    cost = self.lm.P2(" ".join(word1 + [word2]))
                    if len(res) < self.max_candidates:
                        res.append((word1 + [word2], cost))
                    else:
                        if cost > res[-1][1]:
                            res[-1] = (word1 + [word2], cost)
                    res = sorted(res, key=lambda x: x[1], reverse=True)
            candidates1 = list(map(lambda x: x[0], res))

        return res

    def fix_layout(self, words: List[str]) -> List[str]:
        """Fix layout error in the word.

        :param words: list of words
        :return: list with fixing candidates
        """
        query = []
        for word in words:
            new_word = ""
            for char in word:
                if char in keyboard:
                    new_word += keyboard[char]
                else:
                    new_word += char
            query.append(new_word)
        return query

    def spellcorrect(self, query: str) -> List[str]:
        """Correct error in the query.

        :param query: user query
        :return: best fixing candidate
        """
        tokens = tokenize(query)
        for i in range(2):
            grammar_fixes = list(map(lambda x: x[0], self.grammar_error_correct(tokens)))
            splits = self.fix_split(tokens)
            joins = self.fix_join(tokens)
            layouts = [self.fix_layout(tokens)]

            candidates = grammar_fixes + splits + joins + layouts

            uniq_candidates = []
            for candidate in candidates:
                if candidate not in uniq_candidates:
                    uniq_candidates.append((candidate,
                                            self.lm.P2((" ".join(candidate)), smoothing=None),
                                            self.err.P_err(query, " ".join(candidate))))

            uniq_candidates = sorted(uniq_candidates, key=lambda x: x[1], reverse=True)
            res = uniq_candidates[0][0]

            if tokens == res:
                break
            else:
                tokens = res
                query = " ".join(tokens)

        return res
