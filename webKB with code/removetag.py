#!/usr/bin/python
# -*- coding:utf8 -*-

import os
import re
rootpath = ''
filepath = ''
savepath = ''

#获取path目录下所有的文件名
def getfiles(path):
    fileNameList = []

    for fileName in os.listdir(path):
        fileNameList.append(fileName)
    return fileNameList

#这个是用来分feild提取，现在不用了
'''
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
'''

def processbagofword(file, filepath, newFilePath):
    # global filepath, rootpath, savepath
    content=''
    with open(filepath + '/' + file, 'r') as f:
        content = f.read().lower()
    if len(content.split('<',1))>1:
        content = '<'+content.split('<',1)[1]
    #print content
    content = removetag(content)
    
    with open(newFilePath + '/' + file, 'w') as f:
        #根据网页类别填写下面的tag
        f.write(content)


#删除html标签
def removetag(content):
    dr = re.compile(r'<[^>]+>',re.S)
    dd = dr.sub('',content)

    return dd.strip()
#检查html文件的标签是否正确
'''
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
'''   

#主函数
if __name__ == '__main__':
    fileList = []
    schools = ['cornell','misc','texas','washington','wisconsin']
    labels = ['course','department','faculty','other','project','staff','student']
    #这里是网页文件的文件夹

    for label in labels:
        oldRootPath = 'webkb' + '/'+ label
        saveRootPath = 'newWebkbFile' + '/'+ label
        for univ in schools:
            filePath = oldRootPath + '/' + univ 
            newFilePath = saveRootPath + '/' + univ
            if not os.path.exists(newFilePath):
                os.makedirs(newFilePath)
            
            fileNameList = getfiles(filePath)
            for fl in fileNameList:
                if fl != '.DS_Store':
                    #check(fl)
                   processbagofword(fl, filePath, newFilePath)
            print univ
        print label

