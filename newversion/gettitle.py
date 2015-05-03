#!/usr/bin/python
# -*- coding:utf8 -*-


import os
import string
from bs4 import BeautifulSoup
import nltk


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

if __name__ == '__main__':
	removeDsStore("webkb")
	fileList = listFiles("webkb")
	# print fileList
	allwordsDict = dict()
	onefileDict = dict()
	filesDict = dict()
	# merge the main word dict with next one file dict
	for fl in fileList:
		print fl
		title = ""
		with open(fl, 'rt') as f:
			content = f.read()
			soup = BeautifulSoup(content, 'html.parser')
			try:
				title = soup.title.string
			except Exception, e:
				continue
			else:
				print title
		'''
		res = st.tag(title.split())
		length = len(res[0])
		newres=""
		for i in range(length):
			print res[0]
			if(res[0][i][1]=="PERSON"):
				newres += " PERSON"
			else:
				newres = newres + " " + str(res[0][i][0])
		
		newres = title
		'''
		if title == None:
			continue
		s2=nltk.word_tokenize(title)
		s3=nltk.pos_tag(s2)
		s4 = nltk.ne_chunk(s3)
		print s4
		length = len(s4.pos())
		newres=""
		for i in range(length):
			tmp = s4.pos()
			print tmp
			if(tmp[i][1]=="PERSON"):
				newres += " PERSON"
			else:
				newres = newres + " " + tmp[i][0][0]


		if newres == None:
			continue
		with open(fl, 'a') as f:
			try:
				for i in range(10):
					f.write("\n")
					f.write(newres)
			except Exception, e:
				continue	
		
			
			





