import pytest, os,sys
from tffast.tfData.tfLXX import TfLXX
from tffast.tfData.tfDataset import POS
lxx=None
@pytest.fixture()
def LXX():
    global lxx
    if(not lxx):
        lxx= TfLXX()
    return lxx


def test_getLex_test(LXX):
    tests=[
        {'id': 59428, 'lex':'ἀκαθαρσία'}
    ]
    for t in tests:
        assert(LXX.getLemma(t['id']) == t['lex'])


def test_commonLexes(LXX):
    tests = [
        {'sections':[623751,623752], 'count':46, 'lexes':['γῆ','βρῶσις']} #gen 1-2
    ]

    for t in tests:
        commons=LXX.getLexemes2(sections=t['sections'],common=True)
        assert(len(commons['common'])==t['count'])
        for l in t['lexes']:
            assert(l in commons['common'])
#        assert(LXX.countLexInSection(t['lemma'], t['section'])==t['count'])

def test_restricted(LXX):
    tests=[
        {'sections': [623751], 'total':114, 'nouns': 42,'noNouns':72}
    ]
    for t in tests:
        lexes = LXX.getLexemes2(sections=t['sections'])
        nouns = LXX.getLexemes2(sections=t['sections'],restrict=[POS.NOUN.value])
        noNouns = LXX.getLexemes2(sections=t['sections'],exclude=[POS.NOUN.value])
        assert(lexes and lexes['lexemes'] and (len(lexes['lexemes']) == t['total']))
        #assert(nouns and nouns['lexemes'])
        assert(len(nouns['lexemes']) == t['nouns'])
        assert(len(noNouns['lexemes']) == t['noNouns'] and len(noNouns['lexemes']) == t['total'] - t['nouns'])

def test_posEnums(LXX):
    tests=[
        {'wordid':10363,'posEnums':[POS.CONJUNCTION.value,POS.PRONOUN_RELA.value]}
    ]
    for t in tests:
        assert(set(LXX.getPosEnums(t['wordid'])) == set(t['posEnums']))
