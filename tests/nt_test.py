import pytest, os,sys
from tffast.tfData.tfNT import TfN1904
from tffast.env import mylog, debug
NT=None

@pytest.fixture()
def nt():
    global NT
    if(not NT):
        NT= TfN1904()
    return NT


def test_lexemesDict(nt):
    #assert(nt.getLex(1).lemma =='Αἰγύπτιος')
    found = False
    for l in nt.lexemes.keys():
        if l=='Αἰγύπτιος':
            found = True
            break
    assert(found)

    ids = [l.id for l in nt.lexemes.values()]
    assert(len(ids)==5396)
    ids.sort()
    assert(ids[-1]==5395)
    assert(ids[0]==0)
    lex=nt.getLex(1000)
    assert(lex and lex.lemma == nt.lexemes[lex.lemma].lemma)

def test_lexCount(nt):
    assert(len(nt.lexemes)==5396)
    
def test_getLemma(nt):
    tests=[
        {'id': 59428, 'lex':'πρό'},
        {'id': 1, 'lex':'βίβλος'},
    ]
    for t in tests:
        assert(nt.getLemma(t['id']) == t['lex'])

def test_getFreq(nt):
    assert (nt.getFreq(1)==20)

def test_getBooks(nt):
    ntbooks = list(nt.getBooks().values())
    mylog(ntbooks)
    assert(len(ntbooks)==27)
    mattFoundAb = [b for b in ntbooks if b['abbrev']=='Matt']
    mattFoundNm = [b for b in ntbooks if b['name']=='Matthew']
    assert(len(mattFoundAb)>0)
    assert(mattFoundAb[0]['words']==18299)
    assert(len(mattFoundNm)>0)
    assert(mattFoundNm[0]['words']==18299)

def test_getVerseFromNode(nt):
    tests = [
        {'node': 382741, 'verse': 3},#Matt 2:3
        {'node': 137808, 'verse': None}#Matt 2
        ]
    for t in tests:
        assert (nt.getVerseNumberFromNode(t['node']) == t['verse'])