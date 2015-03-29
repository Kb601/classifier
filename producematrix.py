#!/usr/bin/python
# -*- coding:utf8 -*-


import os
import nltk
from nltk.tokenize import RegexpTokenizer
import csv

words = []

def getwordlist():
	global words
	csvfile = file('top2000csvfile.csv', 'rb')
	reader = csv.reader(csvfile)

	for line in reader:
		break

	words = line
	csvfile.close() 

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

        # the part that is not clear
    tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
    # words = nltk.tokenize(content)
    allwords = tokenizer.tokenize(content)


    #stemming
    
    ps = nltk.stem.snowball.PortugueseStemmer()
    


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

def buildmatrix(wordDict,writer):
 	global words
 	result=[]
 	for terms in words:
 		if terms in wordDict:
 			result.append('1')
 		else:
 			result.append('0')

 	
 	writer.writerow(result)

if __name__ == '__main__':
	fileList = listFiles("newfile")
	getwordlist()
	csvfile = file('csv_test.csv','wb')
	writer = csv.writer(csvfile)
	# merge the main word dict with next one file dict
	count = len(fileList)
	i=1
	for fl in fileList:
		onefileDict = processbagofword2(fl)
		buildmatrix(onefileDict, writer)
		i=i+1
		print str(i) +'ok'+ str(count)
	csvfile.close()





