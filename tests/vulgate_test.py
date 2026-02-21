import pytest, os,sys, csv, re
from tffast.tfData.tfVulgate import TfVulgate
from tffast.env import debug,mylog
vul=None
@pytest.fixture()
def VUL():
    global vul
    if(not vul):
        vul= TfVulgate()
    return vul


def test_getLex_test(VUL):
    tests=[
        {'id': 1, 'lex':'Aaron'}
    ]
    for t in tests:
        assert(VUL.getLex(t['id']).lemma == t['lex'])

def test_getRefs(VUL):
    tests=[
        {'id': 1, 'refs':'Exodus 24:1'}
    ]
    for t in tests:
        assert(t['refs'] in VUL.getLexRefs(t['id'])['refs'])

def test_getText(VUL):
    tests=[
        {'section':602193, 'text':'in principio erat Verbum et Verbum erat apud Deum et Deus erat Verbum'}
    ]
    for t in tests:
        assert(t['text'] == VUL.getText(t['section']).strip())