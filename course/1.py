#!/usr/bin/python
# -*- coding:utf8 -*-

import os
import re
rootpath = ''

#获取path目录下所有的文件名
def getfiles(path):
    fileList = []
    files = os.listdir(path)
    for f in files:
        if(os.path.isfile(path + '/' + f)):
            fileList.append(f)
    return fileList

#从html文件中提取title和body
def process(file):
    global rootpath
    content=''
    with open(rootpath+file, 'r') as f:
        content = f.read().lower()

    head = ''
    body = ''
    tmp = ''
    if(len(content.split('<head>'))==1):
        if len(content.split('<title>'))!=1:
            tmp = content.split('<title>')[1].split('</title>')
            title = tmp[0].strip()
            body = tmp[1].strip()
        else:
            body = content.strip()

    else:

        tmp = content.split('<head>')[1].split('</head>')
        if len(tmp[0].split('<title>'))!=1:
            title = tmp[0].split('<title>')[1].split('</title>')[0].strip()
        
        if len(tmp)==1:
            print file
        body = tmp[1].strip()
    #有些文件会在43行报错，是因为网页文件只有<head>而没有对应的</head>需要手动添加 


    title = removetag(title)
    body = removetag(body)

    with open(rootpath+'final/'+file+'final', 'w') as f:
        #根据网页类别填写下面的tag
        f.write('<head>'+head+'</head>'+'<body>'+body+'</body>'+'<tag>course</tag>')


def processbagofword(file):
    global rootpath
    content=''
    with open(rootpath+file, 'r') as f:
        content = f.read().lower()
    #print len(content.split('<'),1)
    content = '<'+content.split('<',1)[1]
    print content
    content = removetag(content)
    
    with open(rootpath+'final/'+file+'final', 'w') as f:
        #根据网页类别填写下面的tag
        f.write(content+'<tag>course')


#删除title和body内部的html标签
def removetag(content):
    dr = re.compile(r'<[^>]+>',re.S)
    dd = dr.sub('',content)

    return dd.strip()
#检查html文件的标签是否正确
def check(file):
    global rootpath
    content=''
    with open(rootpath+file, 'r') as f:
        content = f.read().lower()

    head = ''
    body = ''
    tmp = ''
    if(len(content.split('<head>'))==1):
        if (content.split('<title>')==1):
            print file
    elif len(content.split('<body>'))==1:
            print file
    

#主函数
if __name__ == '__main__':
    fileList = []
    #这里是网页文件的文件夹，手工在这个目录里建一个名叫final的文件夹，用于存放处理后的文件
    rootpath = '/Users/Tony/Desktop/webkb/course/cornell/test/'
    fileList = getfiles(rootpath)
    for fl in fileList:
        if fl != '.DS_Store':
            #check(fl)
            processbagofword(fl)
        
        
