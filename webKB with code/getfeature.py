#!/usr/bin/python
# -*- coding:utf8 -*-


import os
import nltk
from nltk.tokenize import RegexpTokenizer
import csv
# import sys  

# reload(sys)  
# sys.setdefaultencoding('utf8')
def removeDsStore(path):
    if (os.path.isdir(path) == False):
        if (path.endswith(".DS_Store")):
            print "removing:", path
            os.remove(path)
    else:
        # recursive case: it's a folder
        for filename in os.listdir(path):
            removeDsStore(path + "/" + filename)


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


    avoidWords = set()
    avoidWords = {'and', 'to', 'of','in', 'for', 'on', 'with', 'at','by','from'
    'up','about','into','over', 'after', 'beneath', 'under','above', 'the',
    'a', 'that', 'I','it', 'not', 'he', 'as','you','this','but','his','they', 'her',
    'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'be',
    'have', 'do'
    }

    # for i in xrange(10):
    #     print ''
    # print "allwords in ", files
    # print allwords

    for element in allwords:
        if len(element) >= 3 and element[0] == '(' and element[-1] == ')':
            element = element[1:len(element) - 1]
        if len(element) >= 3 and element[0] == '{' and element[-1] == '}':
            element = element[1:len(element) - 1]
        if element.isdigit() and len(element) == 4:
            element = 'DDDD'
        if element.isdigit() and len(element) == 3:
            element = 'DDD'
        if element.isdigit() and len(element) == 2:
            element = 'DD'

        if (element.isalpha() or element.isdigit()):
            element = ps.stem(element)
            element = str(element)
            if element not in avoidWords:
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


# build matrix with two lable at the first one and second colume
# def buildmatrix(wordDict, writer):
#     global words
#     result=[]
#     for terms in words:
#         if terms in wordDict:
#             result.append('1')
#         else:
#             result.append('0')

#     writer.writerow(result)

def addLable(filesDict):
    schools = ['cornell','misc','texas','washington','wisconsin']
    kinds = ['course','department','faculty','other','project','staff','student']
    universityLable = dict()
    kindLable = dict()

    for i in xrange(len(schools)):
        universityLable[schools[i]] = i
    for i in xrange(len(kinds)):
        kindLable[kinds[i]] = i

    for filename in filesDict:
        for piece in filename.split('/'):
            if piece in kindLable:
                filesDict[filename]['kindLabel'] = kindLable[piece]
            if piece in universityLable:
                filesDict[filename]['universityLabel'] = universityLable[piece]


def dictToList(featureLableList, top2000words, lable1, lable2):
    for element in sorted(top2000words.items(), key=lambda x: -x[1]):
        featureLableList.append(element[0])
    featureLableList.append(lable1)
    featureLableList.append(lable2)




def createDataset(filesDict, featureLableList, filename):
    curFileData = [0]*len(featureLableList)
    with open(filename, 'wb') as f:
        wr = csv.writer(f) 
        wr.writerow(featureLableList)
        for fileName in filesDict:
            for i in xrange(len(featureLableList) - 2):
                if featureLableList[i] in filesDict[fileName]:
                    curFileData[i] += 1
                else:
                    curFileData[i] = 0

            if featureLableList[len(featureLableList) - 2] in filesDict[fileName]:
                curFileData[len(featureLableList) - 2] = filesDict[fileName][featureLableList[len(featureLableList) - 2]]
            else:
                curFileData[len(featureLableList) - 2] = -1
            if featureLableList[len(featureLableList) - 1] in filesDict[fileName]:
                curFileData[len(featureLableList) - 1] = filesDict[fileName][featureLableList[len(featureLableList) - 1]]
            else:
                curFileData[len(featureLableList) - 1] = -1

            wr.writerow(curFileData)



#     csvfile = file('webkbDataset.csv','wb')
#     writer = csv.writer(csvfile)

# writer.writerow(result)
# csvfile.close()
#     fileList = listFiles("newfile")
#     getwordlist()
#     
#     
#     # merge the main word dict with next one file dict
#     count = len(fileList)
#     i=1
#     for fl in fileList:
#         onefileDict = processbagofword2(fl)
#         buildmatrix(onefileDict, writer)
#         i=i+1
#         print str(i) +'ok'+ str(count)
#     



#     for element in sorted(allwordsDict.items(), key=lambda x: -x[1]):

def seperateTrainTestData(testFilesDict, trainFilesDict, filesDict, trainNum):
    index = 0
    for element in filesDict:
        if index > trainNum:
            testFilesDict[element] = filesDict[element]
        trainFilesDict[element] = filesDict[element]
        index += 1








if __name__ == '__main__':
    removeDsStore("newWebkbFile")
    fileList = listFiles("newWebkbFile")
    print fileList
    allwordsDict = dict()
    onefileDict = dict()
    top2000words = dict()
    filesDict = dict()
    # merge the main word dict with next one file dict
    for fl in fileList:
        onefileDict = processbagofword2(fl)
        filesDict[fl] = onefileDict
        # print 'onefileDict', onefileDict
        for element in onefileDict:
            if element in allwordsDict:
                allwordsDict[element] += onefileDict[element]
            else:
                allwordsDict[element] = 1

    # print allwordsDict

    getTop2000words(allwordsDict, top2000words)
    

    for i in xrange(10):
        print ""
    print "Top 2000 words:"
    print top2000words  
    create2000DictCsv(top2000words)
    for i in xrange(10):
        print ""
    print "filesDict:"
    print filesDict
    addLable(filesDict)
    print filesDict

    featureLableList = []
    dictToList(featureLableList, top2000words, 'kindLabel', 'universityLabel')
    for i in xrange(10):
        print ""

    print "featureLableList", featureLableList
    filesNumber = len(filesDict)
    trainNum = 0.9 * filesNumber
    testFilesDict = dict()
    trainFilesDict = dict()
    seperateTrainTestData(testFilesDict, trainFilesDict, filesDict, trainNum)

    createDataset(testFilesDict, featureLableList, 'webkbTestDatasetNonBinarary.csv')

    createDataset(trainFilesDict, featureLableList, 'webkbTrainDatasetNonBinarary.csv')

    # createDataset(filesDict, top2000words)








