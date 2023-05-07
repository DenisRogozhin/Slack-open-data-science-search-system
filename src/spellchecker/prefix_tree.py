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
        current = self.tree.children
        n = len(word)
        if n == 0:
            return
        for i in range(n - 1):
            if word[i] not in current:
                new_node = Node()
                current[word[i]] = new_node
            current[word[i]].freq += 1
            current = current[word[i]].children
        if word[n - 1] not in current:
            new_node = Node(word)
            current[word[n - 1]] = new_node
            current[word[n - 1]].freq += 1
        else:
            current[word[n - 1]].freq += 1
            if current[word[n - 1]].word is None:
                current[word[n - 1]].word = word
    
    def get_prefix_freq(self, prefix):
        pass
    
    def search(self, orig):
        pass
    