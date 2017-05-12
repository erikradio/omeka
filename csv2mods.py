# -- coding: utf-8 --
import csv, sys, time, datetime, xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring

#2015-10-07. Converts gould_books.csv to MODS. Records are for plates only but book records can be derived or use existing MARC records.
# dict[key][0] etc
# add second date for bird ksrl_sc_gould_ng_1_2_002.tif - 1880:01:01
xmlFile = 'newBatch.xml'
xmlData = open(xmlFile, 'w')
# dataFile=sys.argv[1]

ts=time.time()
st=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')

root = Element('mods:modsCollection')
root.set('xmlns:xsi','http://www.w3.org/2001/XMLSchema-instance')
root.set('xmlns:mods', 'http://www.loc.gov/mods/v3')
root.set('xsi:schemaLocation', 'http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-6.xsd')
tree = ET.ElementTree(root)


with open(sys.argv[1], 'rU',errors='ignore') as csvfile:
    reader = csv.DictReader(csvfile)


    for row in reader:

        record = SubElement(root, 'mods:mods')
        record.set('xsi:schemaLocation', 'http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-6.xsd')
        # inserts filename as local identifier
        identifier = SubElement(record, 'mods:identifier')
        identifier.set('type', 'local')
        identifier.text = row['Identifier']


        titleInfo = SubElement(record, 'mods:titleInfo')
        title=SubElement(titleInfo,'mods:title')
        title.text = row['Title']

        partNo=SubElement(titleInfo,'mods:partNumber')
        partNo.text = row['Part']
        typeImage=SubElement(record,'mods:typeOfResource')
        typeImage.text = row['TypeOfResource']

        originInfo=SubElement(record,'mods:originInfo')
        dateCreated=SubElement(originInfo,'mods:dateCreated')
        dateCreated.set('encoding','w3cdtf')
        dateCreated.text=row['DateCreated']

        pub=SubElement(originInfo,'mods:publisher')
        pub.text = row['Publisher']



        namerow = row['CreatorName'].split('|')


        name = SubElement(record,'mods:name')
        name.set('type','personal')
        namePart = SubElement(name,'mods:namePart')
        role = SubElement(name,'mods:role')
        roleTermcode = SubElement(role,'mods:roleTerm')
        roleTermcode.set('type','code')

        roleTermtext = SubElement(role,'mods:roleTerm')
        roleTermtext.set('type','text')


        for x in namerow:
            y=x.split(';')
            namePart.text = y[0]
            roleTermtext.text = y[1]
            








        # info about the nature of the resource. not from the spreadsheet
        # physDesc=SubElement(record,'mods:physicalDescription')
        # digOr=SubElement(physDesc,'mods:digitalOrigin')
        # digOr.text='reformatted digital'
        # form=SubElement(physDesc,'mods:form')
        # form.set('type','material')
        # form.set('authorityURI','http://vocab.getty.edu/aat')
        # form.set('valueURI','http://vocab.getty.edu/aat/300041379')
        # form.text='lithograph'
        # interMed=SubElement(physDesc,'mods:internetMediaType')
        # interMed.text='image/tiff'
        #
        # genre=SubElement(record,'mods:genre')
        #
        # genre.text='Ornithological illustration'
        # accessCond=SubElement(record,'mods:accessCondition')
        # accessCond.set('type','use and reproduction')
        # accessCond.text='This work is in the public domain and is available for users to copy, use, and redistribute in part or in whole. No known restrictions apply to the work.'
        #
        # # related item was used for the host parent of the plate, e.g. the monographic volume
        # relatedItem=SubElement(record,'mods:relatedItem')
        # relatedItem.set('type','host')
        #
        #
        #
        # relOrInfo=SubElement(relatedItem,'mods:originInfo')
        # relOrInfo.set('eventType','publication')
        # bookRow=row['Book']
        #
        # if bookRow in books:
        #     relTitleInfo=SubElement(relatedItem,'mods:titleInfo')
        #     relTitle=SubElement(relTitleInfo,'mods:title')
        #     relTitle.text=books.get(bookRow)[0]
        #     relPart=SubElement(relatedItem,'mods:part')
        #     relDet=SubElement(relPart,'mods:detail')
        #     relDet.set('type','volume')
        #     relNum=SubElement(relDet,'mods:number')
        #     relNum.text=row['Part']
        #     if relNum.text=='S':
        #         relNum.text='Supplement'
        #     relLoc=SubElement(relatedItem,'mods:location')
        #
        #     relIdentifier=SubElement(relatedItem,'mods:identifier')
        #     relIdentifier.set('type','oclc')
        #     relIdentifier.text=books.get(bookRow)[5]
        #     relLang=SubElement(relatedItem,'mods:language')
        #     relLangCode=SubElement(relLang,'mods:languageTerm')
        #     relLangCode.set('type','code')
        #     relLangCode.set('authority','639-2')
        #     relLangCode.text='eng'
        #     relLangText=SubElement(relLang,'mods:languageTerm')
        #     relLangText.set('type','text')
        #     relLangText.text='English'
        #     relGenre=SubElement(relatedItem,'mods:genre')
        #     relGenre.text='Illustrated ornithological books'
        #
        #
        #     pubs=books.get(bookRow)[3].split(';')
        #     for x in pubs:
        #         relPub=SubElement(relOrInfo,'mods:publisher')
        #
        #         relPub.text=x
        #
        #
        #
        #     # this wasn't in the spreadsheet, but I used London for the place of publication
        #     relPlace=SubElement(relOrInfo,'mods:place')
        #     relPlaceTerm=SubElement(relPlace,'mods:placeTerm')
        #     relPlaceTerm.text=books.get(bookRow)[2]
        #
        #     relphysText=SubElement(relLoc,"mods:physicalLocation")
        #     relphysText.set('type','text')
        #     relphysText.text='University of Kansas. Kenneth Spencer Research Library'
        #     relphysCode=SubElement(relLoc,'mods:physicalLocation')
        #     relphysCode.set('authority','marcorg')
        #     relphysCode.text='KFS'
        #     relShelf=SubElement(relLoc,'mods:shelfLocator')
        #     relShelf.text=books.get(bookRow)[4]
        #
        #     relEd=SubElement(relOrInfo,'mods:edition')
        #     if '-' in books.get(bookRow)[1]:
        #
        #         relDateStart=SubElement(relOrInfo,'mods:dateIssued')
        #         relDateStart.set('point','start')
        #         relDateEnd=SubElement(relOrInfo,'mods:dateIssued')
        #         relDateEnd.set('point','end')
        #
        #         relDateStart.text=books.get(bookRow)[1][0:4]
        #         relDateEnd.text=books.get(bookRow)[1][5:10]
        #     else:
        #         relDate=SubElement(relOrInfo,'mods:dateIssued')
        #         relDate.text=books.get(bookRow)[1]
        #
        #
        # if row['Edition']=='1S':
        #     relEd.text='1st'
        # else:
        #     relEd.text=row['Edition']
        #
        #
        # # For supplements with same titles as host book or with second editions
        #
        # if relTitle.text=='Monograph of the Trogonidae, or family of trogons' and relEd.text=='2nd ed.':
        #     relDate.text='1875'
        # if relTitle.text=='Monograph of the Ramphastidae, or family of toucans' and row['Part']=='S':
        #     relDate.text='1855'
        #     relTitle.text='Supplement to the first edition of A monograph of the Ramphastidae, : or family of toucans'
        #     relIdentifier.text='ocm05916002'
        #     relShelf.text='Ellis Aves H17 item 2'
        # if relTitle.text=='Monograph of the Ramphastidae, or family of toucans' and relEd.text=='2nd ed.':
        #     relDate.text='1854'
        #     relPub.text='Taylor and Francis'
        #     relIdentifier.text='ocm11587418'
        #     relShelf='Ellis Aves H126'
        # if relTitle.text=='Monograph of the Trochilidae, or family of hummingbirds' and row['Edition']=='1S':
        #     relSubTit=SubElement(relTitleInfo,'mods:subTitle')
        #     relDate.text='1887'
        #     relSubTit.text='Completed after the author\'s death by R. Bowdler Sharpe'
        #     relPub.text='H. Sotheran &amp;   Co.'
        # if relTitle.text=='Birds of Australia' and row['Edition']=='1S':
        #     relTitle.text='The birds of Australia, supplement'
        #     relIdentifier.text='ocm07568143'
        #     relShelf.text='Ellis Aves H130'
        #
        #
        #
        #
        #
        #
        #
        # recordInfo=SubElement(record,'mods:recordInfo')
        # recordConSo=SubElement(recordInfo,'mods:recordContentSource')
        # recordConSo.set('authority','naf')
        # recordConSo.set('authorityURI','http://id.loc.gov/authorities/names')
        # recordConSo.set('valueURI','http://id.loc.gov/authorities/names/n82079265.html')
        # recordConSo.text='University of Kansas'
        # recordID=SubElement(recordInfo,'mods:recordIdentifier')
        # recordID.text=row['BaseFileName']
        # recordOrigin=SubElement(recordInfo,'mods:recordOrigin')
        # recordOrigin.text='Records prepared through a combination of local MARC records and a local database for biological subjects.'
        # recordCreDate=SubElement(recordInfo,'mods:recordCreationDate')
        # recordCreDate.set('encoding','w3cdtf')
        # recordCreDate.text=st
        #
        #
        # # print tostring(root)




tree.write('newBooks.xml',xml_declaration=True, encoding="UTF-8")
