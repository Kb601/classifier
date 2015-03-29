#!/usr/bin/python
# -*- coding:utf8 -*-

import os
import nltk
from nltk import SnowballStemmer
rootpath = ''

#获取path目录下所有的文件名
def getfiles(path):
    fileList = []
    files = os.listdir(path)
    for f in files:
        if(os.path.isfile(path + '/' + f)):
            fileList.append(f)
    return fileList


def processbagofword(file):
    global rootpath
    content=''
    with open(rootpath+file, 'r') as f:
        content = f.read()

    #tokenize
    words = nltk.word_tokenize(content)

    #stemming
    ps = nltk.stem.snowball.PortugueseStemmer()
    wordlist=['']
    for word in words:
        word1 = ps.stem(word)
        word1 = str(word1)
        wordlist.append(word1)
    wordlist.pop(0)

    #termcount
    termcount = {}
    for word in wordlist:
        termcount[word]=termcount.get(word,0)+1


#主函数
if __name__ == '__main__':
    fileList = []
    #这里是网页文件的文件夹，手工在这个目录里建一个名叫final的文件夹，用于存放处理后的文件
    rootpath = '/Users/Tony/Desktop/webkb/course/cornell/test/'
    fileList = getfiles(rootpath)
    for fl in fileList:
        process(fl)
        
        
