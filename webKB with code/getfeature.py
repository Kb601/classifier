#!/usr/bin/python
# -*- coding:utf8 -*-


import os
import nltk
from nltk.tokenize import RegexpTokenizer
import csv
# import sys  

# reload(sys)  
# sys.setdefaultencoding('utf8')

def listFiles(path):
    if (os.path.isdir(path) == False):
        # base case:  not a folder, but a file, so return singleton list with its path
        return [path]
    else:
        # recursive case: it's a folder, return list of all paths
        files = [ ]
        for filename in os.listdir(path):
            files += listFiles(path + "/" + filename)
        return files

# def processbagofword(files):
#         # rt = "read text"
#     mode = "rt"
#     content = ""
#     with open(files, mode) as fin:
#         content += fin.read()

#         # the part that is not clear
#     tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
#     # words = nltk.tokenize(content)
#     allwords = tokenizer.tokenize(content)
#     wordDict = dict()

#     for element in allwords:
#         if (element.isalpha() or element.isdigit()):
#             if element in wordDict:
#                 wordDict[element] += 1
#             else:
#                 wordDict[element] = 1

#     return wordDict


    # global rootpath
    # content=''
    # with open(file, 'r') as f:
    #     content = f.read()

    # #tokenize
    # 

    # #stemming
    # ps = nltk.stem.snowball.PortugueseStemmer()
    # wordlist=['']
    # for word in words:
    #     word1 = ps.stem(word)
    #     word1 = str(word1)
    #     wordlist.append(word1)
    # wordlist.pop(0)

    # #termcount
    # termcount = {}
    # for word in wordlist:
    #     termcount[word]=termcount.get(word,0)+1

def processbagofword2(files):
        # rt = "read text"
    mode = "rt"
    content = ""
    with open(files, mode) as fin:
        content += fin.read()

        # the part that is not clear
    tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
    # words = nltk.tokenize(content)
    allwords = tokenizer.tokenize(content)


    #stemming
    
    ps = nltk.stem.snowball.PortugueseStemmer()
    
    '''
    wordlist=['']
    for word in words:
        word1 = ps.stem(word)
        word1 = str(word1)
        wordlist.append(word1)
    wordlist.pop(0)
'''



    wordDict = dict()

    for element in allwords:
        if (element.isalpha() or element.isdigit()):
            element = ps.stem(element)
            element = str(element)
            if element in wordDict:
                wordDict[element] += 1
            else:
                wordDict[element] = 1

    return wordDict



# put top 2000 words into top2000words dict
def getTop2000words(allwordsDict, top2000words):
    count = 0
    for element in sorted(allwordsDict.items(), key=lambda x: -x[1]):
        if count < 2000:
            count += 1
            top2000words[element[0]] = element[1]
        else:
            break    

# put top2000words dict into csv
def create2000DictCsv(top2000words):
    with open('top2000csvfile.csv', 'wb') as f:  
        w = csv.DictWriter(f, top2000words.keys())
        w.writeheader()
        w.writerow(top2000words)    


if __name__ == '__main__':
    fileList = listFiles("newWebkbFile")
    print fileList
    allwordsDict = dict()
    onefileDict = dict()
    top2000words = dict()

    # merge the main word dict with next one file dict
    for fl in fileList:
        onefileDict = processbagofword2(fl)
        print 'onefileDict', onefileDict
        for element in onefileDict:
            if element in allwordsDict:
                allwordsDict[element] += onefileDict[element]
            else:
                allwordsDict[element] = 1

    print allwordsDict

    getTop2000words(allwordsDict, top2000words)
    

    for i in xrange(10):
        print ""
    print "Top 2000 words:"
    print top2000words  
    create2000DictCsv(top2000words)





