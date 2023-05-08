from utils import keyboard, tokenize

class SpellCorrector():
    
    def __init__(self, lm, err, bor):
        self.lm = lm
        self.err = err
        self.bor = bor
        self.max_candidates = 10
   
    def fix_join(self, words):
        if len(words) < 2:
            return words
        joins = []
        for i in range(len(words) - 1):
            join = words[0:i]
            join.append(words[i] + words[i + 1])
            join.extend(words[i + 2:])
            joins.append(join)
        return joins
    
    def fix_split(self, words):
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
    
    def grammar_error_correct(self, words):
        list_of_candidates = []
        for word in words:
            candidates = list(map(lambda x: x[0], self.bor.search(word)))
            list_of_candidates.append(candidates)
        res = []
        candidates1 = list_of_candidates[0]  
        candidates1 = list(map(lambda x: [x], candidates1))  
        for i in range(1,len(list_of_candidates)):
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
                    res = sorted(res, key = lambda x: x[1],reverse = True)
            candidates1 = list(map(lambda x: x[0], res))
                
        return res

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