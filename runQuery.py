from read import *
from pagerank import *
import sys
import numpy as np

def main(query, dataFile):

    data, rows, columns = readData(dataFile)
    tokenDict, tokPostings, avgDoclen = tokenizer(data, rows, columns)
    outFile1 = open("tokDict.txt", 'w', encoding='utf-8')
    outFile2 = open("tokPostings.txt", 'w', encoding='utf-8')
    pp.pprint(tokenDict, stream=outFile1)
    pp.pprint(tokPostings, stream=outFile2)

    #matrix elements are the results for ranked retrieval with the following columns: [Rank,Doc, Title, Link, Score, QueryVector, DocVector]
    #can be accessed using 2d matrix notation
    matrix = vector_space_model(query,tokenDict, tokPostings,rows, data)
    #hubs and authority are dictionaries with the links as keys and the scores as values
    hubs, authority = HITS(data, rows)
    print(hubs['https://tech.co/news/edn-grow-the-greenest-green-2014-12'])
    #pr is pagerank dictionary with the links as keys and PR scores as values
    #pr = pageRank(data, rows)

    return matrix, hubs, authority, pr


if __name__ == '__main__':
    #query = 'robinhood'
    query = 'Potamic river'
    #query = "Just across the Potomac river from our nation's capital sits Arlington, Virginia, a beautiful city filled with bustling businesses, thriving tech startups, and an innovative vibe that is drawing founders to this growing region"
    dataFile = "crawled_data.xlsx"
    main(query, dataFile)
