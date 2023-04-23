"""Realisation of Error model and some support functions."""

import numpy as np
from collections import defaultdict


def levenshtein_matrix(orig, fix):
    """Count levenshtein matrix for twho given words.

    :param orig: word with mistake
    :param fix: correct word
    :return: np.array(shape=(len(orig) + 1, len(fix) + 1)) - levenshtein matrix
    """
    len_1 = len(orig) + 1
    len_2 = len(fix) + 1
    matrix = np.zeros((len_1, len_2))
    for i in range(len_1):
        matrix[i, 0] = i
    for j in range(len_2):
        matrix[0, j] = j
    for i in range(1, len_1):
        for j in range(1, len_2):
            matrix[i, j] = min(
                matrix[i - 1, j] + 1,
                matrix[i, j - 1] + 1,
                matrix[i - 1, j - 1] + int(orig[i - 1] != fix[j - 1])
            )
    return matrix


def levenshtein_dist(self, matrix):
    """Count levenshtein distance with given levenshtein matrix.

    :param matrix: levenshtein matrix
    :return: levenshtein distance
    """
    return matrix[matrix.shape[0] - 1, matrix.shape[1] - 1]


def find_mistakes_types(orig, fix, matrix):
    """Find types of mistakes in the original word with the fixed word given.

    :param orig: word with mistake
    :param fix: correct word
    :param matrix: levenshtein matrix
    :return: List of mistakes types: ('replace', a, b), ('delete', a), ('insert', a)
    """
    i = matrix.shape[0] - 1
    j = matrix.shape[1] - 1
    way = []
    while i != 0 and j != 0:
        m_up = matrix[i - 1, j]  # insert
        m_left = matrix[i, j - 1]  # del
        m_diag = matrix[i - 1, j - 1]  # replace
        if m_diag <= m_left and m_diag <= m_up:
            if orig[i-1] != fix[j-1]:
                way.append(('replace', fix[j-1], orig[i-1]))
            i = i - 1
            j = j - 1
        elif m_left < m_diag and m_left < m_up:
            way.append(('delete', fix[j-1]))
            j = j - 1
        else:
            way.append(('insert', orig[i-1]))
            i = i - 1
    return way[::-1]


class ErrorModel:
    """Realisation of Error model."""

    def __init__(self):
        """Init Error model."""
        self.alpha = 5.0
        self.replaces = defaultdict(int)
        self.inserts = defaultdict(int)
        self.deletions = defaultdict(int)

    def fit_words(self, orig, fix):
        """Add pair of (orig, fix) words to error model.

        :param orig: word with mistake
        :param fix: correct word
        """
        matrix = levenshtein_matrix(orig, fix)
        errors = find_mistakes_types(orig, fix, matrix)
        for error in errors:
            if error[0] == 'replace':
                self.replaces[(error[1], error[2])] += 1
            elif error[0] == 'delete':
                self.deletions[error[1]] += 1
            elif error[0] == 'insert':
                self.inserts[error[1]] += 1

    def fit(self, pairs_of_texts):
        """Add pairs of (orig, fix) words to error model.

        :param pairs_of_texts: list of texts (orig, fix)
        :param fix: correct word
        """
        for text_pair in pairs_of_texts:
            orig = text_pair[0]
            fix = text_pair[1]
            if len(orig) == len(fix):
                for i in range(len(orig)):
                    self.fit_words(orig[i], fix[i])

    def levenstein(self, orig, fix):
        """Count modified levenstein distance between orig and fix.

        :param orig: word with mistake
        :param fix: correct word
        :return: levenshtein distance
        """
        matrix = levenshtein_matrix(orig, fix)
        errors = find_mistakes_types(orig, fix, matrix)
        dist = 0
        for error in errors:
            if error[0] == 'replace':
                dist += (self.replaces[(error[1], error[2])] /
                         sum([self.replaces[x] for x in self.replaces if x[0] == error[1]]))
            elif error[0] == 'delete':
                dist += (self.deletions[error[1]] / sum([self.deletions[x] for x in self.deletions]))
            elif error[0] == 'insert':
                dist += (self.inserts[error[1]] / sum([self.inserts[x] for x in self.inserts]))
        return dist

    def P_err(self, orig, fix):
        """Count P(orig|fix).

        :param orig: word with mistake
        :param fix: correct word
        :return: P(orig|fix)
        """
        return self.alpha ** (-self.levenstein(orig, fix))
