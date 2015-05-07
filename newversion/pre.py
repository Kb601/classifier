#!/usr/bin/python
# -*- coding:utf8 -*-


import os
import string
from bs4 import BeautifulSoup
import nltk
import re

def hasdigits(content):
	soup = BeautifulSoup(content, 'html.parser')
	title = ""
	try:
		title = soup.title.string
	except Exception, e:
		return False

	if title == "":
		return False

	for cha in title:
		if cha.isdigit():
			return True

	return False

def hasname(content):
	soup = BeautifulSoup(content, 'html.parser')
	title = ""
	try:
		title = soup.title.string
	except Exception, e:
		return False

	if title == "":
		return False

	s2=nltk.word_tokenize(title)
	s3=nltk.pos_tag(s2)
	s4 = nltk.ne_chunk(s3)
	length = len(s4.pos())
	
	for i in range(length):
		tmp = s4.pos()
		if(tmp[i][1]=="PERSON"):
			return True
	
	return False

def getcontent(content):
    dr = re.compile(r'<[^>]+>',re.S)
    dd = dr.sub(' ',content)
    return dd.strip()


if __name__ == '__main__':
	print hasname("<TITLE>rr Tom</TITLE><body>dwerw</body>daf")
