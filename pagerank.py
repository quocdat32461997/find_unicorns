from nltk.corpus import stopwords
import pandas as pd
from pandas import DataFrame
import pprint as pp
from collections import OrderedDict
from nltk import sent_tokenize, word_tokenize, PorterStemmer, WordNetLemmatizer
import numpy as np
import math as m
import operator
import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, link):
        self.link = link
        self.children = []
        self.parents = []
        self.auth = 1.0
        self.hub = 1.0
        self.pagerank = 1.0


def HITS(data: DataFrame, rows):

    graph = nx.DiGraph()
    #print(rows)
    for i in range(0,rows):
        graph.add_edges_from([(data["SourceLink"][i],data["Link"][i])])

    #plt.figure(figsize=(50, 50))
    #nx.draw_networkx(graph, with_labels=True)
    #plt.show()
    hubs, authorities = nx.hits(graph, max_iter=10000, tol = 1e-04, normalized=True)

    print("Hub Scores: ", hubs)
    print("Authority Scores: ", authorities)

    return hubs, authorities

def pageRank(data: DataFrame, rows):

    graph = nx.DiGraph()
    #print(rows)
    for i in range(0,rows):
        graph.add_edges_from([(data["SourceLink"][i],data["Link"][i])])

    #plt.figure(figsize=(50, 50))
    #nx.draw_networkx(graph, with_labels=True)
    #plt.show()
    PR = nx.pagerank(graph, max_iter=10000, tol = 1e-06)

    print("PageRank Scores: ", PR)

    return PR


def readData(fileName):

    data = pd.read_excel(fileName)

    #print(data)
    #print(data.shape)
    rows = data.shape[0]
    columns = data.shape[1]
    #print(sent_tokenize(data["Text"][1]))
    #print(word_tokenize(sent_tokenize(data["Text"][1])[2]))
    return data, rows, columns

# data, rows, columns = readData("crawled_data.xlsx")
# HITS(data, rows)
# pageRank(data, rows)