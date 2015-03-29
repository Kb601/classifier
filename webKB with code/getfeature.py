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

def processbagofword(files):
        # rt = "read text"
    mode = "rt"
    content = ""
    with open(files, mode) as fin:
        content += fin.read()

    start = 0
    end = 0
    tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
    # words = nltk.tokenize(content)
    allwords = tokenizer.tokenize(content)
    wordDict = dict()

    for element in allwords:
        if (element.isalpha() or element.isdigit()):
            if element in wordDict:
                wordDict[element] += 1
            else:
                wordDict[element] = 1

    return wordDict


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



if __name__ == '__main__':
    fileList = listFiles("webkb/newfile")
    processbagofword(fileList[0])
    processbagofword(fileList[1])
    allwordsDict = dict()
    onefileDict = dict()
    top2000words = dict()
    for fl in fileList:
        onefileDict = processbagofword(fl)
        for element in onefileDict:
            if element in allwordsDict:
                allwordsDict[element] += onefileDict[element]
            else:
                allwordsDict[element] = 1
    print allwordsDict
    count = 0
    for element in sorted(allwordsDict.items(), key=lambda x: -x[1]):
        if count < 2000:
            count += 1
            top2000words[element[0]] = element[1]
        else:
            break
    for i in xrange(10):
        print ""
    print "Top 2000 words:"
    print top2000words  
    with open('top2000csvfile.csv', 'wb') as f:  # Just use 'w' mode in 3.x
        w = csv.DictWriter(f, top2000words.keys())
        w.writeheader()
        w.writerow(top2000words)




