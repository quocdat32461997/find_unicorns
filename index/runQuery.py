import pprint
import numpy as np
from read import *
from pagerank import *
import sys
import numpy as np
import subprocess
import ast
import json
import pickle

packages = ['networkx','lxml','xlrd', 'numpy', 'pandas']
for package in packages:
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main(query, dataFile):

    data, rows, columns = readData(dataFile)
    tokenDict, tokPostings, avgDoclen = tokenizer(data, rows, columns)
    outFile1 = open("tokDict.pkl", 'wb')
    outFile2 = open("tokPostings.pkl", 'wb')
    outFile3 = open("pagerank.txt", 'w', encoding='utf-8')
    outFile4 = open("HITS_hub.txt",'w',encoding='utf-8')
    outFile5 = open("HITS_authority.txt",'w',encoding='utf-8')
    #outFile6 = open("matrix_info.txt",'w',encoding='utf-8')
    #pp.pprint(tokenDict, stream=outFile1)
    #pp.pprint(tokPostings, stream=outFile2)
    pickle.dump(tokenDict, outFile1, -1)
    pickle.dump(tokPostings, outFile2, -1)
    #json.dump(tokenDict, outFile1, indent=5, skipkeys=True)
    #json.dump(tokPostings, outFile2, indent=5, skipkeys=True)
    outFile2.close()
    outFile1.close()

    #matrix elements are the results for ranked retrieval with the following columns: [Rank,Doc, Title, Link, Score, QueryVector, DocVector]
    #can be accessed using 2d matrix notation

    matrix = vector_space_model(query,tokenDict, tokPostings,rows, data)

    #hubs and authority are dictionaries with the links as keys and the scores as values
    hubs, authority = HITS(data, rows)
    #pr is pagerank dictionary with the links as keys and PR scores as values
    pr = pageRank(data, rows)

    pp.pprint(hubs, stream=outFile4)
    pp.pprint(authority, stream=outFile5)
    pp.pprint(pr, stream=outFile3)
    np.save("matrix_info", matrix)
    outFile3.close()
    outFile4.close()
    outFile5.close()
    #outFile6.close()


    return matrix, hubs, authority, pr


if __name__ == '__main__':
    query = "new american startups"
    dataFile = "crawled_techco.xlsx"
    main(query, dataFile)
