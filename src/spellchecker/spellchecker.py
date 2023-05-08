from utils import keyboard, tokenize

class SpellCorrector():
    
    def __init__(self, lm, err, bor):
        self.lm = lm
        self.err = err
        self.bor = bor
        self.max_candidates = 10
        
    def fix_layout(self, words):
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
        
    def spellcorrect(self, query):
        pass