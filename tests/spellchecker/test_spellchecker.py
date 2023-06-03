import sys
sys.path.append('src/spellchecker')
from math import isclose
import numpy as np
from error_model import levenshtein_matrix, levenshtein_dist, find_mistakes_types, ErrorModel
from language_models import BigramLanguageModel


def test_language_model():
    texts = ["мама мыла раму", "мама купила поесть"]
    lm = BigramLanguageModel()
    lm.fit(texts)
    assert (isclose(lm.P2('мама'), 2/6))
    assert (isclose(lm.P2('купила'), 1/6))
    assert (isclose(lm.P2('еда'), 0))
    assert (isclose(lm.P2('еда', smoothing='laplace'), 1 / 11))
    assert (isclose(lm.P2('купила', smoothing='laplace'), 2 / 11))
    assert (isclose(lm.P2('мама', smoothing='laplace'), 3 / 11))
    assert (isclose(lm.P2('мама мыла'), 2 / 12))
    assert (isclose(lm.P2('мама учила'), 0))
    assert (isclose(lm.P2('мама мыла', smoothing='laplace'), 6 / 77))
    assert (isclose(lm.P2('мама мыла', smoothing='jelinek-mercer'), 8 / 60))
    assert (isclose(lm.P2('мама мыла', smoothing='katz-smoothing'), 7 / 60))
    assert (isclose(lm.P2('мама мыла', smoothing='unreal-smoothing'), 2 / 12))


def test_levenshtein_matrix():
    fix = "боец"
    orig = "берцы"
    matr = np.array([
                    [0, 1, 2, 3, 4],
                    [1, 0, 1, 2, 3],
                    [2, 1, 1, 1, 2],
                    [3, 2, 2, 2, 2],
                    [4, 3, 3, 3, 2],
                    [5, 4, 4, 4, 3],
                    ])
    assert ((levenshtein_matrix(orig, fix) == matr).all().all())


def test_levenshtein_dist():
    fix = "боец"
    orig = "берцы"
    matr = levenshtein_matrix(orig, fix)
    assert ((levenshtein_dist(matr) == 3))


def test_mistakes_types():
    fix = "боец"
    orig = "берцы"
    res = [('replace', 'о', 'е'), ('replace', 'е', 'р'), ('insert', 'ы')]
    matr = levenshtein_matrix(orig, fix)
    assert ((find_mistakes_types(orig, fix, matr) == res))


def test_error_model():
    data = [('привет', 'прпвет')]
    err = ErrorModel()
    err.fit(data)
    assert (err.P_err('пр', 'пр') == 1)
    assert (isclose(err.P_err('пр', 'пъ'), 2 / 3))
    assert (isclose(err.P_err('пр', 'п'), 2 / 3))
    assert (isclose(err.P_err('п', 'пр'), 2 / 3))
