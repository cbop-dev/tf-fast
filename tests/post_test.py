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
    sections={'sections': [385239]}
    texts=["καὶ καθὼς ἐγένετο ἐν ταῖς ἡμέραις Νῶε, οὕτως ἔσται καὶ ἐν ταῖς ἡμέραις τοῦ Υἱοῦ τοῦ ἀνθρώπου·"
    ]
  #  payload = {"sections": [385239]}
    #req=TextsRequest(sections=[385239])
    response  =client.post(f"/nt/texts/",json=sections)
   # assert response.status_code == 200
   # print(response)
   # print("json: ")
    #print(response.json())
    assert len(sections['sections'])== len(texts)
    assert len(response.json()) == len(sections)
    for i in range(0,len(sections)):
        assert response.json()[i] == texts[i]