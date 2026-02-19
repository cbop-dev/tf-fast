import pytest, os,sys
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

def test_hebrew_normalize:

    unequals = [
    ["שׁ","\uFB2A"],
    ["שׂ","שׂ"],
    ["שׁ","שׁ"],
    ]

    equals=[["שׁ","\uFB2A"]]

    for u in unequals:
        assert u[0] != u[1]

    for e in equals:
        assert u[0] == u[1]

