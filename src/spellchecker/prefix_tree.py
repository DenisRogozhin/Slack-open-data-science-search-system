from utils import tokenize

class Bor():
    
    def __init__(self, error_model):
        pass
    
    def fit(self, correct_queries):
        for query in correct_queries:
            query = tokenize(query)
            for word in query:
                self.add(word)
    
    def add(self, word):
        pass
    
    def get_prefix_freq(self, prefix):
        pass
    
    def search(self, orig):
        pass
    