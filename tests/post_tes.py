import pytest, os
import requests
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#from _old_app import app, load
from tffast.main import create_app, getLexemes, getChaptersDict, getBooksDict
@pytest.fixture()
def base_url():
    return "http://localhost:5000/"

@pytest.fixture()
def loadApp():
    print("Loading app...")
    myApp = create_app()
    print("app loaded?")
   # lexes = app.getLexemes(sections=[1])
    yield myApp

def test_get_text(base_url,loadApp):
    id=385239
    response = requests.get(f"{base_url}/nt/text/{id}")
    assert response.status_code == 200
    assert response.json()['text'] == "καὶ καθὼς ἐγένετο ἐν ταῖς ἡμέραις Νῶε, οὕτως ἔσται καὶ ἐν ταῖς ἡμέραις τοῦ Υἱοῦ τοῦ ἀνθρώπου·"

def test_post_text(base_url, loadApp):
    id=385239
    payload = {"sections": "385239"}
    response = requests.post(f"{base_url}/nt/texts/", json=payload)
    assert response.status_code == 200
    assert response.json()[0]['text'] == "καὶ καθὼς ἐγένετο ἐν ταῖς ἡμέραις Νῶε, οὕτως ἔσται καὶ ἐν ταῖς ἡμέραις τοῦ Υἱοῦ τοῦ ἀνθρώπου·"
