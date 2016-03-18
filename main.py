#!/usr/bin/python
import zipfile
import sys
from extract import unzip
from transformation import transform
import os
import bagit
####extract as cmd argument####
bag = 'bag.zip'
src =  os.getcwd()+'/'+bag #download directory
dest = os.getcwd()+'/'+bag.split(".")[0]

#unzip(src,dest)
zip_ref = zipfile.ZipFile(src, 'r')
zip_ref.extractall(dest)
zip_ref.close()

### check the validity md5.txt

bag = bagit.Bag(dest)

if bag.is_valid():
	print "yay :)"
	typeFile = dest+'/data/info.txt'
	with open(typeFile) as fn:
		flines = fn.readlines()
		count = 0
		for line in flines:
			if count == 0:
				argLs = line.rstrip().split(",")
				gName = argLs[0].split(":")[0]
				gid = argLs[0].split(":")[1]
				colName = argLs[1].split(":")[0]
				colid = argLs[1].split(":")[1]
			elif count == 1:
				files = line.rstrip().split(",")
			count = count+1


	transform(gid,gName,colid,dest,files)


else:
    print "boo :("

