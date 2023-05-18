from collections import defaultdict
import varbyte_encoding
import pickle


class Index:

    def __init__(self):
        self.index = defaultdict(list)


    def build(self, text_list=None):
        text_id = 0

        for text in text_list:
            tokens = text.split(' ')

            for tok in tokens:
                self.index[tok].append(text_id)
            text_id += 1

        self.compress()


    def compress(self):
        for tok in self.index.keys():
            self.index[tok] = varbyte_encoding.compress(self.index[tok])


    def decompress_ids(self, ids):
        return varbyte_encoding.decompress(ids)


    def search(self, query):
        pass


    def dump(self, filepath):
        with open(filepath, mode='wb') as ind_f:
            pickle.dump(self.index, ind_f)


    def load(self, filepath):
        with open(filepath, mode='rb') as ind_f:
            self.index = pickle.load(ind_f)
