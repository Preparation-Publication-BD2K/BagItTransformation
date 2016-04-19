#!/usr/bin/python
import os

def transform(col1,col2,src,dest,annotations,structures):

	dictList = {}
	
	for annot in annotations:
		#header =  col1
		for f in annot:
			#header = header+","+str(f['sample'])  #read sample names
			typeFile = src+str(f['uri']).split("..")[1]  #read file names
			with open(typeFile) as fn:
				
				flines = fn.readlines()
				
				
				fpkmDict = {}
				for lines in flines:

					temp = lines.rstrip().split("	")
					#print len(temp)
					if len(temp) < 9:
						print typeFile
						print lines
						continue
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
					

				dictList[str(f['sample'])] = fpkmDict

	keyList = set()
	header = " \t"
	for d in dictList:
		for key in dictList[d]:
			keyList.add(key)

	f = open(dest+'bagit_data.df','w')

	##header
	

	for key in keyList:
		header =  header + "\t" + key

	header = header+'\n'
	f.write(header.replace("\"",'')) 

	### each row
	for d in dictList:
		line = d
		for key in keyList:
			if key in dictList[d]:
				line = line+"\t"+str(dictList[d][key])
			else:
				line = line+"\t "
		line = line+'\n'
		f.write(line.replace("\"",''))
	
		   	
	f.close()
