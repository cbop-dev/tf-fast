from tffast.tfData.tfBHS import TfBHS
from tffast.tfData.tfLXX import TfLXX
from tffast.tfData.tfWEB import TfWEB
from tffast.tfData.tfNT import TfN1904
from tffast.tfData.tfVulgate import TfVulgate
from tffast.tfData.tfSBLGNT import TfSBLGNT
from versification_utils import remap_verses
from tffast.tfData.tfDataset import TfDataset
from tffast.env import debug,mylog
from tffast.utils.bibleNames import getTfBookAbbrev,getBookMapAbbrev
import re
class BibleUtils:

    # mape to abbreviations used in the versification_utils package (external dependency)
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
        verses: list of verse strings
        fromTfName: abbrev of the tf dataset to remap from
        toTfName: abbrev of the tf dataset to remap to
        """
        fromSchema = BibleUtils.mapNames[fromTfName] if fromTfName in BibleUtils.mapNames.keys() else None
        toSchema = BibleUtils.mapNames[toTfName] if toTfName in BibleUtils.mapNames.keys() else None
        ret = []
        if (fromSchema and toSchema):
            newVersesDict = remap_verses({v:'' for v in verses}, fromSchema, toSchema)
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
        

    @staticmethod
    def splitBookChap(string, replaceUnderscores=True):
        pass
        theBook =None
        theChap = theBook

        matches=re.search(r"^(([1-4]+[ _]*)?[a-zA-Z _]+)([ _]+([0-9a-z-]+))?$", string)
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
