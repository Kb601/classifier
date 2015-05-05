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
		htext = ""
		with open(fl, 'rt') as f:
			content = f.read()
			soup = BeautifulSoup(content, 'html.parser')
			tmp = soup.find_all("h1")
			for term in tmp:
				htext = htext + term.text + "\n"
			tmp = soup.find_all("h2")
			for term in tmp:
				htext = htext + term.text + "\n"
			tmp = soup.find_all("h3")
			for term in tmp:
				htext = htext + term.text + "\n"
			tmp = soup.find_all("h4")
			for term in tmp:
				htext = htext + term.text + "\n"
			tmp = soup.find_all("h5")
			for term in tmp:
				htext = htext + term.text + "\n"
			tmp = soup.find_all("h6")
			for term in tmp:
				htext = htext + term.text + "\n"
			tmp = soup.find_all("h7")
			for term in tmp:
				htext = htext + term.text + "\n"
			tmp = soup.find_all("h8")
			for term in tmp:
				htext = htext + term.text + "\n"
			tmp = soup.find_all("h9")
			for term in tmp:
				htext = htext + term.text + "\n"
			tmp = soup.find_all("h10")
			for term in tmp:
				htext = htext + term.text + "\n"
			
			print htext
		
		if htext == "":
			continue

		with open(fl, 'a') as f:
			try:
				for i in range(5):
					f.write("\n")
					f.write(htext)
			except Exception, e:
				continue	
		
			
			





