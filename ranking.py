from pathlib import Path
from joblib import load

import numpy as np
import pandas as pd
import re
import nltk
from nltk.tokenize import word_tokenize
import gensim
from gensim.models import Word2Vec

from model import Pipe, TextTransform

#Load data and models
logit = load("data/logit.joblib")
word_2_vec_model = Word2Vec.load("data/word2vec.model")
vocab_w2v = list(word_2_vec_model.wv.index_to_key)
embedded_df = pd.read_csv("data/embeddings.csv", index_col=None, delimiter=',')

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
    TextTransform.drop_char(chars=r".,()0123456789«»$^#№"),
    TextTransform.drop_char(chars=r'-*"/&+:;@=\|?!' + r"'", replace=" "),
    TextTransform.drop_words(words=drop_ownership_list),
    TextTransform.drop_words(words=drop_countries_list),
    TextTransform.drop_whitespaces(),
    TextTransform.transliterate(),
)

def get_tokenize_sentence(sent):
    data = []
    for i in word_tokenize(sent):
        data.append(i.lower()) 
    return data

def sent_vector(sent, vocab_w2v, w2v_model):
    sent = [word for word in sent if word in vocab_w2v]
    return np.mean(word_2_vec_model.wv[sent], axis=0)

def get_embedding (comp_name):
    tokenize_name = get_tokenize_sentence(comp_name)
    emb_name = sent_vector(tokenize_name, vocab_w2v, word_2_vec_model)
    return emb_name
    

def rank (comp_name: str, k: int):
    # comp_name_clear = pipe_pre(comp_name, inline = True)
    comp_name_clear = re.sub(r'[^\w\s]', ' ', comp_name).strip()
    comp_name_emb = get_embedding(comp_name_clear)
    comp_name_df = np.array([comp_name_emb for i in range(embedded_df.shape[0])])
    full_df = pd.DataFrame(np.hstack([embedded_df[map(str,range(embedded_df.shape[1] - 1))],
                         comp_name_df]))
    full_df['preds'] = logit.predict_proba(full_df)[:,1]
    full_df['names'] = embedded_df['names']
    ans = full_df.sort_values(by='preds', ascending=False)[['names', 'preds']][0:k].values.tolist()
    return ans


def main():
    while True:
        comp_name = input("Введите название компании:\n\n").rstrip()
        if comp_name == "exit":
            break
        k = 10
        try:
            top_comp = rank(comp_name,k) 
        except ValueError:
            print ("Похожих компаний нет в списке или введены кракозябры\n\n")
            continue
        print (f"Топ {k} похожих компаний:\n\n")
        for i, comp in enumerate(top_comp):
            print (f"{i + 1}: {comp[0]}; вероятность дубля: {round(comp[1],2)}")
        print("\n")

if __name__ == "__main__":
    main()
    