"""

Training script.

Use this script on raw dataset for preparing data and teaching module (on future).

"""

from pathlib import Path

import numpy as np
import pandas as pd

from model import Pipe, TextTransform

duplicate_sign = "is_duplicate"

# Downloading raw training dataset
raw_data = pd.read_csv(Path(r"data/train.csv"), index_col=0)
# Loc company name pairs
data = raw_data.loc[raw_data[duplicate_sign] == 1.0].drop(columns=[duplicate_sign])

# Downloading stoping words
drop_ownership_list = np.genfromtxt(
    Path(r"stoplists/ownership.txt"), dtype=str, delimiter="\n"
)
drop_countries_list = np.genfromtxt(
    Path(r"stoplists/countries.txt"), dtype=str, delimiter="\n"
)
drop_countries_list = np.vectorize(str.lower)(drop_countries_list)

# Generate PRE pipeline
pipe_pre = Pipe(
    TextTransform.to_lower_case(),
    TextTransform.drop_char(chars=r".,()0123456789«»$^#№"),
    TextTransform.drop_char(chars=r'-*"/&+:@=\|?!', replace=" "),
    TextTransform.drop_words(words=drop_ownership_list),
    TextTransform.drop_words(words=drop_countries_list),
    TextTransform.drop_whitespaces(),
    TextTransform.transliterate(),
)

# for column in data.columns:
# data[column] = pipe_pre(data[column])

data = pipe_pre(data)

print(data)

# Writing prepared data
data.to_csv(Path(r"data/result.csv"))
