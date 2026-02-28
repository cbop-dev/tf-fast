import pytest, os,sys
from tffast.tfData.tfSBLGNT import TfSBLGNT
from tffast.env import mylog, debug
from tffast.utils.greekUtils import GreekUtils
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
        if l==GreekUtils.normalize('Αἰγύπτιος'):
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
        {'id': 59428, 'lex':GreekUtils.normalize('νύξ')},
        {'id': 1, 'lex':GreekUtils.normalize('βίβλος')},
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
        {'search':'Mt','node': 137555},
        {'search':'1 Cor','node': 137561},
        {'search':'1 Thess','node': 137567},
        {'search':'1_Thessalonians','node': 137567},
        {'search':'1 Pet','node': 137575},
        {'search':'2_Peter','node': 137576},
    ]

    for t in tests:
        assert(sblgnt.lookupBook(t['search'])==t['node'])

def test_countLexSection(sblgnt):
    tests = [
        {'section':137555, 'lemma': GreekUtils.normalize('πληρόω'), 'count': 16}, #matt
        #{'section':137780, 'lemma': 'πληρόω', 'count': 15} #error
        #lex id of 'זעק' is: 439447
    ]

    for t in tests:
        assert(sblgnt.countLexInSection(t['lemma'], t['section'])==t['count'])
        assert(True)

def test_getNotes(sblgnt):
    tests=[
        {'b':"Acts",'c':10, 'v':19,'note':"νδρες RP ] + τρεῖς Treg NA28; + δύο WH"},
        {'b':"1_Corinthians",'c':11,'v':15,'note':"δέδοται RP ] + αὐτῇ WH Treg NA28"},   
        {'b':"1 Corinthians",'c':11,'v':15,'note':"δέδοται RP ] + αὐτῇ WH Treg NA28"}, # doesn't work: must use name as in this db, here with underscores, not spaces!
        {'b':'2 John', 'c':1, 'v': 5, 'note':"καινὴν γράφων σοι Treg NA27 ] γράφων σοι καινὴν WH NA28 RP"}
    ]

    for t in tests:
        note = sblgnt.apparatusNote(t['b'],t['c'],t['v'])
        print(f"NOTE found for {t['b']} {t['c']}:{t['v']}: {note}")
        assert(GreekUtils.normalize(t['note']) in GreekUtils.normalize(note))

def test_properNouns(sblgnt):
    notProper = [
        {'lexId': 226, 'proper': False}

    ]
    
    for t in notProper:
        #assert(sblgnt.countLexInSection(t['lemma'], t['section'])==t['count'])
        
        assert(sblgnt.isProperNoun(t['lexId']))
def test_lexes(sblgnt):
    tests=[
        {'lexId': 1537, 'lemma': 'ἐκδαπανάομαι'}
    ]

    for t in tests:
        lex = sblgnt.getLex(t['lexId'])
        print(f"{lex.lemma} should == 'ἐκδαπανάομαι'")
        assert  GreekUtils.normalize(lex.lemma) ==  GreekUtils.normalize(t['lemma'])
        print(lex.gloss)
        #assert 'exhaust' in lex.gloss # this is a mistaken in the TF data! someday I'll fork, fix, and make pull request!