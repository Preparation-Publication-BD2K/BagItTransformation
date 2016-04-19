# BagIt Transformation

This project develops techniques for extracting information from data in BagIt format (https://en.wikipedia.org/wiki/BagIt) to the structured representation required by upstream analysis within the KnowEnG center. This data is then published back into the BagIt format for publication.

This project is funded via the NIH BD2K initiative.

# setup for bagit
```
pip install bagit
```

# creating the sample bag
```
mkdir -p mydata/files
mkdir -p mydata/metadata
wget -O mydata.df 'http://knowcloud.cse.illinois.edu/index.php/s/siUrXHxazgawcPb/download'
python createFiles.py
rm mydata.df
python createMeatadata.py
bagit.py --contact-name 'Sajjadur Rahman' mydata
cd mydata
zip -r mydata.zip ./
mv mydata.zip ..
cd ..
rm -rf mydata
```

# save zip file at url
http://knowcloud.cse.illinois.edu/index.php/s/iw9DG6x15ZtXiId/download

# docker container to run code
https://hub.docker.com/r/cblatti3/bagit_extract/

# running extraction, validation, and tranformation
```
# tiny test
python bagit_extract.py -bl 'http://knowcloud.cse.illinois.edu/index.php/s/iw9DG6x15ZtXiId/download' -od result -gd gene_id -sd FPKM

# realistic test
python bagit_extract.py -bl 'http://knowcloud.cse.illinois.edu/index.php/s/n5Zrcqq6yyuOrPI/download' -od result -gd gene_id -sd FPKM
```



# arguments for bagit_extract.py
link to bag,
location/name for output,
feature list,
gene desc name,
score desc name

# small fixes for KnowEnG
sammples by genes matrix (transpose)
remove quote characters (")
use tab separatation
rename result.csv to "bagit_data.df"
