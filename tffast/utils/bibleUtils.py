from tffast.tfData.tfBHS import TfBHS
from tffast.tfData.tfLXX import TfLXX
from tffast.tfData.tfWEB import TfWEB
from tffast.tfData.tfNT import TfN1904
from tffast.tfData.tfVulgate import TfVulgate
from tffast.tfData.tfSBLGNT import TfSBLGNT
from versification_utils import remap_verses
from tffast.tfData.tfDataset import TfDataset
from tffast.env import debug,mylog
import re
class BibleUtils:
    """
    tfs={
        'bhs':TfBHS(),
        'lxx':TfLXX(),
        'web':TfWEB(),
        'nt':TfNT(),
        'vulgate':TfVulgate(),
        'sblgnt':TfSBLGNT()
    }
  
    mapNames = {
        'eng':['WEB'], #this could be wrong for a Catholic Bible, as the versification_utils defines 'eng' as "English (Protestant)" 
                       #see https://github.com/jcuenod/versification_utils

        'vul':['vulgate'],
        'lxx':['lxx'],
        'org':['bhs','lxx','sblgnt','nt'] #this is the default mapping
    }
    """
    mapNames={
        'WEB':'eng',
        'vulgate':'vul',
        'lxx':'lxx',
        'sblgnt':'org',
        'nt':'org',
        'bhs':'org'
    }

    @staticmethod
    def remapVerses(verses,fromTfName, toTfName):

        """ 
        verses: list of verse strings
        fromTfName: abbrev of the tf dataset to remap from
        toTfName: abbrev of the tf dataset to remap to
        """
        fromSchema = BibleUtils.mapNames[fromTfName] if fromTfName in BibleUtils.mapNames else None
        toSchema = BibleUtils.mapNames[toTfName] if toTfName in BibleUtils.mapNames else None
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
        

        #getBookChapVerseFromRef(refString, replaceUnderscores=true) {
    """
    function getBookChapVerseFromRef(refString, replaceUnderscores=true) {

    // mylog(`getBookChapVerseFromRef(${refString})`, true);
        refString = cleanString(refString, replaceUnderscores);
        let book = null, chap = book, v = book;
        //NB books with only 1 chap: [Phlm, Jude,2 John, 3 John]
        let badInput = false;
        if (refString.split(":").length == 2) {//got explicit verses
            let bookChap = '';
            [bookChap, v] = refString.split(":");
            if (v) { //got verses as expected
                const bookChapObj = splitBookChap(bookChap, replaceUnderscores);
                book = bookChapObj.book;
                chap = bookChapObj.chap;
            }
            else { //what?? bad input: colon with not verses! (e.g., "Eph 2:")
                badInput = true;
                mylog("bad input with colon: '" + refString + "'");
            }
        }
        else { //no verses, just book and chap
            const bookChapObj = splitBookChap(refString, replaceUnderscores);
            book = bookChapObj.book;
            chap = bookChapObj.chap;
            if (!chap) {
                // mylog("getBookChapVerseFromRef("+refString+") got no chap!"+chap)
            }

        }
        return { book: book, chap: chap, v: v }
    }
    """

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

"""
    splitBookChap(string, replaceUnderscores=true) {
    //reading 'chapters' which might actually be verses, i.e., Jude 3a
    const matches = cleanString(string, replaceUnderscores).match(/^(([1-4]+[ _]*)?[a-zA-Z _]+)([ _]+([0-9a-z-]+))?$/); 
    let theBook = null, theChap = theBook;

    if (matches && matches.length >= 5) { //got chapter
        theBook = matches[1];
        theChap = matches[4] ? matches[4] : null;
    }
    else if (matches && matches[1]) {//just a book
        theBook = matches[1];

    }
    else {
        //error
        mylog("splitBookChap could not parse '" + string + "'");
    }

//    mylog("splitBookChap(string)->{b:" + theBook + ", c:"+theChap+"}",true);
    return { book: theBook, chap: theChap }
}
"""