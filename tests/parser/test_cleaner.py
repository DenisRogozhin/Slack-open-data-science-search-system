from src.parser.clean import Clean
import pandas as pd


def test_base_clean():
    clean = Clean("test.csv", save=False)
    test_df = clean.clean()
    assert test_df.shape[0] == 1


def test_compare_clean():
    clean = Clean("data.csv", save=False)
    init_df = pd.read_csv("data.csv")
    test_df = clean.clean()
    assert ((test_df == init_df).all()).all()
