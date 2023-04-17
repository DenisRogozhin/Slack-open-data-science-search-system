import numpy as np

def levenshtein_matrix(orig, fix):
    len_1 = len(orig) + 1
    len_2 = len(fix) + 1
    matrix = np.zeros((len_1, len_2))
    for i in range(len_1):
        matrix[i, 0] = i
    for j in range(len_2):
        matrix[0, j] = j
    for i in range(1, len_1):
        for j in range(1, len_2):
            matrix[i, j] = min(
                matrix[i - 1, j] + 1,
                matrix[i, j - 1] + 1,
                matrix[i - 1, j - 1] + int(orig[i - 1] != fix[j - 1])
            )
    return matrix

def levenshtein_dist(self, matrix):
    return matrix[matrix.shape[0] - 1, matrix.shape[1] - 1]

def find_mistakes_types(orig, fix, matrix):
    i = matrix.shape[0] - 1 
    j = matrix.shape[1] - 1
    way = []
    while i != 0 and j != 0:
        #print(i,j)
        m_up = matrix[i - 1, j]  #insert  
        m_left =  matrix[i, j - 1]  #del
        m_diag = matrix[i - 1, j - 1]  #replace
        if m_diag <= m_left and m_diag <= m_up:
            if orig[i-1] != fix[j-1]:
                way.append(('replace', fix[j-1], orig[i-1]))
            i = i - 1
            j = j - 1
        elif m_left < m_diag and m_left < m_up:
            way.append(('delete', fix[j-1]))
            j = j - 1
        else:
            way.append(('insert', orig[i-1]))
            i = i - 1
    return way[::-1]

class ErrorModel:

    def __init__(self):
        self.alpha = 5.0
        self.fixed_texts = []
        for x,y in fixed_texts:
            if len(x) == len(y):
                self.fixed_texts.append((x,y))
        self.replaces = defaultdict(int)
        self.inserts = defaultdict(int)
        self.deletions = defaultdict(int)
        
    def fit_words(self, orig, fix):
        matrix = levenshtein_matrix(orig, fix)
        errors = find_mistakes_types(orig, fix, matrix)
        for error in errors:
            if error[0] == 'replace':
                self.replaces[(error[1], error[2])] += 1
            elif error[0] == 'delete':
                self.deletions[error[1]] += 1
            elif error[0] == 'insert':
                self.inserts[error[1]] += 1
        return
    
    def fit(self, pairs_of_texts): 
        for text_pair in tqdm(pairs_of_texts):
            orig = text_pair[0]
            fix = text_pair[1]
            if len(orig) == len(fix):
                for i in range(len(orig)):
                    self.fit_words(orig[i], fix[i])
        return
    
    def P_err(self, orig, fix):
        pass