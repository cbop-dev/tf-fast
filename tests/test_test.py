import pytest, os
import sys, json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
##import app as app
from fastapi import FastAPI
from fastapi.testclient import TestClient

##app = FastAPI()
from tffast.main import app
from tffast.tfData.tfDataset import TfDataset
from tffast.tfData.tfLXX import TfLXX
from tffast.tfData.tfNT import TfN1904
NT=None

@pytest.fixture()
def base_url():
    return "http://localhost:5000/"
    # clean up / reset resources here
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

#app = create_app
#lexes = app.getLexemes(sections=[623751,623752],common=True)
#print("; ".join(lexes['common']))

#print("hello world!")
#lexes = app.getLexemes(sections=[623694,623694],common=True)
#print(lexes['common'])

#def not_getLex(runner,client):
#   x = 1
    # vocab of Genesis
   # lexes = runner.getLexemes(sections=[623694])
   # assert lexes['totalLexemes'] == 2096
   # assert len(list(lexes['lexemes'])) == 2096
    #print("hello")

'''
def not_getCommonLexes(runner):
    # Gen 1 and 2
    lexes = runner.getLexemes(sections=[623751,623752],common=True)
    assert lexes['totalLexemes'] == 213
    
    assert len(list(lexes['lexemes'])) == 213

    assert len(lexes['common']) == 46
    #assert lexes['common'][0]=="fred"
    #assert type(lexes['common']) == 'list'

def not_getVersesFromNodeRange1():
    db='nt'
    start=382714
    end=382716
    expected = "Βίβλος γενέσεως Ἰησοῦ Χριστοῦ υἱοῦ Δαυεὶδ υἱοῦ Ἀβραάμ. Ἀβραὰμ ἐγέννησεν τὸν Ἰσαάκ, Ἰσαὰκ δὲ ἐγέννησεν τὸν Ἰακώβ, Ἰακὼβ δὲ ἐγέννησεν τὸν Ἰούδαν καὶ τοὺς ἀδελφοὺς αὐτοῦ, Ἰούδας δὲ ἐγέννησεν τὸν Φαρὲς καὶ τὸν Ζαρὰ ἐκ τῆς Θάμαρ, Φαρὲς δὲ ἐγέννησεν τὸν Ἐσρώμ, Ἐσρὼμ δὲ ἐγέννησεν τὸν Ἀράμ, "
    output = app.getVersesFromNodeRange(start,end,False,db)
    assert (expected.strip() == output.strip())


def ts_getVersesFromRange():
    lookupRange = {'start':385239, 'end':385249} #Luke 17:26-37
        # NB: dataset has no Luke 17:36
    
    expected = {'reference': "Luke 17:26-37",
     "text": "καὶ καθὼς ἐγένετο ἐν ταῖς ἡμέραις Νῶε, οὕτως ἔσται καὶ ἐν ταῖς ἡμέραις τοῦ Υἱοῦ τοῦ ἀνθρώπου· ἤσθιον, ἔπινον, ἐγάμουν, ἐγαμίζοντο, ἄχρι ἧς ἡμέρας εἰσῆλθεν Νῶε εἰς τὴν κιβωτόν, καὶ ἦλθεν ὁ κατακλυσμὸς καὶ ἀπώλεσεν πάντας. ὁμοίως καθὼς ἐγένετο ἐν ταῖς ἡμέραις Λώτ· ἤσθιον, ἔπινον, ἠγόραζον, ἐπώλουν, ἐφύτευον, ᾠκοδόμουν· ᾗ δὲ ἡμέρᾳ ἐξῆλθεν Λὼτ ἀπὸ Σοδόμων, ἔβρεξεν πῦρ καὶ θεῖον ἀπ’ οὐρανοῦ καὶ ἀπώλεσεν πάντας. κατὰ τὰ αὐτὰ ἔσται ᾗ ἡμέρᾳ ὁ Υἱὸς τοῦ ἀνθρώπου ἀποκαλύπτεται. ἐν ἐκείνῃ τῇ ἡμέρᾳ ὃς ἔσται ἐπὶ τοῦ δώματος καὶ τὰ σκεύη αὐτοῦ ἐν τῇ οἰκίᾳ, μὴ καταβάτω ἆραι αὐτά, καὶ ὁ ἐν ἀγρῷ ὁμοίως μὴ ἐπιστρεψάτω εἰς τὰ ὀπίσω. μνημονεύετε τῆς γυναικὸς Λώτ. ὃς ἐὰν ζητήσῃ τὴν ψυχὴν αὐτοῦ περιποιήσασθαι, ἀπολέσει αὐτήν, καὶ ὃς ἂν ἀπολέσει, ζωογονήσει αὐτήν. λέγω ὑμῖν, ταύτῃ τῇ νυκτὶ ἔσονται δύο ἐπὶ κλίνης μιᾶς, ὁ εἷς παραλημφθήσεται καὶ ὁ ἕτερος ἀφεθήσεται· ἔσονται δύο ἀλήθουσαι ἐπὶ τὸ αὐτό, ἡ μία παραλημφθήσεται ἡ δὲ ἑτέρα ἀφεθήσεται. καὶ ἀποκριθέντες λέγουσιν αὐτῷ Ποῦ, Κύριε; ὁ δὲ εἶπεν αὐτοῖς Ὅπου τὸ σῶμα, ἐκεῖ καὶ οἱ ἀετοὶ ἐπισυναχθήσονται."}
    result = app.getVersesFromNodeRange(lookupRange['start'],lookupRange['end'],False,'nt')
    assert (result.strip() == expected['text'].strip())

def not_getNodeFromBcV():
    db='nt'
    test = {
     'book': "Matthew", 'c':1, 'v':1, 'node': 382714,
    "text": "Βίβλος γενέσεως Ἰησοῦ Χριστοῦ υἱοῦ Δαυεὶδ υἱοῦ Ἀβραάμ."
    }
    

    node = app.getNodeFromBcV(test['book'], test['c'], test['v'],db)
    assert (node == test['node'])
    text = app.getText(node, db)
    assert (text == test['text'])

def not_test(client,runner):
    count = 1
    #count = lxx.getLexCount()
    assert(count > 0)
'''
def test_get(client):
    response = client.get("/nt/text/1")
    print("response = ")
    print(response)
    
    mydata=response.json()
    print(mydata)
    assert(mydata['text']=='Βίβλος')
    #assert(False)