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
              {'refs': [('Matthew',1,[1])],'options':{'lexemes': True}},
              {'refs': [('Matthews',1,[1])]},
              {'sections': [382714,382715],'options':{'showVerses': True}},
              {'sections': [382714],'options':{'lexemes': True}},
    ]
    results=[
        {'texts':["καὶ καθὼς ἐγένετο ἐν ταῖς ἡμέραις Νῶε, οὕτως ἔσται καὶ ἐν ταῖς ἡμέραις τοῦ Υἱοῦ τοῦ ἀνθρώπου·"]},
        {'texts':["Βίβλος γενέσεως Ἰησοῦ Χριστοῦ υἱοῦ Δαυεὶδ υἱοῦ Ἀβραάμ."]},
        {'texts':['']},
        {'texts':["1 Βίβλος γενέσεως Ἰησοῦ Χριστοῦ υἱοῦ Δαυεὶδ υἱοῦ Ἀβραάμ.", 
                  "2 Ἀβραὰμ ἐγέννησεν τὸν Ἰσαάκ, Ἰσαὰκ δὲ ἐγέννησεν τὸν Ἰακώβ, Ἰακὼβ δὲ ἐγέννησεν τὸν Ἰούδαν καὶ τοὺς ἀδελφοὺς αὐτοῦ,"]},
        {'texts':["Βίβλος γενέσεως Ἰησοῦ Χριστοῦ υἱοῦ Δαυεὶδ υἱοῦ Ἀβραάμ."]},
    ]
    assert len(requests) == len(results)
    for i in range(0,len(requests)):
        testReq = requests[i]
        testRes = results[i]
        response =client.post(f"/nt/texts/",json=testReq).json()
        doLexes= testReq['options']['lexemes'] if 'options' in testReq.keys() and 'lexemes' in testReq['options'].keys() else False
        if ('sections' in testReq.keys()):
            assert len(testReq['sections'])== len(testRes['texts'])
            assert len(response['texts']) == len(testReq['sections'])
            
            print("===========")
            print("response:  ")
            print(response)
            #assert not doLexes
            
        elif('refs' in testReq.keys()):
            assert len(testReq['refs'])== len(testRes['texts'])
            assert len(response['texts']) == len(testReq['refs'])
        for x in range(0,len(testRes['texts'])):
            assert response['texts'][x] == testRes['texts'][x]
            if (doLexes):
                assert(len(response['words'][x]) == len(testRes['texts'][x].split()))
                assert(" ".join(map(lambda w: w['word'],response['words'][x]))==testRes['texts'][x])