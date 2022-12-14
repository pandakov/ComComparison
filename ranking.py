from pathlib import Path

import nltk
import numpy as np
import pandas as pd
from gensim.models import Word2Vec
from joblib import load
from nltk.tokenize import word_tokenize

from model import Pipe, TextTransform

nltk.download("punkt")


def get_tokenize_sentence(sent):
    """Return the pathname of the KOS root directory."""
    data = []
    for i in word_tokenize(sent):
        data.append(i.lower())
    return data


def sent_vector(sent, vocab_w2v, w2v_model):
    """Return the pathname of the KOS root directory."""
    sent = [word for word in sent if word in vocab_w2v]
    return np.mean(w2v_model.wv[sent], axis=0)


def get_embedding(comp_name, *args):
    """Return the pathname of the KOS root directory."""
    tokenize_name = get_tokenize_sentence(comp_name)
    emb_name = sent_vector(tokenize_name, *args)
    return emb_name


def rank(comp_name: str, k: int, embedded_df, model, pipe_pre, *args):
    """Return the pathname of the KOS root directory."""
    comp_name_clear = pipe_pre(comp_name, inline=True).strip()
    # comp_name_clear = re.sub(r'[^\w\s]', ' ', comp_name).strip()
    comp_name_emb = get_embedding(comp_name_clear, *args)
    comp_name_df = np.array([comp_name_emb for i in range(embedded_df.shape[0])])
    full_df = pd.DataFrame(
        np.hstack([comp_name_df, embedded_df[range(embedded_df.shape[1] - 1)]])
    )
    full_df["preds"] = model.predict_proba(full_df)[:, 1]
    full_df["names"] = embedded_df["names"].values
    ans = full_df.sort_values(by="preds", ascending=False)[["names", "preds"]][
        0:k
    ].values.tolist()
    return ans


def main():
    """Return the pathname of the KOS root directory."""
    # Load data and models
    logit = load("data/logit.joblib")
    word_2_vec_model = Word2Vec.load("data/word2vec.model")
    vocab_w2v = list(word_2_vec_model.wv.index_to_key)
    embedded_df = pd.read_hdf("data/embeddings.h5").dropna()

    # Downloading stoping words
    drop_ownership_list = np.genfromtxt(
        Path(r"stoplists/ownership.txt"), dtype=str, delimiter="\n"
    )
    drop_countries_list = np.genfromtxt(
        Path(r"stoplists/countries.txt"), dtype=str, delimiter="\n"
    )
    drop_countries_list = np.vectorize(str.lower)(drop_countries_list)
    pipe_pre = Pipe(
        TextTransform.to_lower_case(),
        TextTransform.drop_char(chars=r".,()0123456789????$^#???"),
        TextTransform.drop_char(chars=r'-*"/&+:;@=\|?!' + r"'", replace=" "),
        TextTransform.drop_words(words=drop_ownership_list),
        TextTransform.drop_words(words=drop_countries_list),
        TextTransform.drop_whitespaces(),
        TextTransform.transliterate(),
    )

    while True:
        comp_name = input("?????????????? ???????????????? ????????????????:\n\n").rstrip()
        if comp_name == "exit":
            break
        k = 10
        try:
            top_comp = rank(
                comp_name, k, embedded_df, logit, pipe_pre, vocab_w2v, word_2_vec_model
            )
        except ValueError:
            print("?????????????? ???????????????? ?????? ?? ???????????? ?????? ?????????????? ????????????????????\n\n")
            continue
        print(f"?????? {k} ?????????????? ????????????????:\n\n")
        for i, comp in enumerate(top_comp):
            print(f"{i + 1}: {comp[0]}; ?????????????????????? ??????????: {round(comp[1],2)}")
        print("\n")


if __name__ == "__main__":
    main()
