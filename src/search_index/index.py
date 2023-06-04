"""Implementation of inverted search index."""
from collections import defaultdict
from typing import List, Tuple

import pandas as pd
import pickle
import bitstring

import src.search_index.varbyte_encoding as varbyte_encoding
import src.search_index.query_processing as query_processing

class Index:
    """Inverted search index class."""

    def __init__(self, filepath: str):
        """Init Index.

        :param filepath: file with data for search
        """
        self.index = defaultdict(list)
        self.filepath = filepath
        self.data = pd.read_csv(self.filepath, index_col=0).reset_index(drop=True)
        self.all_doc_ids = set(self.data.index)

    def build(self, compress: bool = False):
        """Build inverted index for given data.

        :param compress: if True then use compression with VarByte encoding
        """
        self.post_main_id = self.data.sort_values(by=['file', 'ts'],
                                                  ascending=[True, True])\
            .groupby('file').head(1).reset_index().groupby('file')\
            .agg({'index': list})['index'].to_dict()

        for i, row in self.data.iterrows():
            tokens = row['lemmatize_text'].split(' ')

            for tok in tokens:
                self.index[tok].append(i)

        if compress:
            self.compress()

    def compress(self):
        """Compress index with VarByte encoding."""
        for tok in self.index.keys():
            self.index[tok] = varbyte_encoding.compress(self.index[tok])

    def decompress_ids(self, ids: bitstring.BitStream) -> List[int]:
        """Decompress index for one term from VarByte encoding."""
        return varbyte_encoding.decompress(ids)

    def search(self, query: str) -> List[Tuple[str, str]]:
        """Search for user query.

        :param query: query from user
        """
        query_poliz = query_processing.build_search_structure(query)
        found_doc_ids = query_processing.find_doc_ids(query_poliz, self.index, self.all_doc_ids)

        post_names = self.data.loc[list(found_doc_ids)]['file'].values
        main_post_ids = sorted([(self.post_main_id[pn][0], pn) for pn in post_names],
                               key=lambda x: len(self.data.loc[x[0]]['lemmatize_text']
                                                 .strip().split(' ')),
                               reverse=True)

        main_post_ids = main_post_ids[:min(len(main_post_ids), 10)]
        result = list()
        for pi, pn in main_post_ids:
            main_post_data = self.data.loc[pi][['text', 'ts']].tolist()
            comments_data = self.data.query(f'(file == "{pn}")')\
                .sort_values(by=['ts'], ascending=[True])\
                .drop(index=[pi])[['text', 'ts']].values.tolist()
            result.append((main_post_data, comments_data))

        return result

    def dump(self, filepath):
        """Dump index.

        :param filepath: path .pickle files
        """
        with open(filepath + 'index.pkl', mode='wb') as ind_f:
            pickle.dump(self.index, ind_f)

        with open(filepath + 'index_post.pkl', mode='wb') as post_f:
            pickle.dump(self.post_main_id, post_f)

    def load(self, filepath):
        """Load index from dumps.

        :param filepath: path .pickle files
        """
        with open(filepath + 'index.pkl', mode='rb') as ind_f:
            self.index = pickle.load(ind_f)

        with open(filepath + 'index_post.pkl', mode='rb') as post_f:
            self.post_main_id = pickle.load(post_f)
