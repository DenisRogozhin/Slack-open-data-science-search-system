import pandas as pd
import sys
sys.path.append('.')
from src.search_index.index import Index

inv = Index("data/data.csv")
inv.build()
pd.to_pickle(inv, "index/buided_index.pickle")