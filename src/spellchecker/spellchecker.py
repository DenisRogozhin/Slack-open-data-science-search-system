from utils import keyboard, tokenize

class SpellCorrector():
    
    def __init__(self, lm, err, bor):
        self.lm = lm
        self.err = err
        self.bor = bor
        self.max_candidates = 10
        
    def spellcorrect(self, query):
        pass