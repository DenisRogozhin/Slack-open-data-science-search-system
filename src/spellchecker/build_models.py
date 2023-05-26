import pandas as pd
from language_models import BigramLanguageModel
from error_model import ErrorModel
from utils import tokenize
from prefix_tree import Bor
import sys

sys.setrecursionlimit(2000)


def build_language_model(texts):
    model = BigramLanguageModel()
    model.fit(texts)
    pd.to_pickle(model, 'models/language_model.pickle')


def build_error_model(fixed_texts):
    err = ErrorModel()
    err.fit(fixed_texts)
    pd.to_pickle(err, 'models/error_model.pickle')
    return err


def build_prefix_tree(err, texts):
    bor = Bor(err)
    bor.fit(texts)
    pd.to_pickle(bor, 'models/prefix_tree.pickle')


def get_fixes(texts):
    res = []
    for text in texts:
        parts = text.split('\t')
        if len(parts) > 1:
            res.append((tokenize(parts[0]), tokenize(parts[1])))
    return res


if __name__ == "__main__":
    data = pd.read_csv('data.csv')
    texts = data.text.values
    build_language_model(texts)
#    with open('queries_all.txt', 'r', encoding='utf-8') as f:
#        lines = f.read().split('\n')
#    fixed_texts = get_fixes(lines)
#    err = build_error_model(fixed_texts)
    err = pd.read_pickle('models/error_model.pickle')
    build_prefix_tree(err, texts)
