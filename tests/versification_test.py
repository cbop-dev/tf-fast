import pytest, os,sys, csv, re
#from tffast.tfData.tfBHS import TfBHS
#from tffast.tfData.tfLXX import TfLXX
from versification_utils import remap_verses
from tffast.env import debug,mylog
from tffast.utils.bibleUtils import BibleUtils
from tffast.utils.utils import createNumArrayFromStringListRange
#import tffast.utils.bibleNames as BibleNames
#from tffast.MyDatasets import getDataset,loadDatasets
#from tf.app import use
#from tf.advanced import sections as Sections



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

