"""Realisation of Clean model."""
import pandas as pd
from pydantic import BaseModel


class Clean(BaseModel):
    """Clean model."""

    def __init__(self, data_name: str = 'data.csv', save: bool = True):
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
        text_column = df['text']
        user_column = df['user']
        df = df[~text_column.isna()]
        df = df[~user_column.isna()]
        df = df[text_column.str.len() > 10]
        df = df[~text_column.str.contains('<')]
        df = df[~text_column.str.contains(':')]

        counts = text_column.value_counts()
        df = df[text_column.isin(counts[counts < 100].index)]
        if self.save:
            df.to_csv(self.data_name, index=False, escapechar='\\')
        return df
