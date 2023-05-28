from collections import defaultdict
import varbyte_encoding
import query_processing
import pandas as pd
import pickle


class Index:

    def __init__(self, filepath):
        self.index = defaultdict(list)
        self.filepath = filepath
        self.data = pd.read_csv(self.filepath, index_col=0).reset_index(drop=True)
        self.all_doc_ids = set(self.data.index)


    def build(self, compress = False):
        self.post_main_id = self.data.sort_values(by=['file', 'ts'], ascending=[True, True]).groupby('file').head(1)\
                                    .reset_index().groupby('file').agg({'index': list})['index'].to_dict()        

        for i, row in self.data.iterrows():
            tokens = row['lemmatize_text'].split(' ')

            for tok in tokens:
                self.index[tok].append(i)
        
        if compress:
            self.compress()


    def compress(self):
        for tok in self.index.keys():
            self.index[tok] = varbyte_encoding.compress(self.index[tok])


    def decompress_ids(self, ids):
        return varbyte_encoding.decompress(ids)


    def search(self, query):
        query_poliz = query_processing.build_search_structure(query)
        found_doc_ids = query_processing.find_doc_ids(query_poliz, self.index, self.all_doc_ids)

        post_names = self.data.loc[list(found_doc_ids)]['file'].values
        main_post_ids = sorted([(self.post_main_id[pn][0], pn) for pn in post_names],
                               key=lambda x: len(self.data.loc[x[0]]['lemmatize_text'].strip().split(' ')),
                               reverse=True)
        
        result = list()
        for pi, pn in main_post_ids:
            main_post_data = self.data.loc[pi][['text', 'ts']].tolist()
            comments_data = self.data.query(f'(file == "{pn}")').sort_values(by=['ts'], ascending=[True])\
                                                            .drop(index=[pi])[['text', 'ts']].values.tolist()
            result.append((main_post_data, comments_data))
        
        return result


    def dump(self, filepath):
        with open(filepath + 'index.pkl', mode='wb') as ind_f:
            pickle.dump(self.index, ind_f)

        dot = filepath.rfind('.')
        with open(filepath + 'index_post.pkl', mode='wb') as post_f:
            pickle.dump(self.post_main_id, post_f)


    def load(self, filepath):
        with open(filepath + 'index.pkl', mode='rb') as ind_f:
            self.index = pickle.load(ind_f)
        
        dot = filepath.rfind('.')
        with open(filepath + 'index_post.pkl', mode='rb') as post_f:
            self.post_main_id = pickle.load(post_f)
