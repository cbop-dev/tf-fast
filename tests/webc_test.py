import pytest, os,sys, csv, re
from tffast.tfData.tfWEB import TfWEB
from tffast.env import debug,mylog
from tffast.MyDatasets import dataSets,getDataset,loadDatasets
webc=None
@pytest.fixture()
def WEBC():
    global webc
    if(not webc):
        webc=getDataset('web')
    return webc


def test_getLex_test(WEBC):
    tests=[
       # {'id': 0, 'lex':'Aaron'}
    ]
    for t in tests:
        assert(WEBC.getLex(t['id']).lemma == t['lex'])

def test_getRefs(WEBC):
    tests=[
       # {'id': 0, 'refs':'Exodus 24:1'}
    ]
    for t in tests:
        assert(t['refs'] in WEBC.getLexRefs(t['id'])['refs'])

def test_getText(WEBC):
    tests=[
        {'section':879071, 'text':'In the beginning, God created the heavens and the earth.' }#gen 1:1
    ]
    for t in tests:
        assert(t['text'] == WEBC.getText(t['section']).strip())


def test_lookupBook(WEBC):
    tests=[
        {'book':'Matthew', 'node':877716},
        {'book':'Mark', 'node':877717},
        {'book':'Luke', 'node':877718}
    ]
    
    """
       {'book':'John', 'node':875370},
        {'book':'Acts', 'node':875371},
        {'book':'Romans', 'node':875372},
        {'book':'1 Corinthians', 'node':875373},
        {'book':'2 Corinthians', 'node':875374},
        {'book':'Galatians', 'node':875375},
        {'book':'Ephesians', 'node':875376},
        {'book':'Philippians', 'node':875377},
        {'book':'Colossians', 'node':875378},
        {'book':'1 Thessalonians', 'node':875379},
        {'book':'2 Thessalonians', 'node':875380},
        {'book':'1 Timothy', 'node':875381},
        {'book':'2 Timothy', 'node':875382},
        {'book':'Titus', 'node':875383},
        {'book':'Philemon', 'node':875384},
        {'book':'Hebrews', 'node':875385},
        {'book':'James', 'node':875386},
        {'book':'1 Peter', 'node':875387},
        {'book':'2 Peter', 'node':875388},
        {'book':'1 John', 'node':875389},
        {'book':'2 John', 'node':875390},
        {'book':'3 John', 'node':875391},
        {'book':'Jude', 'node':875392},
        {'book':'Revelation', 'node':875393},
    ]
    """

    for t in tests:
        assert(WEBC.lookupBook(t['book']) == t['node'])


def test_getNodeFromBcV(WEBC):
    tests=[
        {'book':'GEN', 'chapter':1, 'verse':'1',  'booknode':877670}
    ]
    for t in tests:
        #assert(WEBC.lookupBook(t['book']) > 0)
        #assert(WEBC.lookupBook(t['book']) == t['booknode'])
        theChapDict=WEBC.getChaptersDict(t['booknode'])
        print(f"chapDict.keys():{theChapDict.keys()}")
        theChap = WEBC.getChapter(t['booknode'],t['chapter'])
        
        print("theChap:"+str(theChap))
        #assert(False)
        #assert(WEBC.getChapter(875321,1) > 0)
        #assert(WEBC.getNodeFromBcV(t['book'],t['chapter'],t['verse']) == t['node'])