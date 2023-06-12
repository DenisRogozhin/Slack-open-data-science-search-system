"""Bigram language model to count text probabilities."""

from src.spellchecker.support_functions import tokenize
from collections import defaultdict
from typing import List, Tuple


class BigramLanguageModel:
    """Bigram language model to count text probabilities."""

    def __init__(self):
        """Init language model."""
        self.unigrams = defaultdict(int)
        self.bigrams = defaultdict(int)
        self.unigram_count = 0

        # for laplace smoothing
        self.alpha = 1

        # for jelinek-mercer-smoothing
        self.l2 = 0.7
        self.l1 = 0.3

    def fit(self, texts: List[str]):
        """Fit language model.

        :param texts: list of texts
        """
        for text in texts:
            words = tokenize(text)
            if len(words) > 0:
                self.unigram_count += 1
                self.unigrams[words[0]] += 1

            for i in range(1, len(words)):
                pair = (words[i - 1], words[i])
                self.bigrams[pair] += 1

                self.unigram_count += 1
                self.unigrams[words[i]] += 1

        self.W = len(self.unigrams)

    def __count_bigram_p(self, bigram: Tuple[str, str], prev_word: str,
                         word: str, smoothing: str) -> float:
        if not smoothing:
            if self.unigrams[prev_word] != 0:
                p = self.bigrams[bigram] / self.unigrams[prev_word]
            else:
                p = 0
        elif smoothing == 'laplace':
            p = ((self.bigrams[bigram] + self.alpha) /
                 (self.unigrams[prev_word] + self.W * self.alpha))
        elif smoothing == 'jelinek-mercer':
            if self.unigrams[prev_word] != 0:
                p = self.l2 * self.bigrams[bigram] / self.unigrams[prev_word]
            else:
                p = 0
            p += self.l1 * self.unigrams[word] / self.unigram_count
        elif smoothing == 'katz-smoothing':
            if self.unigrams[prev_word] != 0:
                p = self.l2 * self.bigrams[bigram] / self.unigrams[prev_word]
            else:
                p = 0
            if p == 0:
                p = self.l1 * self.unigrams[word] / self.unigram_count
        return p

    def __count_unigram_p(self, word: str, smoothing: str) -> float:
        if smoothing != 'laplace':
            smoothing = None
        if not smoothing:
            p = self.unigrams[word] / self.unigram_count
        elif smoothing == 'laplace':
            p = (self.unigrams[word] + self.alpha) / (self.unigram_count + self.alpha * self.W)
        return p

    def P2(self, text: str, smoothing: str = None) -> float:
        """Count text probability with fitted model.

        :param text: text to count probability
        :param smoothing: type of smoothing to use:
                          [None, 'laplace', 'jelinek-mercer', 'katz-smoothing']
        :return: probability of the given text
        """
        words = tokenize(text)
        p = 1
        if smoothing not in [None, 'laplace', 'jelinek-mercer', 'katz-smoothing']:
            print('bad smoothing, changed to None')
            smoothing = None
        # P(w1 ... wn) = p(wn| w(n-1)) * ... * p(w3| w2) * p(w2| w1) * p(w1)

        if len(words) > 0:
            p *= self.__count_unigram_p(words[0], smoothing)
        for i in range(1, len(words)):
            bigram = (words[i - 1], words[i])
            prev_word = words[i - 1]
            word = words[i]
            p *= self.__count_bigram_p(bigram, prev_word, word, smoothing)
        return p
