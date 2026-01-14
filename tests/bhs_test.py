import pytest, os,sys
from tffast.tfData.tfBHS import TfBHS
bhs=None
@pytest.fixture()
def BHS():
    global bhs
    if(not bhs):
        bhs= TfBHS()
    return bhs


def test_getLex_test(BHS):
    tests=[
        {'id': 1437603, 'lex':'רֵאשִׁית'}
    ]
    for t in tests:
        assert(BHS.getLemma(t['id']) == t['lex'])

def test_getChapters(BHS):
    tests=[
        {'abbrev': 'Isa', 'chap':47, 'node':427010}
    ]

    for t in tests:
        assert(BHS.getChapter(BHS.lookupBook(t['abbrev']),t['chap']) == t['node'])


def test_properName(BHS):
    props=[
        228531
    ]

    notProps=[
        228546
    ]

    propNames=[
        'בָּבֶל'
    ]
    for p in props:
        assert(BHS.isProperNoun(p))

    for n in notProps:
        assert(not BHS.isProperNoun(n))

    for pn in propNames:
        assert(BHS.lexemes[pn].isProper)

    
def test_countLexSection(BHS):
    tests = [
        {'section':1428929, 'lemma': 'זעק', 'count': 1},
        {'section':426597, 'lemma': 'זעק', 'count': 13},
       
        
        #lex id of 'זעק' is: 439447
    ]

    for t in tests:
        assert(BHS.countLexInSection(t['lemma'], t['section'])==t['count'])

def test_getLexemes2(BHS):
    tests = [
        {'sections': [1414389], 'lexemes':{ #Gen 1:1
            'ברא':{
                'count':1
            }
        }},
        {'sections': [426591], 'lexemes':{ #Gen 
            'ברא':{
                'count':11
            }
        }},
        # # Gen
    
    ]

    for t in tests:
        lexes = BHS.getLexemes2(sections=t['sections'])
        assert(len(lexes['lexemes'].keys())>1)
        print(lexes['lexemes'].keys())

        for (l,obj) in t['lexemes'].items():
            assert(l in lexes['lexemes'].keys())
            if (l in lexes['lexemes'].keys()):
                assert(lexes['lexemes'][l]['count']==obj['count'])


def test_handyDictionary(BHS):
    tests=[
        {'bookname': 'Genesis', 'chap':1,'verses':[1], 'numLexes':9},
        {'bookname': 'Genesis', 'chap':1,'verses':[], 'numLexes':104}
    ]
    for t in tests:
        d=BHS.getHandyDictionary(t['bookname'],t['chap'],t['verses'])
        assert(len(d)==t['numLexes'])
