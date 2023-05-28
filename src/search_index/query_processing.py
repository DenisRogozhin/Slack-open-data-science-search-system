import re
from collections import deque
import varbyte_encoding

REGEX_SPLIT = re.compile(r'\w+|[\(\)\|&!]', re.U)


def tokenize(query_str):
    return list(map(lambda t: t.lower(), re.findall(REGEX_SPLIT, query_str)))


def tokenized_query_to_poliz(tokens):
    priors = {
        '|': 0,
        '&': 1,
        '!': 2
    }

    tokens = list(reversed(tokens))

    def to_poliz(tokens, prev_prior):
        res = list()

        while len(tokens) > 0:
            tok = tokens.pop()

            if tok == '(':
                bracket_expr = to_poliz(tokens, 0)
                tok = tokens.pop()
                if tok != ')':
                    raise ValueError("Must be ')'")
                res += bracket_expr
                continue
            if tok == ')':
                tokens.append(')')
                break

            if tok in priors:
                if priors[tok] < prev_prior:
                    tokens.append(tok)
                    break

                right = to_poliz(tokens, priors[tok])
                res += right + [tok]

            else:
                res.append(tok)
        return res

    return to_poliz(tokens, 0)


def build_search_structure(query_str):
    tokens = tokenize(query_str)
    return tokenized_query_to_poliz(tokens)


def find_doc_ids(poliz, index, all_doc_ids, decompress=False):
    rest = deque(poliz)
    ids_stack = list()
    ops = {
        '|': lambda x, y: x | y,
        '&': lambda x, y: x & y,
        '!': lambda x: all_doc_ids - x
    }

    while len(rest) > 0:
        tok = rest.popleft()

        if tok in ops:
            if tok in ['&', '|']:
                right, left = ids_stack.pop(), ids_stack.pop()
                ids_stack.append(ops[tok](left, right))
            elif tok == '!':
                right = ids_stack.pop()
                ids_stack.append(ops[tok](right))
        else:
            if decompress:
                ids_stack.append(set(varbyte_encoding.decompress(index[tok])))
            else:
                ids_stack.append(set(index[tok]))

    return ids_stack[0]
