import pytest, os,sys, csv, re
from tffast.utils.bibleUtils import BibleUtils


def test_basic():
    tests=[

    ]

    assert(True)


def test_bcv_test():
    tests=[
        {'in':"Gen 1:1", 'out':{'book': 'Gen', 'chap': '1', 'vv': '1'}}
    ]
    


    assert(True)

    for t in tests:
        bcv=BibleUtils.getBcVfromRef(t['in'])
        assert(bcv is not None)
        
        assert(bcv==t['out'])
        for k in ['book','chap','vv']:
            assert(bcv[k] is not None)
            #assert(bcv[k]==t['out'][k])




def test_splitBookChap_test():
    tests=[
        {'in':"Gen 1", 'out':{'book': 'Gen', 'chap': '1'}}
    ]
    


    assert(True)

    for t in tests:
        bc=BibleUtils.splitBookChap(t['in'])
        assert(bc is not None)
        
        assert(bc==t['out'])
        for k in ['book','chap']:
            assert(bc[k] is not None)
            #assert(bcv[k]==t['out'][k])

#splitBookChap