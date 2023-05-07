from utils import tokenize

class Node():
    def __init__(self, word=None):
        self.word = word
        self.children = dict()
        self.freq = 0

class Bor():
    
    def __init__(self, error_model):
        self.error_model = error_model
        self.tree = Node()
        self.alpha = 0.01
        self.beta = 1
        self.max_queue_len = 100
        self.max_candidates = 20
    
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
        current = self.tree.children
        n = len(prefix)
        if n == 0:
            return 1
        for i in range(n - 1):
            if prefix[i] not in current:
                return 0
            current = current[prefix[i]].children
        if prefix[n - 1] not in current:
            return 0
        return current[prefix[n - 1]].freq
    
    def search(self, orig):
        current = self.tree
        fix = ""
        cur_len = 0
        queue = []
        candidates = []
        ins_cnt = 0
        del_cnt = 0
        
        while len(candidates) < self.max_candidates:
            if abs(len(fix) - len(orig)) <= 1 and current.word is not None:
                candidates.append(fix)
            cur_len = cur_len + 1
            for letter in current.children:
                cost = (self.alpha * np.log2(self.get_prefix_freq(fix + letter)) + self.beta * 
                                    self.error_model.P_err(orig[:cur_len], fix + letter))
                
                if len(queue) < self.max_queue_len:
                    queue.append((fix + letter, cost, current.children[letter], cur_len, ins_cnt, del_cnt))
                elif cost > queue[self.max_queue_len - 1][1]:
                    queue[self.max_queue_len - 1] = (fix + letter, cost, current.children[letter], cur_len, ins_cnt, del_cnt)
                queue = sorted(queue, key = lambda x: x[1],reverse = True)
    
            if len(queue) <= 0:
                return candidates
            fix, cost, current, cur_len, ins_cnt, del_cnt = queue[0]
            queue.remove(queue[0])
        return candidates