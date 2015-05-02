#!/usr/bin/python
# -*- coding:utf8 -*-


import os
import string
from bs4 import BeautifulSoup
#from nltk.tag.stanford import NERTagger


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
	#st = NERTagger('/Users/Tony/Desktop/NLP/stanford-ner-2015-01-30/classifiers/english.all.3class.distsim.crf.ser.gz','/Users/Tony/Desktop/NLP/stanford-ner-2015-01-30/stanford-ner-3.5.1.jar')
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
		'''
		newres = title
		if newres == None:
			continue
		with open(fl, 'a') as f:
			try:
				for i in range(10):
					f.write("\n")
					f.write(newres)
			except Exception, e:
				continue	
		
			
			





