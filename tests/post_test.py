import pytest, os, unicodedata
import requests
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#from _old_app import app, load
from tffast.main import app,TextsRequest
from tffast.tfData.tfDataset import TfDataset
from tffast.tfData.tfLXX import TfLXX
from tffast.tfData.tfSBLGNT import TfSBLGNT
from tffast.tfData.tfNT import TfN1904
from fastapi import FastAPI
from fastapi.testclient import TestClient
from tffast.env import mylog, debug
from tffast.utils.greekUtils import GreekUtils
import json
from tffast.tfData.tfDataset import POS
from tffast.MyDatasets import dataSets,getDataset,loadDatasets
@pytest.fixture()
def base_url():
    return "http://localhost:5000/"
NT=None
TC=None
VUL=None

@pytest.fixture()
def nt():
    global NT
    if(not NT):
        NT= getDataset('nt')
    return NT

@pytest.fixture()
def vul():
    global VUL
    if(not VUL):
        VUL= getDataset('vulgate')
    return VUL
    
@pytest.fixture()
def lxx():
    return getDataset('lxx')

@pytest.fixture()
def client():
    global TC
    if (not TC):
        TC=TestClient(app)
    return TC

@pytest.fixture()
def sblgnt():
    return getDataset('sblgnt')

@pytest.fixture()
def runner():
    return FastAPI()



def test_get_lexes(client):
    section=137780
    response = client.get(f"/nt/lex?sections={section}")
   # assert response.status_code == 200
   # assert response.json()['text'] == "καὶ καθὼς ἐγένετο ἐν ταῖς ἡμέραις Νῶε, οὕτως ἔσται καὶ ἐν ταῖς ἡμέραις τοῦ Υἱοῦ τοῦ ἀνθρώπου·"
    assert(response.json()['lexemes']['πληρόω']['count']==16)


def test_get_text(client):
    id=385239
    response = client.get(f"/nt/text/{id}")
   # assert response.status_code == 200
    assert response.json()['text'] == "καὶ καθὼς ἐγένετο ἐν ταῖς ἡμέραις Νῶε, οὕτως ἔσται καὶ ἐν ταῖς ἡμέραις τοῦ Υἱοῦ τοῦ ἀνθρώπου·"

def test_post_text(base_url, client):
    requests=[{'sections': [385239],'db':'nt'},
              {'refs': [{'book':'Matthew','chapter':1,'verses':[1]}],'options':{'lexemes': True},'db':'nt'},             
              {'refs': [{'book':'Matthews','chapter':1,'verses':[1]}],'db':'nt'},
              {'sections': [382714,382715],'options':{'showVerses': True},'db':'nt'},
              {'sections': [382714],'options':{'lexemes': True},'db':'nt'},
              {'sections': [1],'options':{'lexemes': False},'db':'vulgate'},
    ]
    results=[
        {'texts':[{'text':"καὶ καθὼς ἐγένετο ἐν ταῖς ἡμέραις Νῶε, οὕτως ἔσται καὶ ἐν ταῖς ἡμέραις τοῦ Υἱοῦ τοῦ ἀνθρώπου·"}]},
        {'texts':[{'text':"Βίβλος γενέσεως Ἰησοῦ Χριστοῦ υἱοῦ Δαυεὶδ υἱοῦ Ἀβραάμ."}]},
        {'texts':[{'text':''}]},
        {'texts':[{'text':"(1) Βίβλος γενέσεως Ἰησοῦ Χριστοῦ υἱοῦ Δαυεὶδ υἱοῦ Ἀβραάμ."}, 
                  {'text':"(2) Ἀβραὰμ ἐγέννησεν τὸν Ἰσαάκ, Ἰσαὰκ δὲ ἐγέννησεν τὸν Ἰακώβ, Ἰακὼβ δὲ ἐγέννησεν τὸν Ἰούδαν καὶ τοὺς ἀδελφοὺς αὐτοῦ,"}]},
        {'texts':[{'text':"Βίβλος γενέσεως Ἰησοῦ Χριστοῦ υἱοῦ Δαυεὶδ υἱοῦ Ἀβραάμ."}]},
        {'texts':[{'text':"liber"}]}
    ]
    assert len(requests) == len(results)
    for i in range(0,len(requests)):
        testReq = requests[i]
        testRes = results[i]
        response =client.post(f"/{requests[i]['db']}/texts/",json=testReq).json()
        doLexes= testReq['options']['lexemes'] if 'options' in testReq.keys() and 'lexemes' in testReq['options'].keys() else False
        mylog("the response: ")
        mylog(response)
       #assert not doLexes #for printing!
        if ('sections' in testReq.keys()):
            print(str(response))
            assert len(testReq['sections'])== len(testRes['texts'])
            assert len(response['texts']) == len(testReq['sections'])
            
            mylog("===========")
            mylog("response:  ")
            
            
        elif('refs' in testReq.keys()):
            assert len(testReq['refs'])== len(testRes['texts'])
            assert len(response['texts']) == len(testReq['refs'])
        for x in range(0,len(testRes['texts'])):
            assert response['texts'][x]['text'] == testRes['texts'][x]['text']
            if (doLexes):
                assert(len(response['texts'][x]['words'][0]['words']) == len(testRes['texts'][x]['text'].split()))
                assert(" ".join(map(lambda w: w['word'],response['texts'][x]['words'][0]['words']))==testRes['texts'][x]['text'])


def test_post_ref(base_url, client):
    tests=[
          {'input':{"refs":[],"sections":[137582],"min":1,"max":0,"options":{"common":False,"pos":True,"beta":True,"plain":False,"checkProper":True,"gloss":True}},
         'output':{"totalLexemes":129}},
         {'input':{"refs":[],"sections":[137582],"restrict":[0,2,4,11],"exclude":[],"min":1,"max":0,"options":{"common":False,"pos":True,"beta":True,"plain":False,"checkProper":True,"gloss":True}},
         'output':{"totalLexemes":57}},
         {'input':{"refs":[],"sections":[137582],"exclude":[0,2,4,11],"min":1,"max":0,"options":{"common":False,"pos":True,"beta":True,"plain":False,"checkProper":True,"gloss":True}},
         'output':{"totalLexemes":72}}
    ]
    for test in tests:
        response =client.post(f"/sblgnt/lex",json=test['input']).json()
        #mylog("the response: ",True)
        #mylog(response,True)
        print(str(response))
        assert 'totalLexemes' in response.keys()
        assert response['totalLexemes'] == test['output']['totalLexemes']

def test_verseMap(base_url, client):
    tests=[
          {'input':{"refs":[{'book': 'Gen','chapter':1,'verses':[1]}],'src':'lxx','to':['bhs']}, 'output':{'bhs':['Gen 1:1']}},
          {'input':{"refs":[{'book': 'PSA','chapter':22,'verses':[1]}],'src':'lxx','to':['bhs']}, 'output':{'bhs':['PSA 23:1']}},
          {'input':{"refs":[{'book': 'Ps','chapter':22,'verses':[1]}],'src':'lxx','to':['bhs']}, 'output':{'bhs':['Ps 23:1']}},
          ##^ doesn't work yet. Got to convert book names!
    ]
    for t in tests:
        response =client.post(f"/{t['input']['src']}/versemap",json=t['input']).json()
        #mylog("the response: ",True)
        #mylog(response,True)
        print(str(response))
        #assert 'totalLexemes' in response.keys()
        assert response == t['output']
