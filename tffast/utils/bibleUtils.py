import json
#from tffast.tfData.tfBHS import TfBHS
#from tffast.tfData.tfLXX import TfLXX
#from tffast.tfData.tfWEB import TfWEB
#from tffast.tfData.tfNT import TfN1904
#from tffast.tfData.tfVulgate import TfVulgate
#from tffast.tfData.tfSBLGNT import TfSBLGNT
from versification_utils import remap_verses
#from tffast.tfData.tfDataset import TfDataset
from tffast.env import debug,mylog
from tffast.utils.bibleNames import getTfBookAbbrev,getBookMapAbbrev,getStandarizedBookName
import re
class BibleUtils:

    # map to abbreviations used in the versification_utils package (external dependency)
    # see https://github.com/jcuenod/versification_utils
    mapNames={
        'web':'eng',
        'vulgate':'vul',
        'lxx':'lxx',
        'sblgnt':'org',
        'nt':'org',
        'bhs':'org'
    }

    @staticmethod
    def getTfBookAbbrev(book,versification):
        return getTfBookAbbrev(book,versification)

    @staticmethod
    def getBookMapAbbrev(name):
        return getBookMapAbbrev(name)

    @staticmethod
    def remapVerses(verses,fromTfName, toTfName):

        """ 
        verses: list[int[
            list of verse strings, like ['Gen 1:1','Ps 12:3']
        fromTfName: string
            abbrev of the tf dataset to remap from
        toTfName: string
            abbrev of the tf dataset to remap to
        
        Returns: list[string]
            Returns of mapped verse strings, where the book names have been standardized to match those in bibleNames.py, that is, recognized by versificaion_utils
        """
        fromSchema = BibleUtils.mapNames[fromTfName] if fromTfName in BibleUtils.mapNames.keys() else None
        toSchema = BibleUtils.mapNames[toTfName] if toTfName in BibleUtils.mapNames.keys() else None
        ret = []
        if (fromSchema and toSchema):
            refList=[]
            for verse in verses:
                bcv = BibleUtils.getBcVfromRef(verse)
                bookMapAbbrev=BibleUtils.getBookMapAbbrev(bcv['book'])
                if (bookMapAbbrev):
                    bcv['book']=bookMapAbbrev
                    theNewRef = BibleUtils.bcvToRef(bcv)
                    refList.append(theNewRef)
                    print(f"Remapping {verse} to {theNewRef}")
                else:
                    mylog(f"Could not find book abbreviation for {bcv['book']}", True)

            newVersesDict = remap_verses({ref:'' for ref in refList}, fromSchema, toSchema)

            if (newVersesDict):
                ret = list(newVersesDict.keys())
        return ret

    @staticmethod
    def getBcVfromRef(ref):
        pass
        [bookChap,vv]=ref.split(":")

        bookChapObj=BibleUtils.splitBookChap(bookChap)
        book=None
        chap=None
        if (bookChapObj):
            book=bookChapObj['book']
            chap=bookChapObj['chap']

        return {'book':book,'chap':chap,'vv':vv}
        
    def bcvToRef(bcv,keys=['book','chap','vv']):
        return f"{bcv[keys[0]]} {bcv[keys[1]]}{(":"+bcv[keys[2]]) if bcv[keys[2]] else ''}"

    @staticmethod
    def splitBookChap(string, replaceUnderscores=True):
        pass
        theBook =None
        theChap = theBook

        matches=re.search(r"^(([1-4]+[ _]*)?[0-9a-zA-Z _]+)([ _]+([0-9a-z-]+))$", string)
        # match[0]: book; 1:number of book if any; 2:space+chap; 3: chap
        if (matches):
            if (matches.group(0)): #book
            #got chap
                pass
                theBook=matches.group(1)
            if (matches.group(4)): #chap
                theChap=matches.group(4)
        else:
            print(f"Got not matches for {string}")
        return {'book':theBook,'chap':theChap} 

    @staticmethod
    def getStandarizedBookName(synonym):
        """
            getStandarizedBookName: Returns a book name for the book with the given synonymn or abbreviation.
            synonym: the synonym for the book name. 
            returns a string, the "standardized" book name if found, or an empty string if none found
        """
        return getStandarizedBookName(synonym)