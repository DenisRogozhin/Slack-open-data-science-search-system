from collections import defaultdict


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

        # self.compress()


    def compress(self):
        pass


    def decompress(self):
        pass


    def search(self, query):
        pass


    def dump(self, index_filepath, compression_filepath):
        pass


    def load(self, index_filepath, compression_filepath):
        pass
