import pytest, os
import requests
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#from _old_app import app, load
from tffast.main import app,TextsRequest
from tffast.tfData.tfDataset import TfDataset
from tffast.tfData.tfLXX import TfLXX
from tffast.tfData.tfNT import TfN1904
from fastapi import FastAPI
from fastapi.testclient import TestClient
from tffast.env import mylog, debug
import json

@pytest.fixture()
def base_url():
    return "http://localhost:5000/"
NT=None
@pytest.fixture()
def nt():
    global NT
    if(not NT):
        NT= TfN1904()
    return NT

@pytest.fixture()
def lxx():
    return TfLXX()

@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def runner():
    return FastAPI()


def test_get_text(client):
    id=385239
    response = client.get(f"/nt/text/{id}")
   # assert response.status_code == 200
    assert response.json()['text'] == "καὶ καθὼς ἐγένετο ἐν ταῖς ἡμέραις Νῶε, οὕτως ἔσται καὶ ἐν ταῖς ἡμέραις τοῦ Υἱοῦ τοῦ ἀνθρώπου·"

def test_post_text(base_url, client):
    requests=[{'sections': [385239]},
              {'refs': [{'book':'Matthew','chapter':1,'verses':[1]}],'options':{'lexemes': True}},
              {'refs': [{'book':'Matthews','chapter':1,'verses':[1]}]},
              {'sections': [382714,382715],'options':{'showVerses': True}},
              {'sections': [382714],'options':{'lexemes': True}},
    ]
    results=[
        {'texts':[{'text':"καὶ καθὼς ἐγένετο ἐν ταῖς ἡμέραις Νῶε, οὕτως ἔσται καὶ ἐν ταῖς ἡμέραις τοῦ Υἱοῦ τοῦ ἀνθρώπου·"}]},
        {'texts':[{'text':"Βίβλος γενέσεως Ἰησοῦ Χριστοῦ υἱοῦ Δαυεὶδ υἱοῦ Ἀβραάμ."}]},
        {'texts':[{'text':''}]},
        {'texts':[{'text':"(1) Βίβλος γενέσεως Ἰησοῦ Χριστοῦ υἱοῦ Δαυεὶδ υἱοῦ Ἀβραάμ."}, 
                  {'text':"(2) Ἀβραὰμ ἐγέννησεν τὸν Ἰσαάκ, Ἰσαὰκ δὲ ἐγέννησεν τὸν Ἰακώβ, Ἰακὼβ δὲ ἐγέννησεν τὸν Ἰούδαν καὶ τοὺς ἀδελφοὺς αὐτοῦ,"}]},
        {'texts':[{'text':"Βίβλος γενέσεως Ἰησοῦ Χριστοῦ υἱοῦ Δαυεὶδ υἱοῦ Ἀβραάμ."}]},
    ]
    assert len(requests) == len(results)
    for i in range(0,len(requests)):
        testReq = requests[i]
        testRes = results[i]
        response =client.post(f"/nt/texts/",json=testReq).json()
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