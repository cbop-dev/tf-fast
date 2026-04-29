import pytest, os,sys, csv, re
from tffast.tfData.tfBHS import TfBHS
from tffast.tfData.tfLXX import TfLXX
from versification_utils import remap_verses
from tffast.env import debug,mylog
from tffast.utils.bibleUtils import BibleUtils
from tffast.utils.utils import createNumArrayFromStringListRange
#import tffast.utils.bibleNames as BibleNames
from tffast.MyDatasets import getDataset,loadDatasets
from tf.app import use
from tf.advanced import sections as Sections


datasetMap={}
testTF=True
def loadTheDataset(db):
    if(testTF):
        return getDataset(db)
    else:
        return None

#global bhs
#bhs = bhs if bhs else None
#global lxx
#lxx = lxx if lxx else None
@pytest.fixture()
def BHS():
 #   global bhs
  #  global datasetMap
    bhs=loadTheDataset('bhs')
    #bhs= TfBHS()
    return bhs

@pytest.fixture()
def LXX():
    #global lxx
    #if(not lxx):
        #lxx= TfLXX()
    #global datasetMap
    return loadTheDataset('lxx')

def test_dummy():
    assert(True)


def test_remapExternalPackage():
    verses = {
        "PSA 22:31": "The last verse of Psalm 22",
        "PSA 23:6": "The last verse of Psalm 23"
    }

    from_schema = "eng"
    to_schema = "org"
    new_verses = remap_verses(verses, from_schema, to_schema)
    assert("PSA 22:32" in new_verses.keys())
    assert("PSA 22:31" not in new_verses.keys())
    # {'PSA 22:32': 'The last verse of Psalm 22', 'PSA 23:6': 'The last verse of Psalm 23'}

    from_schema = "eng"
    to_schema = "lxx"
    new_verses = remap_verses(verses, "eng", "lxx")
    assert("PSA 21:32" in new_verses.keys())
    assert("PSA 22:31" not in new_verses.keys())

def test_myRemapMethod():

    tests = [
        {'in': "PSA 22:31", 'out': "PSA 21:31", 'from':'bhs', 'to':'lxx'},
        {'in': "Ps 22:31", 'out': "PSA 21:31", 'from':'bhs', 'to':'lxx'},
        {'in': "PSA 22:3", 'out': "PSA 22:3", 'from':'bhs', 'to':'bhs'},
        {'in': "2SA 2:3", 'out': "2SA 2:3", 'from':'bhs', 'to':'lxx'},
        {'in': "DAN 13:1", 'out': "DAN 13:1", 'from':'lxx', 'to':'vulgate'},
        {'in': "EST 4:22", 'out': "EST 4:22", 'from':'lxx', 'to':'web'},
        {'in': "DAN 3:37", 'out': "S3Y 1:14", 'from':'vulgate', 'to':'lxx'},
       # "PSA 23:6": "The last verse of Psalm 23"
    ]

    for t in tests:
        out = BibleUtils.remapVerses([t['in']], t['from'], t['to'])
        assert(len(out)>0)
        assert(t['out'] == out[0])
        

def test_getBookMapAbbrev():
    assert(BibleUtils.getBookMapAbbrev("Genesis") == "GEN")
    assert(BibleUtils.getBookMapAbbrev("Exodus") == "EXO")

def test_reverseBookAbbrev():
    tests=[
        {'in': "GEN", 'out': "Gen", 'version':'bhs'},
        {'in': "EXO", 'out': "Exod", 'version':'bhs'},
        {'in': "LEV", 'out': "Lev", 'version':'bhs'},
        {'in': "NUM", 'out': "Num", 'version':'bhs'},
        {'in': "GEN", 'out': "Gen", 'version':'lxx'},
        {'in': "EXO", 'out': "Exod", 'version':'lxx'},
        {'in': "LEV", 'out': "Lev", 'version':'lxx'},
        {'in': "NUM", 'out': "Num", 'version':'lxx'},
        {'in': "DAN", 'out': "DanTh", 'version':'lxx'}
      
    ]
    for t in tests:
        assert(BibleUtils.getTfBookAbbrev(t['in'], t['version']) == t['out'])

def test_getBookMapAbbrev():
    tests=[
        {'in': 'Ps', 'out': 'PSA'},
        {'in': 'PSA', 'out': 'PSA'},
        {'in': 'Ps(s)', 'out': 'PSA'},
        {'in': 'Psa', 'out': 'PSA'},
        {'in': 'Psalmi', 'out': 'PSA'},
        {'in': 'Psalms', 'out': 'PSA'},
        {'in': 'psa', 'out': 'PSA'},
        {'in': 'psalms', 'out': 'PSA'},
        {'in': 'ps', 'out': 'PSA'},
        {'in': 'Ps', 'out': 'PSA'},
        {'in': 'Pss', 'out': 'PSA'},
    ]
    for t in tests:
        assert(BibleUtils.getBookMapAbbrev(t['in']) == t['out'])


def test_getParallelVerses(BHS,LXX):
    pass

    assert(BibleUtils.getBookMapAbbrev('Ps')=='PSA')
    if (BHS and LXX):
        tests=[
            {'ref': "Gen 1:1", 'from':'bhs', 'to':'lxx', 'outRef': 'GEN 1:1', 'outText':["ἐν ἀρχῇ ἐποίησεν ὁ θεὸς τὸν οὐρανὸν καὶ τὴν γῆν"]},
            {'ref': "Dan 3:37", 'from':'vulgate', 'to':'lxx', 'outRef': 'DAN 3:37', 'outText':["ὅτι δέσποτα ἐσμικρύνθημεν παρὰ πάντα τὰ ἔθνη καί ἐσμεν ταπεινοὶ ἐν πάσῃ τῇ γῇ σήμερον διὰ τὰς ἁμαρτίας ἡμῶν"]},
            {'ref': "Ps 23:1", 'from':'bhs', 'to':'vulgate', 'outRef':'PSA 22:1','outText':['psalmus David Dominus reget me et nihil mihi deerit']}
        ]

        for t in tests:
            parRef = BibleUtils.remapVerses([t['ref']], t['from'], t['to'])[0]
            toDb=loadTheDataset(t['to'])
            mylog(f"Remapped {t['ref']} to {parRef}")
            parRef=toDb.remapVerseCorrection(parRef)
            mylog(f"Corrected {t['ref']} to {parRef}")
            assert(parRef == t['outRef'])
            
            bcv=BibleUtils.getBcVfromRef(parRef) 
            vlist=createNumArrayFromStringListRange(bcv['vv'])
            textList=[]
            for v in vlist:
                node=toDb.getNodeFromBcV(bcv['book'],bcv['chap'],v)
                text=toDb.getText(node) if node else ''
                textList.append(text)
            
            assert(textList == t['outText'])

        
    