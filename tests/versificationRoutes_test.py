import pytest, os,sys, csv, re
from tffast.tfData.tfBHS import TfBHS
from tffast.tfData.tfLXX import TfLXX
from fastapi import FastAPI
from fastapi.testclient import TestClient
from versification_utils import remap_verses
from tffast.env import debug,mylog
from tffast.utils.bibleUtils import BibleUtils
from tffast.utils.utils import createNumArrayFromStringListRange
#import tffast.utils.bibleNames as BibleNames
from tffast.MyDatasets import getDataset,loadDatasets
from tf.app import use
from tf.advanced import sections as Sections
from tffast.main import app

myDebug=True
TC=None
datasetMap={}
testTF=True
def loadTheDataset(db):
    if(testTF):
        return getDataset(db)
    else:
        return None
@pytest.fixture()

def client():
    global TC
    if (not TC):
        TC=TestClient(app)
    return TC

@pytest.fixture()
def base_url():
    return "http://localhost:5000/"

@pytest.fixture()
def BHS():
 #   global bhs
  #  global datasetMap
    bhs=loadTheDataset('bhs')
    #bhs= TfBHS()
    return bhs

@pytest.fixture()
def LXX():
    #global lxx
    #if(not lxx):
        #lxx= TfLXX()
    #global datasetMap
    return loadTheDataset('lxx')




@pytest.fixture()
def runner():
    return FastAPI()


def test_getParallelVerses(BHS,LXX):
    pass

    assert(BibleUtils.getBookMapAbbrev('Ps')=='PSA')
    if (BHS and LXX):
        tests=[
            {'ref': "Gen 1:1", 'from':'bhs', 'to':'lxx', 'outRef': 'GEN 1:1', 'outText':["ἐν ἀρχῇ ἐποίησεν ὁ θεὸς τὸν οὐρανὸν καὶ τὴν γῆν"]},
            {'ref': "Dan 3:37", 'from':'vulgate', 'to':'lxx', 'outRef': 'DAN 3:37', 'outText':["ὅτι δέσποτα ἐσμικρύνθημεν παρὰ πάντα τὰ ἔθνη καί ἐσμεν ταπεινοὶ ἐν πάσῃ τῇ γῇ σήμερον διὰ τὰς ἁμαρτίας ἡμῶν"]},
            {'ref': "Ps 23:1", 'from':'bhs', 'to':'vulgate', 'outRef':'PSA 22:1','outText':['psalmus David Dominus reget me et nihil mihi deerit']}
        ]

        for t in tests:
            parRef = BibleUtils.remapVerses([t['ref']], t['from'], t['to'])[0]
            toDb=loadTheDataset(t['to'])
            mylog(f"Remapped {t['ref']} to {parRef}")
            parRef=toDb.remapVerseCorrection(parRef)
            mylog(f"Corrected {t['ref']} to {parRef}")
            assert(parRef == t['outRef'])
            
            bcv=BibleUtils.getBcVfromRef(parRef) 
            vlist=createNumArrayFromStringListRange(bcv['vv'])
            textList=[]
            for v in vlist:
                node=toDb.getNodeFromBcV(bcv['book'],bcv['chap'],v)
                text=toDb.getText(node) if node else ''
                textList.append(text)
            
            assert(textList == t['outText'])


def test_verseMapRoute(client,BHS,LXX):

    
    
    if (BHS and LXX):
        tests=[
            {'ref': "Gen 1:1", 'from':'bhs', 'to':['lxx'], 'out': ['GEN 1:1'],'corrected':['GEN 1:1']},
            {'ref': "Dan 3:37", 'from':'vulgate', 'to':['lxx'], 'out': ['S3Y 1:14'],'corrected':['DAN 3:37']},
            {'ref': "Ps 23:1", 'from':'bhs', 'to':['vulgate'], 'out':['PSA 22:1'],'corrected':['PSA 22:1']}
        ]

        for t in tests:
            #parRef = BibleUtils.remapVerses([t['ref']], t['from'], t['to'])[0]
            db=t['from']
            
            ref=BibleUtils.getBcVfromRef(t['ref'])

            request={
                "to": t['to'],
                'refs':[{'book':ref['book'],'chapter':ref['chap'], 'verses':createNumArrayFromStringListRange(ref['vv'])}]
            }
            response = client.post(f"{db}/versemap",json=request).json()

            mylog(f"verseMapRoute({t['ref']},{t['from']}-->{t['to']}):",myDebug)
            mylog(response,myDebug)

            for i,toVersion in enumerate(t['to']):
                toDb=loadTheDataset(toVersion)
                respRefs=response[toVersion]
                assert(respRefs == t['out'])
                
                for j,respRef in enumerate(respRefs):
                    corrected=toDb.remapVerseCorrection(respRef)
                    assert(corrected == t['corrected'][j])
            #mylog(f"Remapped {t['ref']} to {parRef}")
            #parRef=toDb.remapVerseCorrection(parRef)
            #mylog(f"Corrected {t['ref']} to {parRef}")
            #assert(parRef == t['outRef'])
            
   

#src/to