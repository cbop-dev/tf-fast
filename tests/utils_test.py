import pytest, os,sys
from tffast.utils.utils import createNumArrayFromStringListRange
from tffast.utils.greekUtils import GreekUtils
from tffast.env import mylog, debug
# Test the GreekUtils class

def test_greekBeta():
    tests=[
        {'greek':"ἀγάπη", 'beta':'agaph','plain':'αγαπη'}
    ]

    for t in tests:
        assert(GreekUtils.greek_to_beta(t['greek'])==t['beta'])
        assert(GreekUtils.plain_greek(t['greek'])==t['plain'])
    '''
    greek_text = "ἀγάπη"
    beta_text = GreekUtils.greek_to_beta(greek_text)
    mylog(f"Greek to Beta: {greek_text} -> {beta_text}")  # Expected: ἀγάπη -> agaph
    mylog(f"Beta to Greek: {beta_text} -> {GreekUtils.beta_to_greek(beta_text)}")  # Expected: agaph -> αγαπη
    assert(beta_text=='agaph')
    strings = ["ἀγάπη", "ἀγάπης", "λόγος", "ἀγάπῃ"]
    search_result = GreekUtils.fuzzy_search_array("αγαπη", strings)
    mylog(f"Fuzzy search for 'αγαπη': {search_result}")  # Expected: ['ἀγάπη', 'ἀγάπης', 'ἀγάπῃ']

    plain = GreekUtils.plain_greek("ἀγάπη")
    mylog(f"Plain Greek: {plain}")  # Expected: αγαπη
    '''

def test_hebrew_normalize():

    unequals = [
    ["שׁ","\uFB2A"],
    ["שׂ","שׂ"],
    ["שׁ","שׁ"],
    ]

    equals=[["שׁ","\uFB2A"]]

    

    for u in unequals:
        assert u[0] != u[1]

    for e in equals:
        assert e[0] == e[1]

    for u in unequals:
        assert GreekUtils.normalize(u[0]) == GreekUtils.normalize(u[1])

    
def test_createNumArrayFromStringListRange():
    tests=[
        {'in':"1-2",'out':[1,2]},
        {'in':"1-2,4-5",'out':[1,2,4,5]},
        {'in':"4-5,1-2",'out':[1,2,4,5]},
        {'in':"2",'out':[2]},
        {'in':"2,1",'out':[1,2]},
    ]
    for t in tests:
        numList=createNumArrayFromStringListRange(t['in'])
        assert(numList==t['out'])