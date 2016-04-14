#!/usr/bin/python
import zipfile
import sys
from extract import unzip
from transformation3 import transform3
import os
import bagit
import json
from pprint import pprint
####extract as cmd argument####
bag = 'bag2.zip'
src =  os.getcwd()+'/'+bag #download directory
dest = os.getcwd()+'/'+bag.split(".")[0]

#unzip(src,dest)
zip_ref = zipfile.ZipFile(src, 'r')
zip_ref.extractall(dest)
zip_ref.close()

### check the validity md5.txt

bag = bagit.Bag(dest)

if bag.is_valid(): #valid
	print "yay :)"
    # read metadata:list of files
	manifest = dest+'/manifest-md5.txt'

	with open(manifest) as fn:
		flines = fn.readlines()
		files = []
		for line in flines:
			print line
			if "meta" in line:
				typeFile = dest+"/data"+line.split("data")[1].rstrip().lstrip()
				print typeFile
			else:
				files.append(line.split("data")[1].rstrip().lstrip())

	with open(typeFile) as data_file:
		data = json.load(data_file)

	#baginfo =  data['baginfo'][0]
	#path = baginfo['path']
	files =  data['files']
	annotations = []
	structures = []
	for a in files: # there can be a list of annotations where each annotation itself is a list of files
		annotations.append(a['annotations'])
		structures.append(a['structure'])
	
	transform3("gene_id","FPKM",dest,annotations,structures)


else:
    print "boo :("

