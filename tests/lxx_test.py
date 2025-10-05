import pytest, os,sys
from tffast.tfData.tfLXX import TfLXX
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
