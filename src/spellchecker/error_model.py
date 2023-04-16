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
        pass
    
    def fit(self, pairs_of_texts): 
        pass
    
    def P_err(self, orig, fix):
        pass