from pathlib import Path
from joblib import load

import numpy as np
import pandas as pd
import re
from nltk.tokenize import word_tokenize
from gensim.models import Word2Vec
from scipy.special import softmax

from model import Pipe, TextTransform

def get_tokenize_sentence(sent):
    data = []
    for i in word_tokenize(sent):
        data.append(i.lower()) 
    return data

def sent_vector(sent, vocab_w2v, w2v_model):
    sent = [word for word in sent if word in vocab_w2v]
    return np.mean(w2v_model.wv[sent], axis=0)

def get_embedding (comp_name, *args):
    tokenize_name = get_tokenize_sentence(comp_name)
    emb_name = sent_vector(tokenize_name, *args)
    return emb_name
    
def rank (comp_name: str, k: int, embedded_df, model, pipe_pre, *args):
    comp_name_clear = pipe_pre(comp_name, inline = True).strip()
    # comp_name_clear = re.sub(r'[^\w\s]', ' ', comp_name).strip()
    comp_name_emb = get_embedding(comp_name_clear, *args)
    comp_name_df = np.array([comp_name_emb for i in range(embedded_df.shape[0])])
    full_df = pd.DataFrame(np.hstack([comp_name_df, embedded_df[range(embedded_df.shape[1] - 1)]]))
    full_df['preds'] = model.predict_proba(full_df)[:,1]
    full_df['names'] = embedded_df['names'].values
    ans = full_df.sort_values(by='preds', ascending=False)[['names', 'preds']][0:k].values.tolist()
    return ans


def main():
    
    #Load data and models
    logit = load("data/logit2.joblib")
    word_2_vec_model = Word2Vec.load("data/word2vec2.model")
    vocab_w2v = list(word_2_vec_model.wv.index_to_key)
    embedded_df = pd.read_hdf("data/embeddings2.h5").dropna()

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
    
    while True:
        comp_name = input("Введите название компании:\n\n").rstrip()
        if comp_name == "exit":
            break
        k = 10
        try:
            top_comp = rank(comp_name,k,embedded_df,logit,pipe_pre,vocab_w2v,word_2_vec_model) 
        except ValueError:
            print ("Похожих компаний нет в списке или введены кракозябры\n\n")
            continue
        print (f"Топ {k} похожих компаний:\n\n")
        for i, comp in enumerate(top_comp):
            print (f"{i + 1}: {comp[0]}; вероятность дубля: {round(comp[1],2)}")
        print("\n")

if __name__ == "__main__":
    main()
    