#!/usr/bin/python
import zipfile
import os
import bagit
import json
import requests,StringIO
from argparse import ArgumentParser
import glob
#import time
#import config_utilities as cf

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            absfn = os.path.join(root, file)
            zfn = absfn[len(path)+len(os.sep):]
            print 'absfn:', absfn
            print 'zfn:', zfn
            ziph.write(absfn, zfn)
            #ziph.write(os.path.join(root, file),os.path.relpath(os.path.join(root, file), os.path.join(path, '.')))

def main_parse_args():
    """Processes command line arguments.
    Expects a number of pipeline specific and global optional arguments.
    If argument is missing, supplies default value.
    Returns: args as populated namespace
    """
    parser = ArgumentParser()
    parser.add_argument('-al', '--analysis_link',help=('download url of the analysis'), required=True)

    #parser = cf.add_config_args(parser)
    args = parser.parse_args()
    return args

def main():
    ####extract as cmd argument####
    args = main_parse_args()

    ###download bag
    url = args.analysis_link #'http://knowcloud.cse.illinois.edu/index.php/s/iw9DG6x15ZtXiId/download'

    req = requests.get(url, stream=True)

    ###bag extraction
    analysis = 'outs.zip'
    dest = os.getcwd()+'/mydata/data/'
    if not os.path.exists(dest):
        os.makedirs(dest)
    zip_ref = zipfile.ZipFile(StringIO.StringIO(req.content))
    zip_ref.extractall(dest)
    zip_ref.close()

    files = glob.glob(os.getcwd()+'/mydata/*.txt')
    for f in files:
        os.remove(f)
    
    bag = bagit.make_bag(os.getcwd()+'/mydata/data', {'Contact-Name': 'Yihan Gao'})
    zipf = zipfile.ZipFile('newdata.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir(os.getcwd()+'/mydata/data', zipf)
    zipf.close()

if __name__ == "__main__":
    main()
