#!/usr/bin/python
import os

def transform(gid,gName,colid,dest,files):

	dictList = []
	header =  gName
	for f in files:
		header = header+","+f
		typeFile = dest+"/data/"+f+".csv"
		with open(typeFile) as fn:
			flines = fn.readlines()

			count = 0
			fpkmDict = {}
			for lines in flines:

				if count > 0:
					temp = lines.rstrip().split(",")
					fpkmDict[temp[int(gid)-1]] = temp[int(colid)-1]
				count = count+1

			dictList.append(fpkmDict)

	keyList = set()
	for d in dictList:
		for key in d:
			keyList.add(key)

	f = open('result.csv','w')

	##header
	f.write(header+'\n') 

	for key in keyList:
		line = key
		for d in dictList:
			if key in d:
				line = line+","+str(d[key])
		line = line+'\n'
		f.write(line)
	
	f.close()