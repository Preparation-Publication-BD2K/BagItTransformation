#!/usr/bin/python
import os

def transform(col1,col2,src,dest,annotations,structures):

	dictList = []
	
	for annot in annotations:
		header =  col1
		for f in annot:
			header = header+","+str(f['sample'])  #read sample names
			typeFile = src+str(f['uri']).split("..")[1]  #read file names
			with open(typeFile) as fn:
				
				flines = fn.readlines()
				
				count = 0
				fpkmDict = {}
				for lines in flines:

					temp = lines.rstrip().split("	")
					#print len(temp)
					if len(temp) < 9:
						print typeFile
						print lines
					gid = ""
					tif = ""
					fpkm = ""
					# if "feature" column (col 3) is "transcript", only read that line

					if "transcript" in temp[2]:
						for elem in range(len(temp)): # parse gene id
							temp2 = temp[elem].split(";")
							for elem2 in range(len(temp2)):
								if col1 in temp2[elem2]:
									gid = temp2[elem2].rstrip().lstrip().split(" ")[1]
								#print gid

						for elem in range(len(temp)): # parse fpkm
							temp2 = temp[elem].split(";")
							for elem2 in range(len(temp2)):
								#print temp2[elem2]
								if col2 in temp2[elem2]:
									fpkm = temp2[elem2].rstrip().lstrip().split(" ")[1]
						
						if len(gid)>0: #if gene id non-empty
							fpkmDict[gid] = fpkm
					count = count+1

				dictList.append(fpkmDict)

	keyList = set()
	for d in dictList:
		for key in d:
			keyList.add(key)

	f = open(dest+'result.csv','w')

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
