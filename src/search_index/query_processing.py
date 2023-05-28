import re

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
                    raise ValueError('Must be \')\'')
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
