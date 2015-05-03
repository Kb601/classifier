#!/usr/bin/python
# -*- coding:utf8 -*-


import os
import nltk
from nltk.tokenize import RegexpTokenizer
import csv
from nltk.stem.lancaster import LancasterStemmer
import random
import re
import string
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

def wordProcess(word):
    start, end = 0, len(word) - 1
    tmpWord1 = word

    for i in xrange(len(word)):
        if word[i] in string.punctuation:
            if (word[i] != '@') and (word[i]!='('):
                tmpWord1 = word[(i+1):]
    tmpword2 = tmpWord1
    for i in xrange(len(tmpWord1) - 1, -1, -1):
        if tmpWord1[i] in string.punctuation:
            if (tmpWord1[i] != '@') and (tmpWord1[i]!=')'):
                tmpword2 = tmpWord1[:i]
    word = tmpword2
    
    if len(word) >= 3 and word[0] == '(' and word[-1] == ')':
        word = word[1:len(word) - 1]
    if len(word) >= 3 and word[0] == '{' and word[-1] == '}':
        word = word[1:len(word) - 1]

    if word.isdigit(): 
        if len(word) == 4:
            word = 'DDDD'

        if len(word) == 4:
            word = 'DDDD'
        elif len(word) == 3:
            word = 'DDD'
        elif len(word) == 2:
            word = 'DD'
        elif len(word) == 1:
            word = 'D'
        elif re.match("^\d{5}(-\d{4})?$", word)!= None:
            word = 'realZipCode'
        else:
            word = 'Dnth'

    elif word.isalpha() and len(word) == 1:
        word = 'A'
    elif re.match("^([0-9]( |-)?)?(\(?[0-9]{3}\)?|[0-9]{3})( |-)?([0-9]{3}( |-)?[0-9]{4}|[a-zA-Z0-9]{7})$", word)!=None:
        word = 'realPhoneNumber'
    # elif re.match("^([0-9]|0[0-9]|1?[0-9]|2[0-3]):[0-5]?[0-9]$", word)!=None:
    #     word = 'dd:dd'
    # elif re.match("^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[1,3-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$", word) != None:
    #     word = 'mm/dd/yyyy'
    # elif re.match("^[\_]*([a-z0-9]+(\.|\_*)?)*@([a-z][a-z0-9\-]+(\.|\-*\.))+[a-z]{2,6}$", word)!=None:
    #     word = 'xxx@xxx.xxx'
    elif re.match("^([a-z0-9_\.-]*)@([\da-z\.-]+)\.([a-z\.]{2,6})$", word)!=None:
        word = 'realEmail'
    elif re.match("^([0-9]|0[0-9]|1?[0-9]|2[0-3]):[0-5]?[0-9]$", word)!=None:
        word = 'realTime'
    else:
        isDate = True
        for element in word.split('/'):
            if not element.isdigit():
                isDate = False
        if isDate == True:
            word = 'realDate'
    return word

def processbagofword2(files):
        # rt = "read text"
    mode = "rt"
    content = ""
    with open(files, mode) as fin:
        content += fin.read()

        # the part that is not clear
    # tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+|')
    # tokenizer = RegexpTokenizer('^[\_]*([a-z0-9]+(\.|\_*)?)+@([a-z][a-z0-9\-]+(\.|\-*\.))+[a-z]{2,6}$|^(19|20)[\d]{2,2}$|^\+?[\d\s]{3,}$|^\+?[\d\s]+\(?[\d\s]{10,}$|^\d{5}$|^\d$|^\d{4}(\-\d{2}){2}$|\^([1-9]|0[1-9]|[12][0-9]|3[01])\D([1-9]|0[1-9]|1[012])\D(19[0-9][0-9]|20[0-9][0-9])$|^([a-z][a-z0-9\-]+(\.|\-*\.))+[a-z]{2,6}$\w+|^([0-1][0-9]|[2][0-3]):([0-5][0-9])$|^[2-9]\d{2}-\d{3}-\d{4}$|\$[\d\.]+|\S+|')
    # email | 1900 - 2099 | Phone number | Phone with code | Zip |
    # Date | Date (dd mm yyyy, d/m/yyyy, etc.)| domain | time |
    # Phone
    # words = nltk.tokenize(content)

    # tokenizer = RegexpTokenizer('[([A-Z]?[a-z]+)?[\_]*([a-z0-9]+(\.|\_*)?)+](@([a-z][a-z0-9\-]+(\.|\-*\.))+[a-z]{2,6})?|\
    #     ([0-9]|0[0-9]|1?[0-9]|2[0-3]):[0-5]?[0-9]|\
    #     |\w+|\$[\d\.]+|\S+|')
    tokenizer = RegexpTokenizer('^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$|([A-Z]?[a-z]+)+|\S+')
    # Email | Phone | date | time | words
    allwords = tokenizer.tokenize(content)

    #stemming
    
    # ps = nltk.stem.snowball.PortugueseStemmer()
    st = LancasterStemmer()
    
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
    'have', 'do', 'is'
    # 'new', 'work', 'lab', 'parallel', '3460', 'each', 'project'
    # 'we','if', '3601', '2936', '5083', '4793', 'so', 'course', 'group', 'how', 'programming',
    # 'language', 'first', 'any', 'performance', 'these', 'using', 'your', 'file',
    # 'students', 'what', 'more', 'computer', 'are', 'page', 'university', 'science',
    #  'from', 'research','systems', 'information', 'edu', 'home', 'we', 'can', 'cs',
    # 'program', 'department', 'system', 'time', 'project', 'data', 'software', 'other',
    # 'which', 'here', 'some', 'has', 'realZipCode', 'use', 'also', 'engineering',
    #  'class', 'design', 'may', 'web', 'computing', 'was', 'office', 'last', 'no', 
    #  'our', 'should', 'student', 'Dnth', 'based', 'list', 'out', 'me', 'problem', 
    #  'distributed', 'two', 'available', 'code', 'when', 'email', 'number', 'algorithms', 'am', 'up'



    }

    for i in xrange(10):
        print ''
    print "allwords in ", files
    print allwords
    flag = True
    for element in allwords:

        element = wordProcess(element)

        # if (element.isalpha() or element.isdigit()):
        if element.isdigit():
            if  (element != 'realPhoneNumber') and (element != 'realDate') and \
                (element != 'realTime') and (element != 'realEmail') and \
                (element != 'realZipCode'):
                element = st.stem(element)
                element = str(element)
        if element != '' and (element not in avoidWords):
            if element not in avoidWords:
                if element in wordDict:
                    wordDict[element] += 1
                else:
                    wordDict[element] = 1
            if flag:
                last = element
                flag = False
            else:
                newBiGrim = last.lower() + " " + element.lower()
                print "newBiGrim", newBiGrim
                last = element
                if newBiGrim in wordDict:
                    wordDict[newBiGrim] += 1
                else:
                    wordDict[newBiGrim] = 1
    print "a wordDict", wordDict
    return wordDict



# put top 2000 words into top2000words dict
def getTop2000words(allwordsDict, top2000words):
    count = 0
    for element in sorted(allwordsDict.items(), key=lambda x: -x[1]):
        if count < 5000:
            count += 1
            top2000words[element[0]] = element[1]
        else:
            break    

# put top2000words dict into csv
def create2000DictCsv(top2000words):
    with open('top5000csvfile.csv', 'wb') as f:  
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
    keys = filesDict.keys()
    random.shuffle(keys)
    for key in keys:
        if index > trainNum:
            testFilesDict[key] = filesDict[key]
        trainFilesDict[key] = filesDict[key]
        index += 1


if __name__ == '__main__':
    removeDsStore("newfile")
    fileList = listFiles("newfile")
    # print fileList
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
    # print top2000words  
    create2000DictCsv(top2000words)
    # tmpTop200Word = top2000words
    # sorted(tmpTop200Word.items(), key=lambda x: x[1])
    printfeatureLableList = []
    for element in sorted(top2000words.items(), key=lambda x: -x[1]):
        printfeatureLableList.append(element[0])
        printfeatureLableList.append(element[1])

    print 'printfeatureLableList', printfeatureLableList



    for i in xrange(10):
        print ""
    print "filesDict:"
    # print filesDict
    addLable(filesDict)
    # print filesDict

    featureLableList = []
    sort = True
    if sort == True:
        dictToList(featureLableList, top2000words, 'kindLabel', 'universityLabel', sort)
        for i in xrange(10):
            print ""

        print "featureLableList at sorted list", featureLableList
        filesNumber = len(filesDict)
        trainNum = 0.9 * filesNumber
        testFilesDict = dict()
        trainFilesDict = dict()
        seperateTrainTestData(testFilesDict, trainFilesDict, filesDict, trainNum)

        createDataset(testFilesDict, featureLableList, '1-1webkbTestDSNonBinararySortFeature.csv', False)

        createDataset(trainFilesDict, featureLableList, '1-1webkbTrainDSNonBinararySortFeature.csv', False)
        createDataset(testFilesDict, featureLableList, '1-2webkbTestDSBinararySortFeature.csv', True)

        createDataset(trainFilesDict, featureLableList, '1-2webkbTrainDSBinararySortFeature.csv', True)

    sort = False
    featureLableList = []
    if sort == False:
        dictToList(featureLableList, top2000words, 'kindLabel', 'universityLabel', sort)
        for i in xrange(10):
            print ""

        print "featureLableList at none sorted list", featureLableList
        filesNumber = len(filesDict)
        trainNum = 0.9 * filesNumber
        testFilesDict = dict()
        trainFilesDict = dict()
        seperateTrainTestData(testFilesDict, trainFilesDict, filesDict, trainNum)

        createDataset(testFilesDict, featureLableList, '2-1webkbTestDSNonBinararyNonSortFeature.csv', False)

        createDataset(trainFilesDict, featureLableList, '2-1webkbTrainDSNonBinararyNonSortFeature.csv', False)
        createDataset(testFilesDict, featureLableList, '2-2webkbTestDSBinararyNonSortFeature.csv', True)

        createDataset(trainFilesDict, featureLableList, '2-2webkbTrainDSBinararyNonSortFeature.csv', True)
    # createDataset(filesDict, top2000words)








