from typing import Text

import pandas as pd


def get_dataset(dataset_path: Text) -> pd.DataFrame:

    return pd.read_csv(dataset_path)