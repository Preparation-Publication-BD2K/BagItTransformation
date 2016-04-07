#!/usr/bin/python
import zipfile
import sys
from extract import unzip
from transformation2 import transform2
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
	typeFile = dest+'/data/meta.json'
	with open(typeFile) as data_file:
		data = json.load(data_file)

	baginfo =  data['baginfo'][0]
	path = baginfo['path']
	files =  baginfo['files']

	print files
	transform2("gene_id","transcript_id","FPKM",dest+"/data/",files)


else:
    print "boo :("

