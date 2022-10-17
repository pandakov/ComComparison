"""

Training script.

Use this script on raw dataset for preparing data and teaching module (on future).

"""

import numpy as np
import pandas as pd

from model import Pipe, TextTransform

# Downloading raw training dataset
raw_data = pd.read_csv(r"data/train.csv", index_col=0)
# Loc company name pairs
data = raw_data.loc[raw_data["is_duplicate"] == 1.0].drop(columns=["is_duplicate"])

# Downloading stoping words
drop_ownership_list = np.genfromtxt(
    r"stoplists/ownership.txt", dtype=str, delimiter="\n"
)
drop_countries_list = np.genfromtxt(
    r"stoplists/countries.txt", dtype=str, delimiter="\n"
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
data["name_1"] = pipe_pre(data["name_1"])
data["name_2"] = pipe_pre(data["name_2"])
print(data.tail())

# Writing prepared data
data.to_csv(r"data/result.csv")
