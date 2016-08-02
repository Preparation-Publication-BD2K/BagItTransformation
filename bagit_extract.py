#!/usr/bin/env python3


"""
This module extracts data from a bag.

**Arguments**

.. csv-table::
    :header: flag,name,type,status,reqs.,description
    :widths: 5,20,5,20,10,40
    :delim: |

    -b|--bag_file|str|required||the bag file to be extracted
    -bd|--bagit_data_directory|str|optional, default: 'mydata'| \
        the directory in which to put the extracted bagit data and files
    -o|--output_file|str|required||the output file to write the transformed matrix
    -fl|--feature_list||optional, default: None||the list of features in the gtf file
    -gd|--gene_desc|str|required||the gene descriptor name
    -sd|--score_desc|str|required||the score descriptor name
"""


import argparse
import json
import os
import math
import zipfile

import bagit


# Initialization/Constants
DEFAULT_BAGIT_DATA_DIRECTORY = "mydata"
DEFAULT_MANIFEST_FILE = "manifest-md5.txt"
DEFAULT_META_FILE = "meta.json"


def parse_args():
    """
    Processes the command line arguments.

    Returns:
        argparse.Namespace: args as populated namespace
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bag_file', required=True,
                        help='the bag file to be extracted')
    parser.add_argument('-bd', '--bagit_data_directory',
                        default=DEFAULT_BAGIT_DATA_DIRECTORY,
                        help='the directory in which to put the '
                             'extracted bagit data and files')
    parser.add_argument('-o', '--output_file', required=True,
                        help='the output file to write the transformed matrix')
    parser.add_argument('-fl', '--feature_list',
                        help='the list of features in the gtf file')
    parser.add_argument('-gd', '--gene_desc', required=True,
                        help='the gene descriptor name')
    parser.add_argument('-sd', '--score_desc', required=True,
                        help='the score descriptor name')
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()

    return args


def extract_bag(bag_file, bagit_data_directory):
    """
    Downloads and extracts the bag.

    Parameters:
        bag_link (str): the bag's url
        bagit_data_directory (str): the directory to store the bag's contents
    """
    zip_ref = zipfile.ZipFile(bag_file)

    if not os.path.exists(bagit_data_directory):
        os.makedirs(bagit_data_directory)

    zip_ref.extractall(bagit_data_directory)
    zip_ref.close()


def get_meta_file(bagit_data_directory):
    """
    Gets the meta file from the bagit data directory.

    Parameters:
        bagit_data_directory (str): the directory containing the bag's contents

    Returns:
        str: the meta file (possibly None)
    """
    manifest = os.path.join(bagit_data_directory, DEFAULT_MANIFEST_FILE)

    meta_file = None

    with open(manifest) as f:
        for line in f:
            if line.rstrip().endswith(DEFAULT_META_FILE):
                meta_file = os.path.join(bagit_data_directory, line.split()[1])
                break

    return meta_file


def parse_meta_file(meta_file):
    """
    Parses the meta file and builds the annotations and structure data.

    Parameters:
        meta_file (str): the meta file (the full path)

    Returns:
        a 2-tuple containing

        - **annotations** (*list*): the annotations found
        - **structure** (*list*): the structure found
    """
    with open(meta_file) as data_file:
        data = json.load(data_file)

    files = data['files']

    annotations = []
    structure = []

    # There can be a list of annotations, where each annotation
    # itself is a list of files
    for item in files:
        annotations.append(item['annotations'])
        structure.append(item['structure'])

    return annotations, structure


def parse_structure(structure, gene_desc, score_desc):
    """
    Parses the structure to find the columns containing the gene and
    score descriptors.

    Parameters:
        structure (list): a list of lists of dicts

    Returns:
        a 2-tuple containing

        - **gene_desc_col** (*list*): the columns contains the gene descriptor
        - **score_desc_col** (*list*): the columns contains the score descriptor
    """
    gene_desc_col = []
    score_desc_col = []

    # structure is a list of lists of dicts
    # item is a list of dicts
    for item in structure:
        # dct is a dict
        for dct in item:
            if "values" in dct:
                for value in dct['values']:
                    if value['value'] == gene_desc:
                        gene_desc_col.append(dct['column'])
                    if value['value'] == score_desc:
                        score_desc_col.append(dct['column'])

    return gene_desc_col, score_desc_col


def gather_data(gene_desc, gene_desc_col, score_desc, score_desc_col,
                bagit_data_directory, annotations):
    """
    Gathers data from the files in the bag.

    Gathers data from the files in the bag, collecting the scores for
    the columns matching the gene descriptor and the score descriptor.

    Parameters:
        gene_desc (str): the gene descriptor
        gene_desc_col (list): the gene descriptor
        score_desc (str): the gene descriptor
        score_desc_col (list): the gene descriptor
        bagit_data_directory (str): the bagit data directory
        annotations (list): the annotations from the meta file

    Returns:
        a 4-tuple containing

        - **dict_list** (*dict*): the score per gene per file
        - **count_per_gene** (*dict*): the count per gene
        - **score_sum_per_gene** (*dict*): the score sum per gene
        - **score_sq_sum_per_gene** (*dict*): the score sq sum per gene
    """
    dict_list = {}
    count_per_gene = {}
    score_sum_per_gene = {}
    score_sq_sum_per_gene = {}

    for item, gd_col, sd_col in zip(annotations, gene_desc_col, score_desc_col):
        for dct in item:
            filename = bagit_data_directory + str(dct['uri']).split("..")[1]

            with open(filename) as f:
                fpkm_dict = {}
                for line in f:
                    items = line.rstrip().split("\t")
                    if len(items) < 9:
                        continue

                    gid = None
                    fpkm = None

                    # Only look at lines where "feature" column
                    # (column 2) is "transcript"
                    if items[2] == "transcript":
                        attrs = items[gd_col].split("; ")
                        for attr in attrs:
                            if attr.startswith(gene_desc):
                                gid = attr.split()[1]

                        attrs = items[sd_col].split("; ")
                        for attr in attrs:
                            if attr.startswith(score_desc):
                                fpkm = attr.split()[1].replace("\"", "")

                        if gid is not None and fpkm is not None:
                            fpkm_dict[gid] = float(fpkm)
                            if gid not in count_per_gene:
                                count_per_gene[gid] = 0
                                score_sum_per_gene[gid] = 0.0
                                score_sq_sum_per_gene[gid] = 0.0
                            count_per_gene[gid] += 1
                            score_sum_per_gene[gid] += float(fpkm)
                            score_sq_sum_per_gene[gid] += float(fpkm) * float(fpkm)

                dict_list[str(dct['sample'])] = fpkm_dict

    return dict_list, count_per_gene, score_sum_per_gene, score_sq_sum_per_gene


def output_data(output_file, dict_list, count_per_gene, score_sum_per_gene, score_sq_sum_per_gene):
    """
    Outputs the data.

    Outputs the data, in a spreadsheet/dataframe format, with the
    samples/files as the rows and the genes as the columns.  The gene
    names are the column headers and the sample/file names are the row
    labels.  Each value is normalized.

    Parameters:
        output_file (str): the output file
        dict_list (dict): the score per gene per file
        count_per_gene (dict): the count per gene
        score_sum_per_gene (dict): the score sum per gene
        score_sq_sum_per_gene (dict): the score sq sum per gene
    """
    # Build the set of all keys that occur in dict_list
    key_list = set()
    for filename in sorted(dict_list):
        for key in dict_list[filename]:
            key_list.add(key)

    f = open(output_file, 'w')

    # Generate and write the header
    header = ""
    for key in sorted(key_list):
        header += "\t" + key
    header += "\n"
    f.write(header.replace("\"", ""))

    # Generate and write each row
    for filename in sorted(dict_list):
        f.write(filename)

        for key in sorted(key_list):
            # Write each value, normalized
            if key in dict_list[filename]:
                f.write("\t")

                # Finish calculating the standard deviation
                mean = score_sum_per_gene[key]/count_per_gene[key]
                sq_val = (score_sum_per_gene[key] * score_sum_per_gene[key])/count_per_gene[key]
                if sq_val < score_sq_sum_per_gene[key]:
                    val = (score_sq_sum_per_gene[key] - sq_val)/(count_per_gene[key] - 1)
                    stdev = math.sqrt(val)
                    normalized_value = abs(dict_list[filename][key] - mean)/stdev
                else:
                    normalized_value = dict_list[filename][key]

                f.write(str(normalized_value))
            else:
                f.write("\t")

        f.write("\n")

    f.close()


def main():
    """
    This is the main function.

    Raises:
        RuntimeError: if there was a problem with the structure or
            contents of the bag
    """
    args = parse_args()

    extract_bag(args.bag_file, args.bagit_data_directory)
    bag = bagit.Bag(args.bagit_data_directory)

    if not bag.is_valid():
        raise RuntimeError("invalid bag (%s)" % (args.bag_link))

    meta_file = get_meta_file(args.bagit_data_directory)
    if meta_file is None:
        raise RuntimeError("no %s file found in bag" % (DEFAULT_META_FILE))

    annotations, structure = parse_meta_file(meta_file)

    gene_desc_col, score_desc_col = parse_structure(structure, args.gene_desc, args.score_desc)
    if not gene_desc_col:
        raise RuntimeError("no columns match gene descriptor '%s'" % (args.gene_desc))
    if not score_desc_col:
        raise RuntimeError("no columns match score descriptor '%s'" % (args.score_desc))

    dict_list, count_per_gene, score_sum_per_gene, score_sq_sum_per_gene = \
        gather_data(args.gene_desc, gene_desc_col,
                    args.score_desc, score_desc_col,
                    args.bagit_data_directory, annotations)

    output_data(args.output_file, dict_list, count_per_gene,
                score_sum_per_gene, score_sq_sum_per_gene)


if __name__ == "__main__":
    main()


