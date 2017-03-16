import requests
import json
import csv
import uuid
import re
from jsonpatch import JsonPatch
from re import match
import xmltodict
import untangle

from xml.etree import ElementTree as ET
# this script creates accessions from a csv

endpoint = "http://quigon.library.arizona.edu/drsw/api/"
apikey = "d53121b54845ebac8669d9118bba54f913432718"

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

def getOmekaItems():
    getItems=requests.get(endpoint+'items?collection=2&page=1&per_page=18000')
    records=json.loads(getItems.text)
    
    # for x in records:
    #      first_subdiv_id = x['id']
    #      for second in x['element_texts']:
    #          second_subdiv_id = second['element']['id']
    #          if second_subdiv_id == 251:
    #              print(first_subdiv_id, second_subdiv_id)



def main():
    getLoc()
    getOmekaItems()


if __name__ == '__main__':
    main()
# print(makeElement)
# auth = requests.post(aspace_url+"/users/"+username+"/login?password="+password).json()
# session = auth["session"]
# headers = {"X-ArchivesSpace-Session":session}
#
# # print(headers)
#
# with open("final_accession.csv","rU") as csvFile:
# 	reader=csv.DictReader(csvFile)
# 	for row in reader:
#
# 		if len(Provenance) > 0 and len(AccType) > 0:
# 			acc_records={"title":title,"id_0":AccNo,"jsonmodel_type":"accession","accession_date":AccDate,
# 			"extents":[{"jsonmodel_type":"extent","extent_type":"linear_feet","portion":"whole","number":Size}],
# 			"resource_type":"collection","acquisition_type":AccType,"general_note":Notes,"content_description":Abstract,
# 			"provenance":Provenance}
# 			acc_post=requests.post(aspace_url+"/repositories/2/accessions",headers=headers,data=json.dumps(acc_records)).json()
# 			print(acc_post.status_code)
#
#
# 			print(acc_post)
# 		if len(Provenance) > 0 and len(AccType)==0:
# 			acc_records={"title":title,"id_0":AccNo,"jsonmodel_type":"accession","accession_date":AccDate,
# 			"extents":[{"jsonmodel_type":"extent","extent_type":"linear_feet","portion":"whole","number":Size}],
# 			"resource_type":"collection","acquisition_type":"gift","general_note":Notes,"content_description":Abstract,
# 			"provenance":Provenance}
# 			acc_post=requests.post(aspace_url+"/repositories/2/accessions",headers=headers,data=json.dumps(acc_records)).json()
#
#
# 			print(acc_post)
#
#
#
#
# 		if len(Provenance) == 0 and len(AccType) > 0:
# 			acc_data={"title":title,"id_0":AccNo,"jsonmodel_type":"accession","accession_date":AccDate,
# 			"extents":[{"jsonmodel_type":"extent","portion":"whole","extent_type":"cubic_feet","number":Size,}],
# 			"content_description":Abstract,"resource_type":"collection","acquisition_type":AccType,"general_note":Notes}
# 			acc_post=requests.post(aspace_url+"/repositories/2/accessions",headers=headers,data=json.dumps(acc_data)).json()
#
# 			print(acc_post)
# 		if len(Provenance) == 0 and len(AccType) == 0:
# 			acc_data={"title":title,"id_0":AccNo,"jsonmodel_type":"accession","accession_date":AccDate,
# 			"extents":[{"jsonmodel_type":"extent","portion":"whole","extent_type":"cubic_feet","number":Size,}],
# 			"content_description":Abstract,"resource_type":"collection","acquisition_type":"gift","general_note":Notes}
# 			acc_post=requests.post(aspace_url+"/repositories/2/accessions",headers=headers,data=json.dumps(acc_data)).json()
# 			print(acc_post)
