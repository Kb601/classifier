#!/usr/bin/python
# -*- coding:utf8 -*-


import os
import time
import nltk
from nltk.tokenize import RegexpTokenizer
import csv
from nltk.stem.lancaster import LancasterStemmer
import random
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
# import sys  

# reload(sys)  
#sys.setdefaultencoding('utf8')
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


def processbagofword2(files):
        # rt = "read text"
    mode = "rt"
    content = ""
    with open(files, mode) as fin:
        content += fin.read()

    #print files
    return content


def addLable(filesDict):
    schools = ['cornell','misc','texas','washington','wisconsin']
    kinds = ['course','department','faculty','other','project','staff','student']
    universityLable = dict()
    kindLable = dict()
    '''
    for i in xrange(len(schools)):
        universityLable[schools[i]] = i
'''
    for i in xrange(len(kinds)):
        kindLable[kinds[i]] = i

    for filename in filesDict:
        for piece in filename.split('/'):
            if piece in kindLable:
                filesDict[filename]['kindLabel'] = kindLable[piece]
            '''if piece in universityLable:
                filesDict[filename]['universityLabel'] = universityLable[piece]'''


def dictToList(featureLableList, top2000words, lable1, lable2, sort = False):
    if sort == True:
        for element in sorted(top2000words.items(), key=lambda x: -x[1]):
            featureLableList.append(element[0])
    else:
        keys = top2000words.keys()
        random.shuffle(keys)
        for key in keys:
            featureLableList.append(key)
    featureLableList.append(lable1)
    featureLableList.append(lable2)



def createDataset(filesDict, featureLableList, filename, boolean = True):
    curFileData = [0]*len(featureLableList)
    with open(filename, 'wb') as f:
        wr = csv.writer(f) 
        wr.writerow(featureLableList)
        for fileName in filesDict:
            for i in xrange(len(featureLableList) - 2):
                if featureLableList[i] in filesDict[fileName]:
                    if not boolean:
                        curFileData[i] += 1
                    else:
                        curFileData[i] = 1
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

#     for element in sorted(allwordsDict.items(), key=lambda x: -x[1]):

def seperateTrainTestData(testFilesDict, trainFilesDict, filesDict, trainNum):
    index = 0
    keys = filesDict.keys()
    random.shuffle(keys)
    for key in keys:
        if index > trainNum:
            testFilesDict[key] = filesDict[key]
        trainFilesDict[key] = filesDict[key]
        index += 1


if __name__ == '__main__':
    removeDsStore("newWebkbFile")
    fileList = listFiles("newWebkbFile")
    # print fileList
    allwordsDict = []
    allwords = []
    onefileDict = [""]
    top2000words = dict()
    filesDict = dict()
    # merge the main word dict with next one file dict
    vectorizer = TfidfVectorizer(max_features=2000,stop_words='english')
    error = 0
    tag=[]
    for fl in fileList:
        onefileDict[0] = processbagofword2(fl)
        #print onefileDict
        #print "haaabbbb"+onefileDict[0]
        #tfidf = vectorizer.fit_transform(onefileDict)
        #if error ==2:
        #    break
        #print fl.split("/")[1]
        print str(len(allwords))+"%"+str(error)
        try:
            tfidf = vectorizer.fit_transform(onefileDict)
        except Exception, e:
            error = error+1
        else:
            allwords.append(onefileDict[0])
            tag.append(fl.split("/")[1])
        finally:
            pass
        #tfidf = vectorizer.fit_transform(allwords)
        
        #filesDict[fl] = onefileDict
        
    #allwords.append("hahaha")
    print len(tag)  
    
    tfidf = vectorizer.fit_transform(allwords)
    res = tfidf.toarray()
    #print vectorizer.get_feature_names()
    print len(tfidf.toarray()[0])
    # print allwordsDict

    #getTop2000words(allwordsDict, top2000words)


    kinds = {'course':'0','department':'1','faculty':'2','other':'3','project':'4','staff':'5','student':'6'}


    len(res[2])
    restext = ""
    for i in range(2000):
        restext=restext+str(i)+","
    restext=restext+"2001\n"
    #for i in xrange(len(tag)):
    f = open("/Users/Tony/Documents/test.csv", 'w')
    f.write(restext)
    oldtime = time.time()
    for i in range(len(tag)):
        if i%5!=0:
            pass
        else:
            restext=""
            for j in xrange(len(res[0])):
                restext = restext+str(res[i][j])+","
            restext = restext+kinds[tag[i]]+"\n"
            f.write(restext)
            print str(i)
    #print restext
    print time.time()-oldtime
    f.close()







