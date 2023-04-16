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


class ErrorModel:

    def __init__(self):
        pass
    
    def fit(self, pairs_of_texts): 
        pass
    
    def P_err(self, orig, fix):
        pass