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
