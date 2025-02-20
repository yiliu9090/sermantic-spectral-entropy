import numpy as np
import pandas as pd
import warnings
from itertools import combinations
from sklearn.cluster import SpectralClustering
from collections.abc import Callable
from scipy.stats import entropy

warnings.filterwarnings("ignore")


def text_to_number_phi(t: str, if_none :int = 0) -> int:
    assert(if_none in [0, 1])
    if type(t) == type(" "):
        t = t.upper().replace(" ","")
        if t == "TRUE":
            return 1
        elif t == "FALSE":
            return 0
        else:
            return if_none
    if type(t) == type(True):
        return int(t)


def build_matrix(data: pd.DataFrame, transform_to_number: Callable, result_column_name: str):
    N = np.max(data[["index_1","index_2"]])+1
    M = np.zeros((N,N))
    outcome = []
    for i, j, k in zip(data["index_1"], data["index_2"], data[result_column_name]):
        value = transform_to_number(k)
        M[i][j] = value
        outcome.append(value)

    data["outcome"] = outcome
    M = M + M.T
    return M, data

def find_entropy(M,K):
    spec = SpectralClustering(n_clusters=K, affinity= "precomputed", assign_labels='kmeans')
    return compute_entropy(spec.fit_predict(M))

def compute_entropy(data):
    '''
    compute entropy from data
    '''
    _, count = np.unique(data, return_counts= True )          
    entropy_value = entropy(count/np.sum(count))
    return entropy_value

def semantic_spectral_entropy(text: list[str],K:int , determination :Callable )-> float:
    N = len(text)
    df = pd.DataFrame.from_dict({"indices":list(combinations(range(N),2))})
    df["index_1"] = df["indices"].apply(lambda x: x[0])
    df["index_2"] = df["indices"].apply(lambda x: x[1])
    df["sentence_1"] = df["index_1"].apply(lambda x: text[x])
    df["sentence_2"] = df["index_2"].apply(lambda x: text[x])
    df["LLM_determination"] = df[["sentence_1", "sentence_2"]].apply(lambda x: determination(x["sentence_1"], text_2 = x["sentence_2"]), axis =1)
    M, _ = build_matrix(df, lambda x: x, "LLM_determination")
    return find_entropy(M, K)