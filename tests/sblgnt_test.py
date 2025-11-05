import pytest, os,sys
from tffast.tfData.tfSBLGNT import TfSBLGNT
from tffast.env import mylog, debug
SBLGNT=None

@pytest.fixture()
def sblgnt():
    global SBLGNT
    if(not SBLGNT):
        SBLGNT= TfSBLGNT()
    return SBLGNT


def test_lexemesDict(sblgnt):
    #assert(sblgnt.getLex(1).lemma =='Αἰγύπτιος')
    found = False
    for l in sblgnt.lexemes.keys():
        if l=='Αἰγύπτιος':
            found = True
            break
    assert(found)

    ids = [l.id for l in sblgnt.lexemes.values()]
    assert(len(ids)==5461)
    ids.sort()
    assert(ids[-1]==5460)
    assert(ids[0]==0)
    lex=sblgnt.getLex(1000)
    assert(lex and lex.lemma == sblgnt.lexemes[lex.lemma].lemma)

def test_lexCount(sblgnt):
    assert(len(sblgnt.lexemes)==5461)
    
def test_getLemma(sblgnt):
    tests=[
        {'id': 59428, 'lex':'νύξ'},
        {'id': 1, 'lex':'βίβλος'},
    ]
    for t in tests:
        assert(sblgnt.getLemma(t['id']) == t['lex'])

def test_getFreq(sblgnt):
    assert (sblgnt.getFreq(1)==10)

def test_getBooks(sblgnt):
    ntbooks = list(sblgnt.getBooks().values())
    mylog(ntbooks)
    assert(len(ntbooks)==27)
    mattFoundAb = [b for b in ntbooks if b['abbrev']=='Matt']
    mattFoundNm = [b for b in ntbooks if b['name']=='Matthew']
    assert(len(mattFoundAb)>0)
    assert(mattFoundAb[0]['words']==18329)
    assert(len(mattFoundNm)>0)
    assert(mattFoundNm[0]['words']==18329)

def test_getVerseFromNode(sblgnt):
    tests = [
        {'node': 163588, 'verse': 3},#Matt 2:3
        {'node': 137583, 'verse': None}#Matt 2
        ]
    for t in tests:
        assert (sblgnt.getVerseNumberFromNode(t['node']) == t['verse'])

def test_getBook(sblgnt):
    tests=[
        {'search':'Mt','node': 137555}
    ]

    for t in tests:
        assert(sblgnt.lookupBook(t['search'])==t['node'])

def test_countLexSection(sblgnt):
    tests = [
        {'section':137555, 'lemma': 'πληρόω', 'count': 16}, #matt
        #{'section':137780, 'lemma': 'πληρόω', 'count': 15} #error
        #lex id of 'זעק' is: 439447
    ]

    for t in tests:
        assert(sblgnt.countLexInSection(t['lemma'], t['section'])==t['count'])
        assert(True)