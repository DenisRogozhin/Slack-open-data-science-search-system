import pandas as pd


class Clean:
    def __init__(self, data_name: str = "data.csv", save: bool = True):
        self.data_name = data_name
        self.save = save

    def clean(self) -> pd.DataFrame:
        df = pd.read_csv(self.data_name)
        df = df[~df["text"].isna()]
        df = df[~df["user"].isna()]
        if self.save:
            df.to_csv(self.data_name, index=False, escapechar="\\")
        return df
