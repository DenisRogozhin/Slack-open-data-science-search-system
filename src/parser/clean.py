"""Realisation of Clean model."""
import pandas as pd


class Clean:
    """Clean model."""

    def __init__(self, data_name: str = 'data/data.csv', save: bool = True):
        """Init Parser model.

        :param data_name: name of raw data
        :param save: bool flag for saving data
        """
        self.data_name = data_name
        self.save = save

    def clean(self) -> pd.DataFrame:
        """
        Clean information from csv file.

        1) Drop empty messages
        2) Drop messages without users
        3) Drop short messages
        4) Drop messages with tech info (with <)
        5) Drop messages with smiles (with :)
        6) Drop messages that repeat more than 100 times

        :return: pd.DataFrame: Cleaning dataframe
        """
        df = pd.read_csv(self.data_name)
        df = df[~df['text'].isna()]
        df = df[~df['user'].isna()]
        df = df[(df['text'].str.len() > 10)]
        df = df[~df['text'].str.contains('<', na=False)]
        df = df[~df['text'].str.contains(':', na=False)]

        counts = df['text'].value_counts()
        df = df[df['text'].isin(counts[counts < 100].index)]
        if self.save:
            df.to_csv(self.data_name, index=False, escapechar='\\')
        return df
