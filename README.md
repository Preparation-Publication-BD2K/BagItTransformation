# BagIt Transformation

This project develops techniques for extracting information from data in BagIt format (https://en.wikipedia.org/wiki/BagIt) to the structured representation required by upstream analysis within the KnowEnG center. This data is then published back into the BagIt format for publication.

This project is funded via the NIH BD2K initiative.

### setup for bagit
```
pip install bagit
```

### creating the sample bag
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

### save zip file at url
http://knowcloud.cse.illinois.edu/index.php/s/iw9DG6x15ZtXiId/download

### docker container to run code
https://hub.docker.com/r/cblatti3/bagit_extract/

### test datasets
tiny test: http://knowcloud.cse.illinois.edu/index.php/s/iw9DG6x15ZtXiId/download
realistic test: http://knowcloud.cse.illinois.edu/index.php/s/n5Zrcqq6yyuOrPI/download

### running extraction, validation, and tranformation
```
python bagit_extract.py -b mydata.zip -bd mydata -o bagit_data.df -gd gene_id -sd FPKM
```

### arguments for bagit_extract.py
```
    --bag_file              |str    |-b     |the bag file to be extracted
    --output_file           |str    |-o     |the output file to write the transformed matrix
    --feature_list          |array  |-fl    |list of features in the gtf file
    --gene_desc             |str    |-gd    |gene descript name
    --bagit_data_directory  |str    |-bd    |the directory in which to put the extracted bagit data
    --score_desc            |str    |-sd    |score descript name
```

# generate new bag
```
python generateNewBag.py -ad outs -md chron_jobs
```

### arguments for generateNewBag.py
```
    --analysis_dir  |str    |-ad    |directory of the analysis
    --metadata_dir  |str    |-md    |directory of the analysis metadata
```

### assumptions
- url points to zipped bag
- multiple gtf files in data/files with metadata in data/metadata
- outputs in output_dir file "bagit_data.df"
- samples by genes tab seperated matrix with row and column names
- generateNewBag will work on the same working directory, so the downloaded bag from BDDS is already extracted
