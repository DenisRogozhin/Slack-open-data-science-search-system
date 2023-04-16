from nltk import word_tokenize
from collections import defaultdict

class BigramLanguageModel: 

    def __init__(self):
        self.unigrams = defaultdict(int)
        self.bigrams = defaultdict(int)
        self.unigram_count = 0
        
        #for laplace smoothing
        self.alpha = 1
        
        #for jelinek-mercer-smoothing
        self.l2 = 0.7
        self.l1 = 0.3
    
    def fit(self, texts):
        for text in texts:
            words = word_tokenize(text.lower())
            if len(words) > 0:
                self.unigram_count += 1
                self.unigrams[words[0]] += 1
            
            for i in range(1, len(words)):              
                pair = (words[i - 1], words[i])
                self.bigrams[pair] += 1
                
                self.unigram_count += 1
                self.unigrams[words[i]] += 1
                
        self.W = len(self.unigrams)
        self.dictionary = set(self.unigrams.keys())
    
    def P2(self, text, smoothing=None):
        pass