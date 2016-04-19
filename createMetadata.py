import os
import glob

aggregates = "{\n \"aggregates\": [ \n { \n \"uri\": \"../data/p1.fasta\",\n \"mediatype\" : \"application/json\",\n \"conformsTo\":\"http://edamontology.org/format_1929\"\n }\n ],\n"

filesStr = "\"files\":[\n {\n"



annotations = "\"annotations\" :  [\n"

metadir = os.getcwd() + "/mydata/metadata/"
datadir = os.getcwd()+"/mydata/files/"

ls = glob.glob(datadir+"*.gtf")

count = 0           
for f in ls:
    sample =  f.split(datadir)[1]

    count = count+1
    if count < len(ls):
        annotations = annotations+ "{\n\"uri\": \"../data/files/"+sample+"\",\n \"sample\":\""+sample.split(".gtf")[0]+"\"\n},\n"

    else:
        annotations = annotations+ "{\n\"uri\": \"../data/files/"+sample+"\",\n \"sample\":\""+sample.split(".gtf")[0]+"\"\n}\n],\n"

                                    
structure = ""
with open("json_samples/meta.json","r") as fn:
    lines = fn.readlines()

    flag = 0

    for line in lines:

        if "\"structure\"" in line:
            flag = 1

        if flag == 1:
            structure += line
#print structure 

jsonFile = open(metadir+"meta.json","w")

jsonData = aggregates+filesStr+annotations+structure
jsonFile.write(jsonData)
jsonFile.close()