#!/usr/bin/python
import zipfile
import sys
from extract import unzip
from transformation import transform
import os
import bagit
# load the bag
bag = bagit.Bag('/media/sunny/OS/Users/Sajjadur/workspace/ProtoType/bag1')

if bag.is_valid():
    print "yay :)"
else:
    print "boo :("