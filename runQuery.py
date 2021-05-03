from read import *
from pagerank import *
import sys

def main(query, dataFile):

    data, rows, columns = readData(dataFile)
    tokenDict, tokPostings, avgDoclen = tokenizer(data, rows, columns)
    outFile1 = open("tokDict.txt", 'w', encoding='utf-8')
    outFile2 = open("tokPostings.txt", 'w', encoding='utf-8')
    pp.pprint(tokenDict, stream=outFile1)
    pp.pprint(tokPostings, stream=outFile2)
    vector_space_model(query,tokenDict, tokPostings,rows, data)
    HITS(data, rows)
    pageRank(data, rows)


if __name__ == '__main__':
    query = "Just across the Potomac river from our nation's capital sits Arlington, Virginia, a beautiful city filled with bustling businesses, thriving tech startups, and an innovative vibe that is drawing founders to this growing region"
    dataFile = "crawled_data.xlsx"
    main(query, dataFile)