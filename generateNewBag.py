#!/usr/bin/python
import zipfile
import os
import bagit
import json
import requests,StringIO
from argparse import ArgumentParser
import glob
import shutil
#import time
#import config_utilities as cf

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            absfn = os.path.join(root, file)
            zfn = absfn[len(path)+len(os.sep):]
            ziph.write(absfn, zfn)
            #ziph.write(os.path.join(root, file),os.path.relpath(os.path.join(root, file), os.path.join(path, '.')))

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def main_parse_args():
    """Processes command line arguments.
    Expects a number of pipeline specific and global optional arguments.
    If argument is missing, supplies default value.
    Returns: args as populated namespace
    """
    parser = ArgumentParser()
    parser.add_argument('-ad', '--analysis_dir',help=('directory of the analysis'), required=True)
    parser.add_argument('-md', '--metadata_dir',help=('directory of the metadata'), required=True)

    #parser = cf.add_config_args(parser)
    args = parser.parse_args()
    return args

def main():
    ####extract as cmd argument####
    args = main_parse_args()

    ###download bag
    ad = args.analysis_dir
    md = args.metadata_dir
 
    ###move analysis
    analysis = ad.split('/')[-1]
    dest = os.getcwd()+'/mydata/data/'
    metadest = dest + 'cluster_metadata'
    analysisdest = dest + analysis
    if not os.path.exists(metadest):
        os.mkdir(metadest)
    if not os.path.exists(analysisdest):
        os.mkdir(analysisdest)
    files = glob.glob(md + '/*')
    for f in files:
        shutil.copyfile(f, metadest + '/' + f.split('/')[-1])
    copytree(ad, analysisdest)
    #shutil.copytree(md, dest)
    #if not os.path.exists(dest):
    #    os.makedirs(dest)
    #zip_ref = zipfile.ZipFile(StringIO.StringIO(ad))
    #zip_ref.extractall(dest)
    #zip_ref.close()

    files = glob.glob(os.getcwd()+'/mydata/*.txt')
    for f in files:
        os.remove(f)
    
    bag = bagit.make_bag(os.getcwd()+'/mydata/data', {'Contact-Name': 'Yihan Gao'})
    zipf = zipfile.ZipFile('newdata.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir(os.getcwd()+'/mydata/data', zipf)
    zipf.close()

if __name__ == "__main__":
    main()
