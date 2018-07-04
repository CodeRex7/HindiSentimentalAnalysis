# -*- coding: utf-8 -*-

import HSWN
import preprocess
import MF
import tagger
import sys
import xlrd
import translate
import moduleeng

if(len(sys.argv)!=2):
	sys.exit("Usage: python algo.py <input_filename.xlsx>")

#### Read the corpus

posts = []

book = xlrd.open_workbook(sys.argv[1])
sheet = book.sheet_by_index(0)
ctr = 0
for row in sheet.col(1):
	if ctr!=0:
		posts.append(row.value.encode('utf-8'))
	ctr+=1

#### Write posts with polarity
writeDoc = open('OUTPUT.csv','w+')


#### STEP 1 - Apply preprocessing

for i in range(len(posts)):
	posts[i] = preprocess.preProcess(posts[i])

#### STEP 2 - Actual work

sno = 1
for post in posts:

	## Get multipliers
	totalPol = 0.0

	tagdata = tagger.getTag(post)
	## List of multiplying factors
	MFlist = MF.getMF(tagdata)

	for word in post.split(' '):
		## Get tag info
		for mf in MFlist:
			if mf[0] == word:
				mult = mf[1]
				typ = mf[2]

		# If word exists in HSWN
		if HSWN.searchHSWN(word) != 'NF':
			wordPol = HSWN.searchHSWN(word)

			####### HANDLE MULTIPLIER
			wordPol = wordPol*mult

			totalPol += wordPol

		# If word not in HSWN
		else:
			#print 'yes'
			#pass
			if typ in ['NN','VB','JJ','RB']:
				inEn = translate.translate(word)
				pol = moduleeng.polarity(inEn,typ)
				if pol != 'NF':
					totalPol += pol
					print 'yes'

	writeDoc.write(str(sno)+',')
	
	if totalPol>0.1:
		writeDoc.write('1\n')
	elif totalPol<-0.1:
		writeDoc.write('-1\n')
	else:
		writeDoc.write('0\n')

	sno+=1

