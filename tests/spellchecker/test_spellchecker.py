import sys
sys.path.append('src/spellchecker')
from math import isclose


from language_models import BigramLanguageModel


def test_language_model():
    texts = ["мама мыла раму", "мама купила поесть"]
    lm = BigramLanguageModel()
    lm.fit(texts)
    assert(isclose(lm.P2('мама'), 2 / 6))
    assert(isclose(lm.P2('купила'), 1 / 6))
    assert(isclose(lm.P2('еда'), 0))
    assert(isclose(lm.P2('еда', smoothing = 'laplace'), 1 / 11))
    assert(isclose(lm.P2('купила', smoothing = 'laplace'), 2 / 11))
    assert(isclose(lm.P2('мама', smoothing = 'laplace'), 3 / 11))
    
    assert(isclose(lm.P2('мама мыла'), 2 / 12))
    assert(isclose(lm.P2('мама учила'), 0))
    
    assert(isclose(lm.P2('мама мыла', smoothing = 'laplace'), 6 / 77))
    assert(isclose(lm.P2('мама мыла', smoothing = 'jelinek-mercer'), 8 / 60))
    assert(isclose(lm.P2('мама мыла', smoothing = 'katz-smoothing'), 7 / 60))
    assert(isclose(lm.P2('мама мыла', smoothing = 'unreal-smoothing'), 2 / 12))