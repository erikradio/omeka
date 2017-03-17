import requests
import json
import csv
from jsonpatch import JsonPatch
from re import match

from xml.etree import ElementTree as ET
# this script creates accessions from a csv

endpoint = "http://quigon.library.arizona.edu/drsw/api/"
apikey = ""

cred = {'key': apikey}




# id 260 for otherlocation
#serno is 251

# gggget=requests.get(endpoint+"items?").json()
# print(gggget)


# def addOtherLoc():
#     newElement = {"name": "Other Location", "description": "",
#                   "comment": "", "element_set": {"id": 4}}
#     makeElement = requests.post(
#         endpoint + "elements", params=cred, data=json.dumps(newElement)).json()



def getLoc():
    drswDict={}
    with open('masterfile_20160811.xml') as mfile:
        tree=ET.parse(mfile)
        root=tree.getroot()
        for rec in root.findall('rec'):
            serno=rec.find('serno')
            otherLoc=rec.find('othloc')
            if otherLoc is not None:
                drswDict[serno.text] = otherLoc.text
    return drswDict

import csv, json
import sys
import requests


def read_file_get_list_of_dicts(infile_path):
    """
    __Args__

    1. infile_path (str): The path to the input file

    __Returns__

    * out_rows (list): A list of dictionaries populated with the existing
        csv data
    """
    out_rows = []
    with open(infile_path, mode='rU', errors='ignore') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            out_rows.append(row)
    return out_rows


def write_list_of_dicts_to_file(outfile_path, out_rows, field_names):
    """
    __Args__

    1. outfile_path (str): The path to the output file
    2. out_rows (list): A list of dictionaries containing data
    3. field_names (list): A list of strings containing field names
        which are present in EVERY dictionary in the out_rows array
    """
    with open(outfile_path, 'w') as resultsFile:
        writer = csv.DictWriter(resultsFile, field_names)
        writer.writeheader()
        for out_row in out_rows:
            writer.writerow(out_row)


def main():
    # Grab our infile_path and outfile_path from the cli
    infile_path = sys.argv[1]
    outfile_path = sys.argv[2]

    # Specify our original fields
    original_fields = [
        'Occupation','Biography','Bibliography','Source','Title','BID','Language','Birth','Death',
        'Marriage','Ethnicity','Occupation','UnFamily','Family','Baptism','Confirmation','Notes',
        'See Also','Other','Second Marriage','Third Marriage','UnResidents','Residents','Author',
        'Documentation','Misc Note','Precis','Serial Number','Persons','Places','Keywords','Ethnic Group',
        'General Subject','Original Location','First Location','Other Location'
        ]

    # Get our original data structure
    rows = read_file_get_list_of_dicts(infile_path)
    original_fields = [x for x in rows[0].keys()]

    # Manipulate that structure however we want, in this case I add another
    # column to everything called "brian_column" that has a random uuid in it

    for row in rows:

        


                # Take every entry in our list of "last, first" strs and jam them
                # together into one big string separated by the double pipe
                # characters.

                row['Crossref_author'] = "||".join(auth_names)
                row['Crossref_title'] = title
                row['Crossref_issn'] = issn
                row['Crossref_journal'] = journal_title

    # Now we've finished manipulating our data structure, we want to write it
    # back into csv somewhere on disk. Keep in mind I added a column, so I
    # have to specify that in the field_names array

    # make our field_names array reflect any changes in the data

    # copy our original the cheating-y way because strings are immutable
    field_names = [x for x in original_fields]
    # add the column we added to everything
    field_names.append('Crossref_author')
    field_names.append('Crossref_title')
    field_names.append('Crossref_journal')
    field_names.append('Crossref_author')
    field_names.append('Crossref_issn')

    write_list_of_dicts_to_file(outfile_path, rows, field_names)

# make this a safe-ish cli script
if __name__ == '__main__':
    main()
