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
        assert(BibleUtils.bcvToRef(bcv)==t['in'])




def test_splitBookChap_test():
    tests=[
        {'in':"Gen 1", 'out':{'book': 'Gen', 'chap': '1'}},
        {'in':"S3Y 1", 'out':{'book': 'S3Y', 'chap': '1'}}
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

def test_getStandarizedBookName_test():

    tests=[
        {'in':"Gen", 'out':"Genesis"},
        {'in':"GEN", 'out':"Genesis"},
        {'in':"1SA", 'out':"1 Samuel"},
        {'in':"1Sa", 'out':"1 Samuel"},
        {'in':"1_Samuel", 'out':"1 Samuel"},
        
    ]
    for t in tests:
        sbn=BibleUtils.getStandarizedBookName(t['in'])
        assert(sbn is not '')
        assert(sbn==t['out'])



    assert(True)