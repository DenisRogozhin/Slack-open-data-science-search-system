"""Implementation of inverted search index."""
from collections import defaultdict
import varbyte_encoding
import query_processing
import pandas as pd
import pickle
import bitstring
from typing import List, Tuple


class Index:
    """Inverted search index class."""

    def __init__(self, filepath: str):
        """Init Index.

        :param filepath: file with data for search
        """
        self.index = defaultdict(list)
        self.filepath = filepath
        self.data = pd.read_csv(self.filepath)
        self.data = self.data[~self.data['text'].isna()].copy()
        self.all_doc_ids = set(self.data.index)

    def build(self, compress: bool = False):
        """Build inverted index for given data.

        :param compress: if True then use compression with VarByte encoding
        """
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

        found_posts = pd.merge(
            self.data,
            self.data.loc[list(found_doc_ids)].groupby(['date', 'file'], as_index=False).size(),
            on=['date', 'file']
        ).sort_values(by=['size', 'date', 'ts'], ascending=[False, True, True])

        result = list()
        for p, p_data in found_posts.groupby(['date', 'file'], sort=False):
            main_post_data = p_data.reset_index(drop=True).loc[0, ['text', 'ts']].tolist()
            comments_data = p_data.reset_index(drop=True).drop(index=[0])[['text', 'ts']]\
                .values.tolist()
            result.append((main_post_data, comments_data))
        return result

    def dump(self, filepath):
        """Dump index.

        :param filepath: path .pickle file
        """
        with open(filepath + 'index.pkl', mode='wb') as ind_f:
            pickle.dump(self.index, ind_f)

    def load(self, filepath):
        """Load index from dumps.

        :param filepath: path .pickle file
        """
        with open(filepath + 'index.pkl', mode='rb') as ind_f:
            self.index = pickle.load(ind_f)
