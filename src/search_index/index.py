from collections import defaultdict
import varbyte_encoding
import pandas as pd
import pickle


class Index:

    def __init__(self, filepath):
        self.index = defaultdict(list)
        self.filepath = filepath
        self.data = pd.read_csv(self.filepath, index_col=0).reset_index(drop=True)


    def build(self):
        self.post_main_id = self.data.sort_values(by=['file', 'ts'], ascending=[True, True]).groupby('file').head(1)\
                                    .reset_index().groupby('file').agg({'index': list})['index'].to_dict()        

        for i, row in self.data.iterrows():
            tokens = row['lemmatize_text'].split(' ')

            for tok in tokens:
                self.index[tok].append(i)
        
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

        dot = filepath.rfind('.')
        with open(filepath[:dot] + '_post' + filepath[dot:], mode='wb') as post_f:
            pickle.dump(self.post_main_id, post_f)


    def load(self, filepath):
        with open(filepath, mode='rb') as ind_f:
            self.index = pickle.load(ind_f)
        
        dot = filepath.rfind('.')
        with open(filepath[:dot] + '_post' + filepath[dot:], mode='rb') as post_f:
            self.post_main_id = pickle.load(post_f)
