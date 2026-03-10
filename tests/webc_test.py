import pytest, os,sys, csv, re
from tffast.tfData.tfWEB import TfWEB
from tffast.env import debug,mylog
webc=None
@pytest.fixture()
def WEBC():
    global webc
    if(not webc):
        webc= TfWEB()
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