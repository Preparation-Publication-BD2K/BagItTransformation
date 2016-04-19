#!/usr/bin/python
import zipfile
from gtf2df_transformation import transform
import os
import bagit
import json
import requests,StringIO
from argparse import ArgumentParser
#import config_utilities as cf

def main_parse_args():
    """Processes command line arguments.
    Expects a number of pipeline specific and global optional arguments.
    If argument is missing, supplies default value.
    Returns: args as populated namespace
    """
    parser = ArgumentParser()
    parser.add_argument('-bl', '--bag_link',help=('download url of the bag'), required=True)
    parser.add_argument('-od', '--output_dir',help=('relative directory of the transformed matrix'), required=True)
    parser.add_argument('-fl', '--feature_list',help=('list of features in the gtf file'))
    parser.add_argument('-gd', '--gene_desc',help=('gene descript name'), required=True)
    parser.add_argument('-sd', '--score_desc',help=('score descript name'), required=True)

    #parser = cf.add_config_args(parser)
    args = parser.parse_args()
    return args



def main():
	####extract as cmd argument####
	args = main_parse_args()

    
	###download bag
	url = args.bag_link #'http://knowcloud.cse.illinois.edu/index.php/s/iw9DG6x15ZtXiId/download'

	req = requests.get(url, stream=True)

	###bag extraction
	bag = 'mydata.zip'
	dest = os.getcwd()+'/'+bag.split(".")[0]
	if not os.path.exists(dest):
		os.makedirs(dest)
	zip_ref = zipfile.ZipFile(StringIO.StringIO(req.content))
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
			for line in flines:
				#print line
				if "meta.json" in line:
					typeFile = dest+"/data/"+line.split(" data/")[1].rstrip().lstrip()
					#print typeFile


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

		#transform("gene_id","FPKM",dest,annotations,structures)
		#output diretory

		out = os.getcwd()+"/"+args.output_dir+"/"
		if not os.path.exists(out):
			os.makedirs(out)
		
		transform(args.gene_desc,args.score_desc,dest,out,annotations,structures)

	else:
	    print "boo :("

if __name__ == "__main__":
    main()