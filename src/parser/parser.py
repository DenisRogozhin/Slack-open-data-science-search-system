"""Realisation of Parser model."""

import json
from datetime import datetime
from os import getcwd, walk
from typing import List

import pandas as pd
from pymystem3 import Mystem


class Parser:
    """Parser model."""

    def __init__(self, data_path: str = "/data/"):
        """Init Parser model.

        :param data_path: path with raw data
        """
        self.path: str = getcwd() + data_path
        self.file_arr: List[str] = []
        self.date_arr: List[str] = []
        self.type_arr: List[str] = []
        self.ts_arr: List[datetime] = []
        self.source_arr: List[str] = []
        self.user_arr: List[str] = []
        self.text_arr: List[str] = []
        self.lemmatize_text_arr: List[str] = []
        self.stem = Mystem()

    def parse(self, stem: bool = False, local_save: bool = True) -> pd.DataFrame:
        """Take information from raw json files.

        :param stem: bool param for use stemming
        :param local_save: bool param for local saving result
        :return: dataframe with parse result
        """
        init_path = True
        for (dirpath, _, filenames) in walk(self.path):
            if init_path:
                init_path = False
                continue
            for cur_file in filenames:
                file_name = dirpath + "/" + cur_file
                json_file = open(file_name)
                dialog_arr = json.loads(json_file.read())
                for cur_dialog in dialog_arr:
                    self.file_arr.append(dirpath.split('/')[-1])
                    self.date_arr.append(file_name.split('/')[-1].split('.')[0])
                    self.type_arr.append(cur_dialog["type"])
                    self.ts_arr.append(datetime.fromtimestamp(float(cur_dialog["ts"])))
                    self.source_arr.append(
                        cur_dialog["source_team"] if "source_team" in cur_dialog else None
                    )
                    self.user_arr.append(
                        cur_dialog["user"] if "user" in cur_dialog else None
                    )
                    self.text_arr.append(cur_dialog["text"])
                    if stem:
                        self.lemmatize_text_arr.append(
                            ''.join(self.stem.lemmatize(cur_dialog["text"]))
                        )
                json_file.close()
        ans_dict = {
            "file": self.file_arr,
            "date": self.date_arr,
            "ts": self.ts_arr,
            "source_team": self.source_arr,
            "user": self.user_arr,
            "text": self.text_arr,
        }
        if stem:
            ans_dict["lemmatize_text"] = self.lemmatize_text_arr
        df = pd.DataFrame({ans_dict})
        if local_save:
            df.to_csv("data.csv", index=False, escapechar="\\")
        return df
