from nltk.corpus import stopwords
import pandas as pd
from pandas import DataFrame
import pprint as pp
from collections import OrderedDict
from nltk import sent_tokenize, word_tokenize, PorterStemmer, WordNetLemmatizer
import numpy as np
import math as m
import operator



def readData(fileName):

    data = pd.read_excel(fileName)

    #print(data)
    #print(data.shape)
    rows = data.shape[0]
    columns = data.shape[1]
    #print(sent_tokenize(data["Text"][1]))
    #print(word_tokenize(sent_tokenize(data["Text"][1])[2]))
    return data, rows, columns

def checkKeys(keySet1, keySet2):

    for key in keySet1:
        if key not in keySet2:
            return False

    return True

def combineDicts(dict1, dict2):

    combinedDict = dict()

    if checkKeys(dict1, dict2):
        for k in dict1.keys():
            combinedDict[k] = (dict1[k], len(dict2[k]), dict2[k]) #()
    else:
        return -1
    return combinedDict

def tokenizer(data: DataFrame, rows, columns):
    tokenDict = dict() #"<entry>": (tf(overall), df, [list of docs it appears in])
    tokenDocs = dict()
    tokPostings = dict() #"<entry>": {docid: [tf in that doc, max_tf, doclen], ...}
    docInfo = dict()
    lematizer = WordNetLemmatizer()
    stopWords = set(stopwords.words("english"))

    for i in range(0, rows):
        tf = 1
        max_tf = 1
        doclen = 0
        docNo = i
        tokens1 = word_tokenize(data["Title"][i])
        tokens = list()
        sentenceList = sent_tokenize(data["Text"][i])
        for sentence in sentenceList:
            tmp = word_tokenize(sentence)
            for t in tmp:
                tokens.append(t)

        #tokens = word_tokenize(sent_tokenize(data["Text"]))

        for t in tokens1:
            tokens.append(t)

        for tok in tokens:
            doclen += 1
            if tok in stopWords:
                continue
            word = lematizer.lemmatize(tok)
            if word in tokenDict:
                tokenDict[word] = tokenDict.get(word) + 1
                tokenDocs[word].add(docNo)
                # tokPostings[word].
            else:
                tokenDict[word] = 1
                tokenDocs[word] = {docNo}
                # tokPostings[word] = {docNo:1}
            if word in tokPostings:
                if docNo in tokPostings[word].keys():
                    tokPostings[word][docNo][0] = tokPostings[word][docNo][0] + 1
                    tf = tokPostings[word][docNo][0]
                    if tf > max_tf:
                        max_tf = tf
                else:
                    tokPostings[word][docNo] = [1, 0, 0]
            else:
                tokPostings[word] = {docNo: [1, 0, 0]}  # {docid: (tf,max_tf, doclen)}

        docInfo[docNo] = [max_tf, doclen]
        for word in tokPostings.keys():
            for doc in tokPostings[word]:
                tokPostings[word][int(doc)][1] = docInfo[int(doc)][0]
                tokPostings[word][int(doc)][2] = docInfo[int(doc)][1]
    sumOfDoclens = 0
    for doc in docInfo:
        sumOfDoclens += docInfo[doc][1]
    avgDoclen = sumOfDoclens / rows
    fullTokenDict = combineDicts(tokenDict, tokenDocs)  # combine dictionaries with same key set


    if fullTokenDict == -1:
        print("Failed in combining dictionaries")
        return
    # else:
    #     print(fullTokenDict)
    # print(tokenDict)
    # stemmedTokenDict, stemmedTokenDocs = stemmer(tokenDict)
    return fullTokenDict, tokPostings, avgDoclen

def getDocVector(queryVector, docNo, tokDict: dict, tokPostings: dict):
    docVector = dict() # {}
    for word in queryVector:
        if word in tokDict.keys():
            if docNo in tokDict[word][2]:
                tmp = list() #(df, tf, max_tf, doclen)
                tmp.append(tokDict[word][1])
                tmp.append(tokPostings[word][docNo][0])
                tmp.append(tokPostings[word][docNo][1])
                tmp.append(tokPostings[word][docNo][2])
                docVector[word] = tmp.copy()



    return docVector

def calcScore(docVector: dict, queryVector: list, collectionSize):
    W1 = np.zeros(len(queryVector))

    Q1 = np.zeros(len(queryVector))
    lemmatizer = WordNetLemmatizer()

    similarKeys = list()
    query_info = dict() #({word: [tf] })

    for q in queryVector:
        if q in query_info:
            query_info[q] = query_info.get(q) + 1
        else:
            query_info[q] = 1
    q_maxtf = max(query_info.values())
    for q in queryVector:
        if q in docVector:
            similarKeys.append(q)
    for word in similarKeys:
        lemma = lemmatizer.lemmatize(word)
        tf = float(docVector[lemma][1])
        q_tf = float(query_info[lemma])
        df_t = float(docVector[lemma][0])
        q_df_t = float(query_info[lemma])
        maxtf = float(docVector[lemma][2])
        index = queryVector.index(lemma)
        doclen = float(docVector[lemma][3])

        tf_t_d = 1 + m.log10(tf)
        q_tf_t_d = 1 + m.log10(q_tf)

        idf_t = m.log10(collectionSize/(df_t+1))
        q_idf_t = m.log10(collectionSize/(q_df_t+1))

        tf_idf = tf_t_d * idf_t
        q_tf_idf = q_tf_t_d * q_idf_t
        # ###
        # [0.4 + 0.6 * log(tf + 0.5) / log(maxtf + 1.0)]
        # *[log(collectionsize / df) / log(collectionsize)]
        # ###
        #w_val1 = (0.4 + 0.6*m.log10(tf + 0.5)/m.log10(maxtf + 1.0)) * (m.log10(collectionSize/df))/m.log10(collectionSize)
        w_val1 = tf_idf
        q_val1 = q_tf_idf
        #q_val1 = (0.4 + 0.6*m.log10(q_tf + 0.5)/m.log10(q_maxtf + 1.0)) * (m.log10(collectionSize/df)/m.log10(collectionSize))
        W1[index] = w_val1
        Q1[index] = q_val1

    norm_W1 = W1 / np.linalg.norm(W1)
    norm_Q1 = Q1 / np.linalg.norm(Q1)
    score1 = np.dot(norm_Q1, norm_W1)


    return score1, norm_W1, norm_Q1

def printInfo(fileName, all_vectors1: list, info_vectors1: dict):
    file = open(fileName, 'w', encoding="utf-8")
    matrix = list()
    counter = 0
    for item in reversed(all_vectors1):
        tmp = list()

        counter += 1
        tmp.append(counter)
        tmp.append(item[0])
        tmp.append(info_vectors1[item[0]][2])
        tmp.append(info_vectors1[item[0]][3])
        tmp.append(item[1])
        tmp.append(info_vectors1[item[0]][0])
        tmp.append(info_vectors1[item[0]][1])

        matrix.append(tmp)

        file.write("Rank:{}\nDoc:{}\nTitle:{}\nLink:{}\nScore:{}\nQueryVec:{}\nDocVec{}\n".format(counter,
                                                                                                  item[0],
                                                                                                  info_vectors1[item[0]][2],
                                                                                                  info_vectors1[item[0]][3],
                                                                                                  item[1],
                                                                                                  info_vectors1[item[0]][0],
                                                                                                  info_vectors1[item[0]][1]))
        file.write("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")

    matrix = np.asmatrix(matrix)
    return matrix


def vector_space_model(query, tokDict, tokPostings, collectionSize, data: DataFrame):
    stopWords = set(stopwords.words("english"))
    lematizer = WordNetLemmatizer()
    sorted_all_vectors1 = dict()
    queryVector = list()
    all_vectors1 = OrderedDict()
    info_vectors1 = dict()


    q = word_tokenize(query)
    for word in stopWords:
        if word in q:
            q.remove(word)
    for w in q:
        queryVector.append(lematizer.lemmatize(w))
    #print(queryVector)
    for doc in range(0, collectionSize): #docNoRange = no rows
        docVector = getDocVector(queryVector, doc, tokDict, tokPostings)
        if len(docVector) == 0:
            continue
        score1, w1, q1 = calcScore(docVector, queryVector, collectionSize)
        all_vectors1[doc] = score1
        info_vectors1[doc] = (q1, w1, data["Title"][doc], data["Link"][doc])
    sorted1 = sorted(all_vectors1.items(), key=operator.itemgetter(1))

    fname1 = "query_results.txt"
    matrix = printInfo(fname1, sorted1, info_vectors1)
    return matrix

# data, rows, columns = readData("crawled_data.xlsx")

# tokenDict, tokPostings, avgDoclen = tokenizer(data, rows, columns)
# outFile1 = open("tokDict.txt", 'w', encoding='utf-8')
# outFile2 = open("tokPostings.txt", 'w', encoding='utf-8')
# pp.pprint(tokenDict, stream=outFile1)
# pp.pprint(tokPostings, stream=outFile2)
# vector_space_model("Just across the Potomac river from our nation's capital sits Arlington, Virginia, a beautiful city filled with bustling businesses, thriving tech startups, and an innovative vibe that is drawing founders to this growing region",tokenDict, tokPostings,rows, data)

