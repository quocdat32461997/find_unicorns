import pprint
import numpy as np
from read import *
from pagerank import *
import sys
import subprocess
import ast
import pickle

def readIndexedInfo(query, dataFile):
    inFile1 = open("tokDict.pkl", 'rb')
    inFile2 = open("tokPostings.pkl", 'rb')
    #inFile3 = open("pagerank.txt", encoding='utf-8')
    #inFile4 = open("HITS_hub.txt", encoding='utf-8')
    #inFile5 = open("HITS_authority.txt", encoding='utf-8')
    #inFile6 = open("matrix_info.txt", encoding='utf-8')
    data, rows, columns = readData(dataFile)
    #tmp1 = inFile1.read()
    #inFile1.close()
    #tokdict = ast.literal_eval(tmp1)
    tokdict = pickle.load(inFile1)
    #tmp2 = inFile2.read()
    #inFile2.close()
    #tokpostings = ast.literal_eval(tmp2)
    tokpostings = pickle.load(inFile2)

    # matrix elements are the results for ranked retrieval with the following columns: [Rank,Doc, Title, Link, Score, QueryVector, DocVector]
    # can be accessed using 2d matrix notation

    matrix = vector_space_model(query, tokdict, tokpostings, rows, data)

    # hubs and authority are dictionaries with the links as keys and the scores as values
    hubs, authority = HITS(data, rows)

    # pr is pagerank dictionary with the links as keys and PR scores as values
    pr = pageRank(data, rows)

    print(matrix)



    return matrix, hubs, authority, pr

readIndexedInfo("american startup", "crawled_techco.xlsx")
# print(tokdict)
# print(tokpostings)
# print(pr)
# print(hub)
# print(authority)
# print(matrix)