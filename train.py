"""

Training script.

Use this script on raw dataset for preparing data and teaching module (on future).

"""

from pathlib import Path
from joblib import dump
import re

import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize
import gensim
from sklearn.linear_model import LogisticRegression

from model import Pipe, TextTransform
import nltk
nltk.download('punkt')

duplicate_sign = "is_duplicate"
companies_columns = ['name_1', 'name_2']

# Downloading raw training dataset
data = pd.read_csv(Path(r"data/train.csv"), index_col=0)

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
    TextTransform.drop_char(chars=r'-*"/&+:;@=\|?!' + r"'", replace=" "),
    TextTransform.drop_words(words=drop_ownership_list),
    TextTransform.drop_words(words=drop_countries_list),
    TextTransform.drop_whitespaces(),
    TextTransform.transliterate(),
)

pipe_raw = Pipe(
    TextTransform.drop_char(chars=r",;"),
)

# Run pipe
for column in companies_columns:
    data[column + '_clear'] = data[column]
    data[column] = pipe_pre(data[column])

data = data.dropna()

# data.to_hdf(Path(r"data/result.h5"), key="df", mode="w", index = False)
# data = pd.read_hdf("data/result.h5")

# For pipe
data['name_1'] = data[['name_1','name_1_clear']].apply \
 (lambda x: re.sub(r'[^\w\s]', ' ',x['name_1_clear'].lower()).strip()if x.name_1 == '' else x['name_1'],axis=1)
data['name_2'] = data[['name_2','name_2_clear']].apply \
 (lambda x: re.sub(r'[^\w\s]', ' ',x['name_2_clear'].lower()).strip()if x.name_2 == '' else x['name_2'],axis=1)

# Wor2Vec train


def get_tokenize_sentence(sent):
    datas = []
    for i in word_tokenize(sent):
        datas.append(i.lower()) 
    return datas


def sent_vector(sent, vocab_w2v, w2v_model):
    sent = [word for word in sent if word in vocab_w2v]
    return np.mean(word_2_vec_model.wv[sent], axis=0)


name_1_sentences = data['name_1'].apply(lambda x: get_tokenize_sentence(x))
name_2_sentences = data['name_2'].apply(lambda x: get_tokenize_sentence(x))

word_2_vec_model = gensim.models.Word2Vec([*name_1_sentences.to_list(),
                                           *name_2_sentences.to_list()],
                                          min_count=1, vector_size=150,
                                          window=5, epochs=10)

vocab_w2v = list(word_2_vec_model.wv.index_to_key)

X_1 = [sent_vector(sent, vocab_w2v, word_2_vec_model) for sent in name_1_sentences.to_list()]
X_2 = [sent_vector(sent, vocab_w2v, word_2_vec_model) for sent in name_2_sentences.to_list()]
 
embedded_df = pd.DataFrame(np.vstack([np.array(X_1),np.array(X_2)]))
embedded_df['names'] = pd.concat([data[c + '_clear'] for c in companies_columns], ignore_index=True)
embedded_df = embedded_df.drop_duplicates()

# Logistic Regression train
X = np.hstack([np.array(X_1),np.array(X_2)])
y = data[duplicate_sign].values
logit = LogisticRegression(random_state=42, n_jobs=4)
logit.fit(X, y)

# Writing prepared data and models
data.to_hdf(Path(r"data/result.h5"), key="df", mode="w", index=False)
embedded_df.to_hdf(Path(r"data/embeddings.h5"), key="df", mode="w", index=False)
word_2_vec_model.save("data/word2vec.model")
dump(logit, Path(r"data/logit.joblib", sep=";"))
 